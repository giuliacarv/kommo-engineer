"""Versioned local workflow extensions. Remote execution lives in kommo_api."""
import argparse
import json
import re
import shutil
from pathlib import Path

MENU=['0. Ajuda','1. Configurar projeto','2. Diagnóstico','3. Planejar implementação','4. Executar tarefa','5. Salesbots/IA','6. API e integrações','7. Metas e continuidade','8. Auditoria','9. Relatórios e treinamento']

def configure(sub,psub,ssub,gsub,ks,rs):
    p=sub.add_parser('menu');p.add_argument('--project');p.add_argument('--intent')
    p=psub.add_parser('migrate');p.add_argument('--project',required=True)
    for action in ('interview','summary','backlog'):
        p=ssub.add_parser(action);p.add_argument('--project',required=True)
    for action in ('select','defer','cancel','reopen','handoff','dependencies','observe'):
        p=gsub.add_parser(action);p.add_argument('--project',required=True);p.add_argument('--goal',required=True)
        if action in ('defer','cancel','reopen'):p.add_argument('--reason',required=True)
        if action=='dependencies':p.add_argument('--file')
        if action=='observe':
            p.add_argument('--criterion',type=int,required=True);p.add_argument('--method',required=True)
            p.add_argument('--result',required=True);p.add_argument('--level',choices=['offline','account','deployed'],required=True)
            p.add_argument('--account-id');p.add_argument('--scope-ref');p.add_argument('--human-approved',action='store_true')
    p=gsub.add_parser('step');sp=p.add_subparsers(dest='step_action',required=True)
    for action in ('add','status','update'):
        q=sp.add_parser(action);q.add_argument('--project',required=True);q.add_argument('--goal',required=True)
        if action!='add':q.add_argument('--step',required=True)
        if action in ('add','update'):
            q.add_argument('--file',required=True)
            if action=='update':q.add_argument('--expected-revision',type=int,required=True)
    p=gsub.add_parser('plan');sp=p.add_subparsers(dest='plan_action',required=True)
    q=sp.add_parser('revise');q.add_argument('--project',required=True);q.add_argument('--goal',required=True);q.add_argument('--file',required=True);q.add_argument('--reason',required=True);q.add_argument('--expected-version',type=int,required=True)
    p=gsub.add_parser('decision');sp=p.add_subparsers(dest='decision_action',required=True)
    q=sp.add_parser('add');q.add_argument('--project',required=True);q.add_argument('--goal',required=True)
    for name in ('summary','reason','impact'):q.add_argument('--'+name,required=True)
    q.add_argument('--disposition',choices=['accepted','rejected','deferred','superseded'],required=True);q.add_argument('--supersedes')
    p=ks.add_parser('check')
    p=rs.add_parser('add');p.add_argument('--project',required=True);p.add_argument('--goal',required=True);p.add_argument('--file',required=True)

def handles(a):
    return (a.command=='menu' or (a.command=='project' and a.action=='migrate') or
            (a.command=='setup' and a.action in ('interview','summary','backlog')) or
            (a.command=='goal' and a.action not in ('create','status','record','accept','close','resume')) or
            (a.command=='knowledge' and a.action=='check') or (a.command=='report' and a.action=='add'))

def dependencies(k,root,gid):
    g=k.readj(k.gp(root,gid)/'state.json');out=[]
    for dep in g['dependencies']:
        ident=dep if isinstance(dep,str) else dep['goal_id']
        d=k.readj(k.gp(root,ident)/'state.json')
        # A cancelled predecessor is not a delivery. A reasoned waiver is explicit.
        resolution=(dep.get('resolution') if isinstance(dep,dict) else None)
        criteria=dep.get('criteria',[]) if isinstance(dep,dict) else []
        acc=k.readj(k.gp(root,ident)/'acceptance.json')['criteria']
        if criteria:
            relevant=[x for x in acc if x['id'] in criteria]
            met=(len(relevant)==len(set(criteria)) and all(x['status'] in ('observed_pass','human_approved') for x in relevant))
        else:met=d['status']=='completed'
        waiver=resolution=='waived' and bool(dep.get('reason')) if isinstance(dep,dict) else False
        out.append(dict(goal_id=ident,status=d['status'],criteria=criteria,satisfied=met or waiver,waived=waiver))
    return dict(goal_id=gid,dependencies=out,blocked=any(not x['satisfied'] for x in out))

def observe(k,root,gid,criterion,method,result,level,account_id=None,scope_ref=None,human=False):
    method=k.ensure_safe_text(method);result=k.ensure_safe_text(result)
    if level!='offline' and (not account_id or not scope_ref):raise k.KEError('Observação remota exige --account-id e --scope-ref da autorização')
    with k.locked(root):
        p=k.gp(root,gid);g=k.readj(p/'state.json');acc=k.readj(p/'acceptance.json')
        if g['status'] in ('completed','cancelled','deferred'):raise k.KEError('Reabra a meta antes de registrar aceite')
        if not 1<=criterion<=len(acc['criteria']):raise k.KEError('Critério inexistente')
        c=acc['criteria'][criterion-1]
        if c.get('status') not in ('evidence_attached','observed_pass','human_approved'):raise k.KEError('Anexe evidência atual antes da observação')
        f=k.ensure_safe_relative(root,Path(c['evidence']))
        if k.sha(f)!=c['hash']:raise k.KEError('Evidência alterada')
        if level!='offline':
            proj=k.readj(k.data_dir(root)/'project.json')
            if str(proj.get('account_id'))!=str(account_id):raise k.KEError('Conta não corresponde ao vínculo confirmado do projeto')
        c.update(status='human_approved' if human else 'observed_pass',test_executed=True,
                 observation=dict(method=method,result=result,level=level,account_id=account_id,scope_ref=scope_ref,at=k.now()),human_approved=human)
        k.putj(p/'acceptance.json',acc)
        g.update(status='ready_for_acceptance' if all(x['status'] in ('observed_pass','human_approved') for x in acc['criteria']) else 'in_progress',revision=g['revision']+1,updated_at=k.now())
        k.putj(p/'state.json',g);k.event(root,'criterion_observed',f'Critério {criterion}: {level}; observação declarada pelo operador',goal=gid)
    return dict(goal_id=gid,criterion=criterion,status=c['status'],level=level,note='Registro do operador; integridade não atesta por si só a verdade semântica do resultado')

def run(a,k):
    if a.command=='knowledge':
        from knowledge import validate
        return validate()
    if a.command=='menu':
        active=None
        if a.project:active=k.project_status(k.getroot(a.project))
        return dict(menu=sorted(MENU),project=active,recommendation='1. Configurar projeto' if not active else 'Retomar meta selecionada ou escolher intenção',intent=a.intent,rule='Pedido claro vai diretamente à referência pertinente; dúvida pontual dispensa setup',decisions=['A — econômico','B — intermediário','C — maior controle','Não sei, apresente alternativas','Adiar','Escolha tecnicamente'])
    root=k.getroot(a.project);d=k.data_dir(root)
    if a.command=='project':
        with k.locked(root):
            p=k.readj(d/'project.json')
            if p.get('schema_version')==2:return dict(migrated=False,version=2)
            backup=d/'migrations'/('v1-'+k.uid());backup.mkdir(parents=True)
            files=[d/'project.json',d/'state.json']+[x for x in (d/'goals').glob('META-*/*.json')] if (d/'goals').exists() else [d/'project.json',d/'state.json']
            inventory=[]
            for f in files:
                dest=backup/f.relative_to(d);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,dest)
                inventory.append(dict(path=f.relative_to(d).as_posix(),sha256=k.sha(f)))
            k.putj(backup/'manifest.json',dict(files=inventory,rollback='Restaurar somente com escrita suspensa; conservar events e snapshots',at=k.now()),once=True)
            marker=k.begin_pending(root,'migration_v1_to_v2',backup=backup.relative_to(root).as_posix())
            for f in files:
                obj=k.readj(f)
                if f.name=='acceptance.json':
                    for c in obj['criteria']:
                        if c['status']=='verified':c.update(status='legacy_unreviewed',legacy_status='verified')
                else:obj['schema_version']=2
                k.putj(f,obj)
            k.event(root,'migration','v1 -> v2; snapshot antigo conservado; aceite legado exige revisão')
            marker.unlink()
        return dict(migrated=True,version=2,backup=str(backup))
    if a.command=='setup':
        p=k.readj(d/'project.json');s=k.setup_summary(p)
        if a.action=='interview':
            order=['goal','business','role','skill_level','product','sales_process','acceptance','restrictions']+[x for x in k.setup_contract()['fields'] if x not in ('goal','business','role','skill_level','product','sales_process','acceptance','restrictions')]
            remaining=[x for x in order if p['answers'][x]['status'] not in ('confirmed','not_applicable','deferred')]
            field=remaining[0] if remaining else None
            spec=k.setup_contract()['fields']
            return dict(first_question='O que você quer que mude no resultado da sua empresa após implementar o Kommo?',next_field=field,next_question=spec[field]['question'] if field else None,example=spec[field]['example'] if field else None,summary=s,deferred=[x for x in order if p['answers'][x]['status']=='deferred'],rule='Confirmar propostas explicitamente; adiado permanece adiado e bloqueia somente tarefas dependentes')
        if a.action=='backlog':
            return dict(proposals=[dict(title='Diagnosticar situação e mapear IDs',requires=['account','permissions','tools']),dict(title='Implementar objetivo confirmado',objective=p['answers']['goal']['value'],requires=['acceptance','restrictions']),dict(title='Homologar e treinar equipe',requires=['delivery'])],created_goals=False)
        text='# Resumo derivado do setup\n\nFonte autoritativa: project.json, revisão '+str(p['revision'])+'\n\n'
        text+='\n'.join(f"- {f}: [{v['status']}] {v.get('value') or v.get('notes') or 'pendente'}" for f,v in p['answers'].items())
        with k.locked(root):k.atomic_write(d/'setup-complete.md',(text+'\n').encode('utf-8'))
        return dict(file=str(d/'setup-complete.md'),complete=s['complete'],source_revision=p['revision'])
    if a.command=='report':return delivery_add(k,root,a.goal,a.file)
    gid=a.goal;p=k.gp(root,gid)
    if a.action=='observe':return observe(k,root,gid,a.criterion,a.method,a.result,a.level,a.account_id,a.scope_ref,a.human_approved)
    if a.action=='dependencies':
        if a.file:
            value=k.readj(k.ensure_safe_relative(root,Path(a.file)))
            if not isinstance(value,list):raise k.KEError('Dependências devem ser lista')
            k.ensure_safe_text(json.dumps(value,ensure_ascii=False))
            def visit(node,trail):
                if node in trail:raise k.KEError('Ciclo de dependências')
                ds=value if node==gid else k.readj(k.gp(root,node)/'state.json')['dependencies']
                for dep in ds:
                    ident=dep if isinstance(dep,str) else dep['goal_id'];k.gp(root,ident)
                    if isinstance(dep,dict):
                        if dep.get('resolution') not in (None,'waived'):raise k.KEError('Resolução não suportada')
                        if dep.get('resolution')=='waived' and not dep.get('reason'):raise k.KEError('Dispensa exige motivo')
                        if not isinstance(dep.get('criteria',[]),list):raise k.KEError('Critérios devem ser lista')
                    visit(ident,trail+[node])
            with k.locked(root):
                visit(gid,[]);g=k.readj(p/'state.json');g.update(dependencies=value,revision=g['revision']+1,updated_at=k.now());k.putj(p/'state.json',g);k.event(root,'dependencies_updated',gid,goal=gid)
        return dependencies(k,root,gid)
    if a.action=='step' and a.step_action=='status':return k.readj(step_path(k,p,gid,a.step))
    with k.locked(root):
        g=k.readj(p/'state.json')
        if a.action=='select':
            if g['status'] in ('completed','cancelled','deferred'):raise k.KEError('Selecione uma meta aberta ou reabra formalmente')
            st=k.readj(d/'state.json');st.update(active_goal_id=gid,next_action=g['next_action'],revision=st['revision']+1,updated_at=k.now());k.putj(d/'state.json',st)
        elif a.action in ('defer','cancel','reopen'):
            reason=k.ensure_safe_text(a.reason)
            if a.action=='reopen':
                if g['status'] not in ('completed','cancelled','deferred'):raise k.KEError('Meta já aberta')
                g.setdefault('historic_snapshot_ids',[])
                if g.get('snapshot_id'):g['historic_snapshot_ids'].append(g['snapshot_id'])
                g['snapshot_id']=None
                acc=k.readj(p/'acceptance.json')
                for c in acc['criteria']:
                    if c['status']!='pending':c['prior_acceptance']=dict(c);c.update(status='pending',evidence=None)
                k.putj(p/'acceptance.json',acc);g['status']='planned'
            else:g['status']='deferred' if a.action=='defer' else 'cancelled'
            g.update(status_reason=reason,next_action='Revisar escopo e critérios' if a.action=='reopen' else reason)
            st=k.readj(d/'state.json')
            if st.get('active_goal_id')==gid and a.action!='reopen':
                st.update(active_goal_id=None,revision=st['revision']+1,updated_at=k.now());k.putj(d/'state.json',st)
        elif a.action=='plan':
            if g['status'] in ('completed','cancelled'):raise k.KEError('Reabra antes de revisar plano')
            if g['plan_version']!=a.expected_version:raise k.KEError('Conflito de versão do plano')
            content=k.ensure_safe_relative(root,Path(a.file)).read_text(encoding='utf-8');k.ensure_safe_text(content)
            version=g['plan_version']+1
            marker=k.begin_pending(root,'plan_revise',goal=gid,from_version=g['plan_version'],to_version=version)
            k.write_bytes_once(p/f'plan-v{version:03}.md',content.encode('utf-8'));g.update(plan_version=version,plan_revision_reason=k.ensure_safe_text(a.reason))
            g.update(revision=g['revision']+1,updated_at=k.now());k.putj(p/'state.json',g);k.event(root,'plan_revised',g['plan_revision_reason'],goal=gid);marker.unlink()
            return g
        elif a.action=='step':
            if g['status'] in ('completed','cancelled','deferred'):raise k.KEError('Etapa exige meta aberta')
            value=k.readj(k.ensure_safe_relative(root,Path(a.file)))
            required={'objective','inputs','prerequisites','actions','exceptions','status','evidence','logs','next_action'}
            if not required.issubset(value):raise k.KEError('Contrato de etapa incompleto: '+','.join(sorted(required-set(value))))
            if value['status'] not in ('planned','in_progress','blocked','done','deferred','cancelled'):raise k.KEError('Status de etapa inválido')
            k.ensure_safe_text(json.dumps(value,ensure_ascii=False))
            for name in ('inputs','prerequisites','actions','exceptions','evidence','logs'):
                if not isinstance(value[name],list):raise k.KEError(name+' deve ser lista')
            if value['status']=='done' and not value['evidence']:raise k.KEError('Etapa done exige referência de evidência')
            for ref in value['evidence']:k.ensure_safe_relative(root,Path(ref))
            if a.step_action=='add':
                existing=list((p/'steps').glob('E*.json'));num=max([int(x.stem[1:]) for x in existing],default=-1)+1
                sid=f'E{num:02}';dest=p/'steps'/f'{sid}.json';rev=1
            else:
                dest=step_path(k,p,gid,a.step);old=k.readj(dest)
                if old['revision']!=a.expected_revision:raise k.KEError('Conflito de revisão da etapa')
                sid=dest.stem;rev=old['revision']+1
            value.update(id=gid+'/'+sid,revision=rev,updated_at=k.now());k.putj(dest,value,once=a.step_action=='add')
            k.event(root,'step_'+a.step_action,value['id'],goal=gid);return value
        elif a.action=='decision':
            record=dict(id='DEC-'+k.uid(),goal_id=gid,disposition=a.disposition,summary=k.ensure_safe_text(a.summary),reason=k.ensure_safe_text(a.reason),impact=k.ensure_safe_text(a.impact),supersedes=a.supersedes,at=k.now())
            log=d/'decisions.jsonl';old=[json.loads(s) for s in log.read_text(encoding='utf-8').splitlines()] if log.exists() else []
            if a.supersedes and a.supersedes not in {v['id'] for v in old}:raise k.KEError('Decisão anterior inexistente')
            if a.disposition=='superseded' and not a.supersedes:raise k.KEError('Superseded exige --supersedes')
            with log.open('a',encoding='utf-8') as f:f.write(json.dumps(record,ensure_ascii=False)+'\n');f.flush()
            k.event(root,'decision_added',record['id'],goal=gid);return record
        elif a.action=='handoff':
            deps=dependencies(k,root,gid)
            planfile=p/('plan-v%03d.md' % g['plan_version'])
            text=f"Ative a skill kommo-engineer neste ambiente.\nProjeto: {root}.\nMeta exclusiva: {gid}. Estado: {g['status']}.\nLeia {root/'AGENTS.md'}, {d/'state.json'}, {p/'state.json'}, {planfile} e {p/'acceptance.json'}.\nDecisões: {d/'decisions.jsonl'} (somente escopo pertinente).\nDependências materiais: {json.dumps(deps,ensure_ascii=False)}.\nPróximo passo: {g['next_action']}.\nNão reaudite metas inteiras nem reabra decisões descartadas sem novo motivo. Registre evidência e nível de teste; não declare homologação por arquivo existente.\n"
            k.atomic_write(p/'handoff.md',text.encode('utf-8'));return dict(file=str(p/'handoff.md'),prompt=text)
        g.update(revision=g['revision']+1,updated_at=k.now());k.putj(p/'state.json',g);k.event(root,'goal_'+a.action,gid,goal=gid)
    return dict(goal_id=gid,state=g)

def step_path(k,p,gid,step):
    sid=step.removeprefix(gid+'/')
    if not re.fullmatch(r'E\d{2,}',sid):raise k.KEError('ID de etapa inválido')
    return p/'steps'/f'{sid}.json'

def delivery_add(k,root,gid,filename):
    p=k.gp(root,gid);value=k.readj(k.ensure_safe_relative(root,Path(filename)))
    required={'title','before','objective','solution','role','daily_tasks','common_errors','faq','level','evidence'}
    if not required.issubset(value):raise k.KEError('Entrega incompleta: '+','.join(sorted(required-set(value))))
    if value['level'] not in ('documented','offline','account','deployed'):raise k.KEError('Nível de entrega inválido')
    if not isinstance(value['evidence'],list) or not value['evidence']:raise k.KEError('Entrega exige evidência')
    for ref in value['evidence']:k.ensure_safe_relative(root,Path(ref))
    acc=k.readj(p/'acceptance.json')['criteria']
    if value['level'] in ('account','deployed') and not all(c.get('observation',{}).get('level') in ('account','deployed') and c['status'] in ('observed_pass','human_approved') for c in acc):raise k.KEError('Entrega remota exige critérios observados na conta')
    k.ensure_safe_text(json.dumps(value,ensure_ascii=False))
    with k.locked(root):
        dest=k.data_dir(root)/'deliveries'/'records'/('DEL-'+k.uid()+'.json')
        value.update(goal_id=gid,created_at=k.now());k.putj(dest,value,once=True);k.event(root,'delivery_added',dest.name,goal=gid)
    return dict(file=str(dest),level=value['level'])
