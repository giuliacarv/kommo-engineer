#!/usr/bin/env python3
"""Kommo Engineer CLI — ações locais; nenhuma requisição remota."""
from __future__ import annotations
import argparse
import contextlib
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import uuid
from pathlib import Path

VERSION = "0.5.0-rc.1"
SKILL = Path(__file__).resolve().parent.parent
SAFE_TOKEN_RE = re.compile(r"(?i)(bearer\s+\S+|(?:api[_ -]?key|access[_ -]?token|refresh[_ -]?token|password|secret)\s*[:=]\s*['\"]?\S+)")
GOAL_RE = re.compile(r"^META-\d{3,}$")

class KEError(Exception):
    pass

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")

def uid():
    return uuid.uuid4().hex[:12]

def sanitize(s: str):
    # Defense-in-depth, but do not rely on regex as complete secret detection.
    return SAFE_TOKEN_RE.sub("[SEGREDO_REMOVIDO]", s)

def readj(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise KEError(f"Não foi possível ler JSON válido: {path.name}: {e}")

def write_bytes_once(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
    except FileExistsError:
        raise KEError(f"Recusa sobrescrita: {path}")

def atomic_write(path: Path, data: bytes):
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=None
    try:
        fd, name=tempfile.mkstemp(prefix=".ke-",dir=path.parent)
        tmp=Path(name)
        with os.fdopen(fd,"wb") as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if tmp and tmp.exists(): tmp.unlink()

def putj(path: Path, data, once=False):
    raw=(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)+"\n").encode("utf-8")
    if once: write_bytes_once(path,raw)
    else: atomic_write(path,raw)

def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for part in iter(lambda:f.read(65536),b""): h.update(part)
    return h.hexdigest()

def getroot(raw, new=False, init_existing=False):
    if not raw: raise KEError("--project é obrigatório")
    p=Path(raw).expanduser().absolute()
    if p==Path(p.anchor) or p==Path.home().absolute():
        raise KEError("Recusa operar na raiz do disco ou na pasta HOME")
    # Do not follow a link in the project path, including junction-like links available to pathlib.
    for part in [p,*p.parents]:
        if part.exists() and (part.is_symlink() or getattr(part,"is_junction",lambda:False)()):
            raise KEError("Pasta ou ancestral simbólico não permitido")
    if new and p.exists(): raise KEError("Projeto já existe. Não sobrescrevo.")
    if not new and not init_existing and not (p/".kommo-engineer"/"project.json").is_file():
        raise KEError("Projeto Kommo Engineer não encontrado nessa pasta")
    if init_existing and not p.is_dir(): raise KEError("--use-existing-dir requer pasta existente")
    return p.resolve()

def data_dir(root):
    return root/".kommo-engineer"

def gp(root, goal):
    if not GOAL_RE.fullmatch(goal): raise KEError("ID de meta inválido")
    base=data_dir(root)/"goals"/goal
    if not base.is_dir(): raise KEError(f"Meta inexistente: {goal}")
    return base

def ensure_safe_relative(root: Path, candidate: Path):
    path=(root/candidate).resolve() if not candidate.is_absolute() else candidate.resolve()
    if not path.is_relative_to(root.resolve()):
        raise KEError("Caminho fora do projeto")
    if not path.is_file(): raise KEError(f"Evidência não encontrada: {path}")
    if path.stat().st_size > 2_000_000: raise KEError("Evidência excede 2 MB; selecione trecho sanitizado")
    return path

@contextlib.contextmanager
def locked(root):
    runtime=data_dir(root)/".runtime"
    runtime.mkdir(parents=True,exist_ok=True)
    lock=runtime/"write.lock"
    try:
        fd=os.open(lock, os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    except FileExistsError:
        raise KEError("Outra escrita ou bloqueio abandonado detectado. Faça diagnóstico; não apague às cegas.")
    try:
        os.write(fd,f"pid={os.getpid()} at={now()}\n".encode())
        os.close(fd)
        if (runtime/"pending-operation.json").exists():
            raise KEError("Operação anterior interrompida. Inspecione .runtime/pending-operation.json")
        yield
    finally:
        if lock.exists(): lock.unlink()

def begin_pending(root, operation, **details):
    p=data_dir(root)/".runtime"/"pending-operation.json"
    putj(p,dict(operation=operation,created_at=now(),**details),once=True)
    return p

def event(root, name, summary, goal=None, simulated=False):
    path=data_dir(root)/"events"/f"{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uid()}.json"
    putj(path,dict(event_id=path.stem,at=now(),type=name,summary=sanitize(summary)[:500],goal_id=goal,simulated=simulated),once=True)
    return path

def setup_contract():
    return readj(SKILL / "schemas" / "setup-fields.json")


def required_setup_fields():
    return [k for k, meta in setup_contract()["fields"].items() if meta["required"]]


def setup_summary(project):
    contract = setup_contract()
    specs = contract["fields"]
    answers = project["answers"]
    required = [k for k, meta in specs.items() if meta["required"]]
    missing = [k for k in required if answers.get(k, {}).get("status") != "confirmed"]
    proposed = [k for k in specs if answers.get(k, {}).get("status") == "proposed"]
    deferred = [k for k in specs if answers.get(k, {}).get("status") == "deferred"]
    confirmed = [k for k in specs if answers.get(k, {}).get("status") == "confirmed"]
    core = contract["planning_core"]
    planning_ready = all(answers.get(k, {}).get("status") == "confirmed" for k in core)
    status = ("complete" if not missing else
              "ready_for_planning" if planning_ready else "in_progress")
    next_field = next((k for k in required if k in missing and
                        answers.get(k, {}).get("status") != "deferred"), None)
    if next_field is None and missing:
        next_field = missing[0]
    next_question = (dict(field=next_field, question=specs[next_field]["question"],
                          example=specs[next_field]["example"], group=specs[next_field]["group"])
                     if next_field else None)
    return dict(status=status, missing=missing, proposed=proposed, deferred=deferred,
                confirmed=confirmed, pending_optional=[k for k, meta in specs.items()
                                if not meta["required"] and answers.get(k, {}).get("status") == "pending"],
                fields={k: answers.get(k, {}).get("status", "pending") for k in specs},
                next_question=next_question, planning_ready=planning_ready,
                complete=not missing)


def ensure_safe_text(value):
    if not isinstance(value, str) or not value.strip():
        raise KEError("Resposta vazia")
    if len(value) > 3000:
        raise KEError("Resposta grande demais; resuma em até 3000 caracteres")
    if "\x00" in value or SAFE_TOKEN_RE.search(value):
        raise KEError("Possível credencial ou segredo detectado; não registre no projeto")
    return value.strip()


def prepare_agents(root, name):
    agents = root / "AGENTS.md"
    section = (
        "<!-- kommo-engineer:start -->\n"
        "## Kommo Engineer — contexto local\n"
        f"Projeto: {sanitize(name)}\n"
        "Ative `$kommo-engineer` quando a tarefa envolver Kommo. "
        "Leia `.kommo-engineer/state.json` e apenas a meta pertinente.\n"
        "Setup: `.kommo-engineer/project.json`. Metas: `.kommo-engineer/goals/`. "
        "Evidências e snapshots: `.kommo-engineer/snapshots/`.\n"
        "Não exponha credenciais nem presuma autorização de alterações remotas.\n"
        "<!-- kommo-engineer:end -->\n"
    )
    if not agents.exists():
        write_bytes_once(agents, (f"# Projeto {sanitize(name)}\n\n" + section).encode("utf-8"))
        return "created"
    if agents.is_symlink() or not agents.is_file():
        raise KEError("AGENTS.md existente não é arquivo regular seguro")
    prior = agents.read_text(encoding="utf-8")
    if "<!-- kommo-engineer:start -->" in prior or "<!-- kommo-engineer:end -->" in prior:
        raise KEError("AGENTS.md já contém seção Kommo Engineer; confirme manualmente")
    atomic_write(agents, (prior.rstrip() + "\n\n" + section).encode("utf-8"))
    return "appended"

def create_project(root, name, business, goal, simulation=False, use_existing=False):
    name, goal = ensure_safe_text(name), ensure_safe_text(goal)
    if "\n" in name or "\r" in name:
        raise KEError("Nome do projeto deve ocupar uma linha")
    business = ensure_safe_text(business) if business else ""
    if use_existing:
        if not root.is_dir() or (data_dir(root) / "project.json").exists():
            raise KEError("--use-existing-dir exige pasta existente, sem projeto Kommo Engineer")
        if data_dir(root).exists():
            raise KEError("Pasta .kommo-engineer já existe; não reutilizo sem inspeção")
        if (root / "AGENTS.md").exists():
            ag = root / "AGENTS.md"
            if not ag.is_file() or ag.is_symlink():
                raise KEError("AGENTS.md existente não pode ser preservado com segurança")
            content = ag.read_text(encoding="utf-8")
            if "<!-- kommo-engineer:start -->" in content or "<!-- kommo-engineer:end -->" in content:
                raise KEError("Seção Kommo já existe; não duplico")
    else:
        getroot(str(root), new=True)
        root.mkdir(parents=True)
    d = data_dir(root)
    spec = setup_contract()["fields"]
    answers = {k: dict(value=None, status="pending", source=None, confirmed_at=None)
               for k in spec}
    for k, v in (("business", business), ("goal", goal)):
        if v:
            answers[k] = dict(value=v, status="proposed" if simulation else "confirmed",
                              source="fixture" if simulation else "usuario",
                              confirmed_at=None if simulation else now())
    project = dict(schema_version=2, project_id=uid(), name=name,
                   created_at=now(), updated_at=now(), revision=1,
                   setup_status="in_progress",
                   environment="simulation" if simulation else "unverified",
                   account_id=None, answers=answers)
    project["setup_status"] = setup_summary(project)["status"]
    state = dict(schema_version=2, revision=1, project_id=project["project_id"],
                 active_goal_id=None, last_goal_id=None,
                 next_action="Concluir o setup" if not simulation else "Revisar o resultado da simulação",
                 updated_at=now())
    putj(d / "project.json", project, once=True)
    putj(d / "state.json", state, once=True)
    write_bytes_once(d / "scope.md",
        b"# Escopo do projeto\n\n> Em elaboracao. Defina objetivos e decisoes durante o setup.\n")
    agents_action = prepare_agents(root, name)
    event(root, "project_created", f"Projeto inicializado: {name}", simulated=simulation)
    return dict(project_id=project["project_id"], name=name, setup_status=project["setup_status"],
                agents_action=agents_action, environment=project["environment"])

def project_status(root):
    proj=readj(data_dir(root)/"project.json")
    state=readj(data_dir(root)/"state.json")
    return dict(project=proj["name"],project_id=proj["project_id"],environment=proj["environment"],
                setup_status=proj["setup_status"],active_goal_id=state["active_goal_id"],
                last_goal_id=state["last_goal_id"],next_action=state["next_action"],
                recovery_required=(data_dir(root)/".runtime"/"pending-operation.json").exists())

def project_resume(root):
    d = data_dir(root)
    project = readj(d / "project.json")
    st = readj(d / "state.json")
    setup = setup_summary(project)
    active = st.get("active_goal_id")
    latest = active or st.get("last_goal_id")
    goal = None
    if latest:
        gs = readj(gp(root, latest) / "state.json")
        goal = dict(id=latest, title=gs["title"], status=gs["status"],
                    plan=f".kommo-engineer/goals/{latest}/plan-v{gs['plan_version']:03}.md",
                    next_action=gs.get("next_action"), snapshot_id=gs.get("snapshot_id"))
    return dict(project=project["name"], project_id=project["project_id"],
                project_file=".kommo-engineer/project.json",
                state_file=".kommo-engineer/state.json",
                setup_status=setup["status"],
                missing_required=setup["missing"],
                next_question=setup["next_question"],
                active_goal_id=active, last_goal_id=st.get("last_goal_id"), goal=goal,
                next_action=st.get("next_action"),
                recommended_next_action=("Criar primeira meta ou revisar prioridades" if
                    setup["complete"] and st.get("next_action") == "Concluir o setup" else
                    "Planejar primeira meta (pendências não críticas ainda abertas)" if
                    setup["planning_ready"] and st.get("next_action") == "Concluir o setup" else
                    st.get("next_action")),
                recovery_required=(d / ".runtime" / "pending-operation.json").exists(),
                note="Estado documental local; não prova situação atual da conta Kommo")


def setup_status(root):
    p = readj(data_dir(root) / "project.json")
    result = setup_summary(p)
    result["stored_status"] = p.get("setup_status")
    result["revision"] = p.get("revision")
    return result

def setup_update(root, field, value=None, proposed=False, deferred=False,
                 not_applicable=False, reason=None):
    specs = setup_contract()["fields"]
    if field not in specs:
        raise KEError(f"Campo desconhecido: {field}. Consulte setup status")
    if deferred and (proposed or not_applicable):
        raise KEError("Ação contraditória para resposta")
    if not_applicable and proposed:
        raise KEError("Ação contraditória para resposta")
    if not_applicable and specs[field]["required"]:
        raise KEError("Campo obrigatório não admite not_applicable")
    if deferred or not_applicable:
        if value is not None:
            raise KEError("Não informe --value ao adiar/marcar inaplicável")
        if not reason or not reason.strip():
            raise KEError("--reason é obrigatório para defer/not_applicable")
        clean = None
        notes = ensure_safe_text(reason)
        new_status = "deferred" if deferred else "not_applicable"
    else:
        clean = ensure_safe_text(value)
        notes = ensure_safe_text(reason) if reason else None
        new_status = "proposed" if proposed else "confirmed"
    with locked(root):
        p = readj(data_dir(root) / "project.json")
        old = p["answers"].get(field, {})
        if (old.get("value") == clean and old.get("status") == new_status and
                old.get("notes") == notes):
            return setup_status(root)
        p["answers"][field] = dict(value=clean, status=new_status,
                    source="usuario" if not proposed else "hipotese",
                    confirmed_at=now() if new_status == "confirmed" else None,
                    notes=notes)
        p["revision"] += 1
        p["updated_at"] = now()
        p["setup_status"] = setup_summary(p)["status"]
        putj(data_dir(root) / "project.json", p)
        event(root, "setup_updated", f"Campo {field}: {old.get('status')} -> {new_status}")
    return setup_status(root)

def list_goals(root):
    base=data_dir(root)/"goals"
    if not base.exists():return []
    out=[]
    for d in sorted(base.iterdir()):
        if d.is_dir() and GOAL_RE.fullmatch(d.name) and (d/"state.json").exists():
            s=readj(d/"state.json")
            out.append(dict(id=d.name,title=s["title"],status=s["status"],next_action=s.get("next_action")))
    return out

def goal_create(root,title,objective,criteria,depends=None):
    if not criteria: raise KEError("Forneça ao menos um critério --accept")
    if not title.strip() or not objective.strip(): raise KEError("Título/objetivo ausente")
    depends=depends or []
    with locked(root):
        old=list_goals(root)
        ids={g["id"] for g in old}
        for dep in depends:
            if dep not in ids: raise KEError(f"Dependência inexistente: {dep}")
        gid=f"META-{(max([int(x[5:]) for x in ids], default=0)+1):03}"
        p=data_dir(root)/"goals"/gid
        p.mkdir(parents=True,exist_ok=False)
        plan="# "+gid+" — "+sanitize(title)+"\n\n## Objetivo\n\n"+sanitize(objective)+"\n\n## Plano v001\n\n1. Validar pré-requisitos.\n2. Executar ações autorizadas.\n3. Conferir critérios de aceite e evidências.\n"
        (p/"plan-v001.md").write_text(plan,encoding="utf-8")
        putj(p/"acceptance.json",dict(criteria=[dict(id=i+1,text=sanitize(c),status="pending",evidence=None) for i,c in enumerate(criteria)]),once=True)
        putj(p/"state.json",dict(schema_version=2,id=gid,title=sanitize(title),status="planned",revision=1,plan_version=1,
                                 dependencies=depends,objective=sanitize(objective),next_action="Preparar e aprovar execução",
                                 snapshot_id=None,updated_at=now()),once=True)
        state=readj(data_dir(root)/"state.json")
        if not state.get("active_goal_id"):
            state.update(active_goal_id=gid,next_action=f"Planejar {gid}",revision=state["revision"]+1,updated_at=now())
        putj(data_dir(root)/"state.json",state)
        event(root,"goal_created",f"Criada {gid}",goal=gid)
    return dict(goal_id=gid,status="planned")

def goal_status(root,goal=None):
    if goal:
        p=gp(root,goal)
        return dict(state=readj(p/"state.json"),acceptance=readj(p/"acceptance.json"))
    return list_goals(root)

def goal_record(root,goal,summary):
    if not summary.strip(): raise KEError("Resumo vazio")
    p=gp(root,goal)
    with locked(root):
        g=readj(p/"state.json")
        if g["status"] in ("completed","cancelled"): raise KEError("Meta fechada; não reescrever histórico")
        g.update(status="in_progress",next_action="Validar execução e registrar evidências",revision=g["revision"]+1,updated_at=now())
        putj(p/"state.json",g)
        ev=event(root,"goal_action",summary,goal=goal)
    return dict(goal=goal,event=ev.name,status="in_progress")

def goal_accept(root,goal,criterion,evidence):
    p=gp(root,goal)
    source=ensure_safe_relative(root,Path(evidence))
    if source.is_relative_to(data_dir(root)/"snapshots"):raise KEError("Evidência de snapshots anteriores não pode ser reaproveitada automaticamente")
    raw=source.read_bytes()
    if SAFE_TOKEN_RE.search(raw.decode("utf-8",errors="ignore")):
        raise KEError("Possível segredo detectado na evidência; saneie antes")
    with locked(root):
        acc=readj(p/"acceptance.json")
        entries=acc["criteria"]
        if not (1<=criterion<=len(entries)):raise KEError("Critério inexistente")
        g=readj(p/"state.json")
        if g["status"] in ("completed","cancelled","deferred"): raise KEError("Reabra a meta antes de anexar evidência")
        evpath=p/"artifacts"/f"accept-{criterion}-{uid()}{source.suffix}"
        write_bytes_once(evpath,raw)
        entries[criterion-1]["status"]="evidence_attached"
        entries[criterion-1].pop("observation",None)
        entries[criterion-1]["test_executed"]=False
        entries[criterion-1]["evidence"]=evpath.relative_to(root).as_posix()
        entries[criterion-1]["hash"]=sha(evpath)
        putj(p/"acceptance.json",acc)
        if all(e["status"] in ("observed_pass","human_approved") for e in entries):
            g["status"]="ready_for_acceptance"
        g["revision"]+=1;g["updated_at"]=now()
        putj(p/"state.json",g)
        event(root,"criterion_attached",f"Critério {criterion} ligado à evidência",goal=goal)
    return dict(goal=goal,criterion=criterion,status="evidence_attached")

def make_snapshot(root,goal):
    p=gp(root,goal)
    gs=readj(p/"state.json")
    acc=readj(p/"acceptance.json")
    if not acc["criteria"] or any(c["status"] not in ("observed_pass","human_approved") for c in acc["criteria"]):
        raise KEError("Critérios não verificados; fechamento bloqueado")
    if gs["status"] not in ("ready_for_acceptance","in_progress"):
        raise KEError("Meta não está pronta para aceite")
    snaps=data_dir(root)/"snapshots"
    sid=f"{goal}-{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uid()}"
    tmp=snaps/f".pending-{sid}"
    final=snaps/sid
    tmp.mkdir(parents=True)
    wanted=[data_dir(root)/"project.json",data_dir(root)/"state.json",
            p/"state.json",p/"acceptance.json",p/f"plan-v{gs['plan_version']:03}.md"]
    for c in acc["criteria"]:
        f=ensure_safe_relative(root,Path(c["evidence"]))
        if sha(f)!=c["hash"]:raise KEError("Evidência foi alterada depois do aceite")
        wanted.append(f)
    wanted.extend(x for x in (p/"steps").glob("*.json"))
    wanted.extend(x for x in (data_dir(root)/"decisions.jsonl",p/"handoff.md") if x.is_file())
    items=[]
    for f in wanted:
        rel=f.relative_to(root)
        dest=tmp/"state"/rel
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(f,dest)
        items.append(dict(path=str(Path("state")/rel).replace("\\","/"),sha256=sha(dest)))
    manifest=dict(version=1,project_id=readj(data_dir(root)/"project.json")["project_id"],
                  goal_id=goal,snapshot_id=sid,created_at=now(),capture_phase="before_close",
                  documents=items,backup_restorable=False)
    putj(tmp/"manifest.json",manifest,once=True)
    snaps.mkdir(exist_ok=True)
    tmp.rename(final)
    return sid

def snapshot_verify(root, goal=None):
    """Valida conteúdo, vínculos e conjunto mínimo de documentos da captura.

    Hashes detectam corrupção acidental, não fornecem autenticidade criptográfica
    contra um adversário que também consiga editar o manifesto.
    """
    base = data_dir(root) / "snapshots"
    if not base.exists():
        raise KEError("Nenhum snapshot")
    folders = [d for d in base.iterdir()
               if d.is_dir() and not d.name.startswith(".pending-")]
    if goal:
        folders = [d for d in folders if d.name.startswith(goal + "-")]
    if not folders:
        raise KEError("Nenhum snapshot correspondente")
    project_id = readj(data_dir(root) / "project.json")["project_id"]
    results = []
    for directory in sorted(folders):
        reasons = []
        try:
            manifest = readj(directory / "manifest.json")
            sid = manifest.get("snapshot_id")
            gid = manifest.get("goal_id")
            docs = manifest.get("documents")
            if sid != directory.name:
                reasons.append("ID do snapshot não corresponde ao diretório")
            if manifest.get("project_id") != project_id:
                reasons.append("Snapshot pertence a outro projeto")
            if not isinstance(gid, str) or not GOAL_RE.fullmatch(gid) or not sid.startswith(gid + "-"):
                reasons.append("Identificação da meta inválida")
            if goal and gid != goal:
                reasons.append("Meta divergente da consulta")
            if manifest.get("capture_phase") != "before_close":
                reasons.append("Fase de captura inválida")
            if not isinstance(docs, list) or not docs:
                reasons.append("Manifesto sem documentos")
                docs = []
            paths = set()
            for entry in docs:
                rel = entry.get("path") if isinstance(entry, dict) else None
                digest = entry.get("sha256") if isinstance(entry, dict) else None
                if not isinstance(rel, str) or not rel.startswith("state/") or rel in paths:
                    reasons.append("Caminho ausente, duplicado ou inválido no manifesto")
                    continue
                paths.add(rel)
                candidate = directory / rel
                if (not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest)
                    or not candidate.resolve().is_relative_to(directory.resolve())
                    or not candidate.is_file() or sha(candidate) != digest):
                    reasons.append(f"Arquivo ausente ou checksum divergente: {rel}")
            if isinstance(gid, str) and GOAL_RE.fullmatch(gid):
                prefix = f"state/.kommo-engineer/goals/{gid}/"
                required = {
                    "state/.kommo-engineer/project.json",
                    "state/.kommo-engineer/state.json",
                    prefix + "state.json",
                    prefix + "acceptance.json",
                }
                goal_state_file = directory / (prefix + "state.json")
                acceptance_file = directory / (prefix + "acceptance.json")
                if goal_state_file.is_file() and acceptance_file.is_file():
                    captured_goal = readj(goal_state_file)
                    captured_acc = readj(acceptance_file)
                    plan_version = captured_goal.get("plan_version")
                    if not isinstance(plan_version, int) or plan_version < 1:
                        reasons.append("Versão do plano capturado inválida")
                    else:
                        required.add(prefix + f"plan-v{plan_version:03}.md")
                    criteria = captured_acc.get("criteria")
                    if not isinstance(criteria, list) or not criteria:
                        reasons.append("Critérios capturados ausentes")
                    else:
                        for c in criteria:
                            rel_evidence = c.get("evidence") if isinstance(c, dict) else None
                            if c.get("status") not in ("verified","observed_pass","human_approved") or not rel_evidence:
                                reasons.append("Aceite sem evidência confirmada na captura")
                            elif Path(rel_evidence).is_absolute() or ".." in Path(rel_evidence).parts:
                                reasons.append("Caminho de evidência inválido")
                            else:
                                required.add("state/" + rel_evidence.replace("\\", "/"))
                    if captured_goal.get("id") != gid:
                        reasons.append("ID da meta capturada divergente")
                if not required.issubset(paths):
                    reasons.append("Documentos obrigatórios ausentes do manifesto")
                try:
                    current_goal = readj(gp(root, gid) / "state.json")
                    # Historic snapshots remain valid after a formal reopening.
                    # project_validate checks the currently selected snapshot separately.
                except (KEError, OSError, KeyError):
                    reasons.append("Meta do snapshot não encontrada ou inválida")
        except (KEError, OSError, ValueError, KeyError, TypeError, AttributeError) as e:
            reasons.append(f"Manifesto inválido: {e}")
            docs = []
        results.append(dict(snapshot=directory.name, valid=not reasons,
                            documents=len(docs), errors=reasons))
    return dict(all_valid=all(x["valid"] for x in results), snapshots=results)

def goal_close(root,goal):
    p=gp(root,goal)
    with locked(root):
        sid=None
        from ke_extended import dependencies
        if dependencies(sys.modules[__name__],root,goal)["blocked"]:raise KEError("Dependências não satisfeitas")
        acc=readj(p/"acceptance.json")
        if any(c["status"] not in ("observed_pass","human_approved") for c in acc["criteria"]):raise KEError("Registre teste e resultado observado antes de fechar")
        # Marker permits diagnosing partial multi-file completion.
        marker=begin_pending(root,"goal_close",goal=goal)
        try:
            sid=make_snapshot(root,goal)
            g=readj(p/"state.json")
            g.update(status="completed",snapshot_id=sid,next_action="Revisar o resultado e planejar a próxima meta",
                     revision=g["revision"]+1,updated_at=now())
            putj(p/"state.json",g)
            state=readj(data_dir(root)/"state.json")
            state.update(active_goal_id=None if state.get("active_goal_id")==goal else state.get("active_goal_id"),last_goal_id=goal,
                         next_action="Revisar o resultado e planejar a próxima meta",
                         revision=state["revision"]+1,updated_at=now())
            putj(data_dir(root)/"state.json",state)
            event(root,"goal_completed",f"Meta {goal} concluída, snapshot={sid}",goal=goal)
            v=snapshot_verify(root,goal)
            if not v["all_valid"]:raise KEError("Snapshot não verificou")
            marker.unlink()
        except Exception:
            # Recovery marker remains intentionally to prohibit silent continuation.
            raise
    return dict(goal=goal,status="completed",snapshot_id=sid,snapshot_verified=True)

def goal_resume(root,goal):
    s=goal_status(root,goal)
    g=s["state"]
    resume=(f"# Retomada {goal}\n\nProjeto: {readj(data_dir(root)/'project.json')['name']}\n"
            f"Estado: {g['status']}\nPlano: plan-v{g['plan_version']:03}.md\n"
            f"Próxima ação: {g['next_action']}\n"
            f"Snapshot: {g['snapshot_id'] or 'nenhum'}\n"
            "Leia AGENTS.md e o estado desta meta; não revise todas as metas.\n")
    return resume

def project_validate(root):
    d=data_dir(root)
    errs=[]
    try:
        from schema_runtime import validate as schema_validate
        for name in ("project","state"):
            schema_validate(readj(d/(name+".json")),readj(SKILL/"schemas"/(name+".schema.json")))
        for gfile in (d/"goals").glob("META-*/state.json"):
            schema_validate(readj(gfile),readj(SKILL/"schemas/goal.schema.json"))
        p=readj(d/"project.json")
        s=readj(d/"state.json")
        if p["project_id"]!=s["project_id"]:errs.append("project_id divergente")
        contract = setup_contract()["fields"]
        answers = p.get("answers")
        if not isinstance(answers, dict):
            errs.append("Respostas do setup ausentes ou inválidas")
        else:
            for field, meta in contract.items():
                answer = answers.get(field)
                if not isinstance(answer, dict):
                    errs.append(f"Campo de setup ausente: {field}")
                    continue
                stt = answer.get("status")
                if stt not in ("pending", "proposed", "confirmed", "deferred", "not_applicable"):
                    errs.append(f"Status inválido em {field}")
                if stt == "not_applicable" and meta["required"]:
                    errs.append(f"Campo obrigatório marcado inaplicável: {field}")
                if stt == "confirmed" and (
                        not isinstance(answer.get("value"), str) or
                        not answer["value"].strip() or
                        not answer.get("confirmed_at")):
                    errs.append(f"Confirmação inválida em {field}")
                if stt in ("deferred", "not_applicable") and not answer.get("notes"):
                    errs.append(f"Justificativa ausente em {field}")
            computed = setup_summary(p)["status"]
            if p.get("setup_status") != computed:
                if not (p.get("setup_status") == "in_progress" and computed == "ready_for_planning"):
                    errs.append(f"Status de setup inconsistente: registrado={p.get('setup_status')}, esperado={computed}")
                # Projetos v0.3 podiam estar prontos para planejar ainda com in_progress.
        if not (root/"AGENTS.md").exists():errs.append("AGENTS.md ausente")
        for g in list_goals(root):
            gp1=gp(root,g["id"])
            st=readj(gp1/"state.json")
            if not (gp1/f"plan-v{st['plan_version']:03}.md").exists():errs.append(f"Plano ausente: {g['id']}")
            if st["status"]=="completed":
                if not st["snapshot_id"]: errs.append(f"Snapshot ausente: {g['id']}")
                else:
                    snap=d/"snapshots"/st["snapshot_id"]
                    if not snap.exists():
                        errs.append(f"Snapshot não encontrado: {g['id']}")
                    else:
                        verified = snapshot_verify(root, g["id"])
                        match = [x for x in verified["snapshots"] if x["snapshot"] == st["snapshot_id"]]
                        if len(match) != 1 or not match[0]["valid"]:
                            errs.append(f"Snapshot vinculado inválido: {g['id']}")
        if (d/".runtime"/"pending-operation.json").exists():errs.append("Operação interrompida: requer inspeção")
    except Exception as e:
        errs.append(str(e))
    return dict(valid=not errs,errors=errs,goals=len(list_goals(root)) if (d/"goals").exists() else 0)

def knowledge_find(query):
    from knowledge import find
    return find(query)


def report_build(root):
    from deliveries import build
    return build(sys.modules[__name__],root)


def smoke_prepare(root):
    proj=create_project(root,"Aurora Fictícia — Teste","Consultoria fictícia","Validar persistência",simulation=True)
    for field,value in (("role","Analista fictício"),("product","Serviço fictício"),
                        ("acceptance","Evidência local simulada"),("restrictions","Sem rede"),
                        ("skill_level","Iniciante"),("sales_process","Triagem fictícia")):
        setup_update(root,field,value)
    res=goal_create(root,"Meta de demonstração","Provar persistência local",
                    ["Artefato sintético gerado e verificado"])
    goal=res["goal_id"]
    goal_record(root,goal,"Execução sintética; nenhum contato Kommo")
    artifact=data_dir(root)/"fixtures"/"synthetic.json"
    putj(artifact,dict(simulation=True,remote_changes=False,goal=goal),once=True)
    goal_accept(root,goal,1,str(artifact))
    from ke_extended import observe
    observe(sys.modules[__name__],root,goal,1,"Leitura e hash do artefato sintético","Artefato presente e coerente com a fixture", "offline")
    closed=goal_close(root,goal)
    marker=uid()
    putj(data_dir(root)/"smoke-marker.json",dict(marker=marker,project_id=proj["project_id"],goal=goal),once=True)
    return dict(project_id=proj["project_id"],marker=marker,**closed)

def smoke_verify(root):
    if readj(data_dir(root)/"project.json")["environment"]!="simulation":
        raise KEError("Smoke verify aceita somente projetos sintéticos")
    marker=readj(data_dir(root)/"smoke-marker.json")
    state=readj(data_dir(root)/"state.json")
    v=snapshot_verify(root,marker["goal"])
    errors=project_validate(root)["errors"]
    g=readj(gp(root,marker["goal"])/"state.json")
    ok=(not errors and v["all_valid"] and g["status"]=="completed" and
        state["last_goal_id"]==marker["goal"] and state["active_goal_id"] is None and
        bool(marker["marker"]) and g["snapshot_id"])
    return dict(valid=bool(ok),marker=marker["marker"],goal=marker["goal"],snapshot=g["snapshot_id"],errors=errors)

def main(argv=None):
    ap=argparse.ArgumentParser(description="Kommo Engineer CLI local — sem acesso remoto")
    ap.add_argument("--version",action="version",version=VERSION)
    sub=ap.add_subparsers(dest="command",required=True)
    sub.add_parser("doctor")
    proj=sub.add_parser("project"); psub=proj.add_subparsers(dest="action",required=True)
    for action in ("init","status","validate","resume"):
        s=psub.add_parser(action);s.add_argument("--project",required=True)
        if action=="init":
            for arg in ("name","business","goal"):s.add_argument("--"+arg,required=True)
            s.add_argument("--use-existing-dir",action="store_true")
    setup=sub.add_parser("setup");ssub=setup.add_subparsers(dest="action",required=True)
    for action in ("status","update"):
        s=ssub.add_parser(action);s.add_argument("--project",required=True)
        if action=="update":
            s.add_argument("--field",required=True)
            group = s.add_mutually_exclusive_group(required=True)
            group.add_argument("--value")
            group.add_argument("--defer",action="store_true")
            group.add_argument("--not-applicable",action="store_true")
            s.add_argument("--proposed",action="store_true")
            s.add_argument("--reason")
    goals=sub.add_parser("goal");gsub=goals.add_subparsers(dest="action",required=True)
    for action in ("create","status","record","accept","close","resume"):
        s=gsub.add_parser(action);s.add_argument("--project",required=True)
        if action=="create":
            s.add_argument("--title",required=True);s.add_argument("--objective",required=True)
            s.add_argument("--accept",action="append",required=True);s.add_argument("--depends",action="append")
        elif action in ("record","accept","close","resume"):s.add_argument("--goal",required=True)
        if action=="record":s.add_argument("--summary",required=True)
        if action=="accept":
            s.add_argument("--criterion",type=int,required=True);s.add_argument("--evidence",required=True)
        if action=="status":s.add_argument("--goal")
    snapshot=sub.add_parser("snapshot");ss=snapshot.add_subparsers(dest="action",required=True)
    s=ss.add_parser("verify");s.add_argument("--project",required=True);s.add_argument("--goal")
    knowledge=sub.add_parser("knowledge"); ks=knowledge.add_subparsers(dest="action",required=True)
    k=ks.add_parser("find");k.add_argument("--query",required=True)
    reports=sub.add_parser("report");rs=reports.add_subparsers(dest="action",required=True)
    r=rs.add_parser("build");r.add_argument("--project",required=True)
    sm=sub.add_parser("smoke");ms=sm.add_subparsers(dest="action",required=True)
    for action in ("prepare","verify"):
        s=ms.add_parser(action);s.add_argument("--project",required=True);s.add_argument("--offline",action="store_true",required=True)
    import ke_extended
    ke_extended.configure(sub,psub,ssub,gsub,ks,rs)
    args=ap.parse_args(argv)
    try:
        if ke_extended.handles(args):result=ke_extended.run(args,sys.modules[__name__])
        elif args.command=="doctor":
            result=dict(version=VERSION,python=sys.version.split()[0],compatible=sys.version_info>=(3,11),
                        skill=str(SKILL),local_only=True)
        elif args.command=="knowledge":result=knowledge_find(args.query)
        else:
            root=getroot(args.project,
                         new=(args.command=="project" and args.action=="init" and not args.use_existing_dir) or
                             (args.command=="smoke" and args.action=="prepare"),
                         init_existing=(args.command=="project" and args.action=="init" and args.use_existing_dir))
            if args.command=="project":
                if args.action=="init":result=create_project(root,args.name,args.business,args.goal,use_existing=args.use_existing_dir)
                elif args.action=="status":result=project_status(root)
                elif args.action=="resume":result=project_resume(root)
                else:result=project_validate(root)
            elif args.command=="setup":
                result=setup_status(root) if args.action=="status" else setup_update(root,args.field,args.value,args.proposed,args.defer,args.not_applicable,args.reason)
            elif args.command=="goal":
                if args.action=="create":result=goal_create(root,args.title,args.objective,args.accept,args.depends)
                elif args.action=="status":result=goal_status(root,args.goal)
                elif args.action=="record":result=goal_record(root,args.goal,args.summary)
                elif args.action=="accept":result=goal_accept(root,args.goal,args.criterion,args.evidence)
                elif args.action=="close":result=goal_close(root,args.goal)
                else:result=goal_resume(root,args.goal)
            elif args.command=="snapshot":result=snapshot_verify(root,args.goal)
            elif args.command=="report":result=report_build(root)
            elif args.command=="smoke":
                if not args.offline:raise KEError("Smoke exige --offline")
                result=smoke_prepare(root) if args.action=="prepare" else smoke_verify(root)
        if isinstance(result,str):print(result)
        else:print(json.dumps(result,ensure_ascii=False,indent=2))
        if isinstance(result,dict) and (result.get("valid") is False or result.get("all_valid") is False):
            return 1
        return 0
    except (KEError,OSError,ValueError,KeyError,IndexError) as e:
        print(json.dumps(dict(error=sanitize(str(e))),ensure_ascii=False),file=sys.stderr)
        return 2

if __name__=="__main__":sys.exit(main())
