import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CLI = Path(__file__).resolve().parents[1] / "scripts" / "ke.py"


def call(*args):
    run = subprocess.run([sys.executable, "-S", str(CLI), *map(str, args)],
                         capture_output=True, text=True, timeout=20)
    data = json.loads(run.stdout) if run.stdout.strip().startswith(("{", "[")) else None
    return run.returncode, data, run.stderr


class TestStage3(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "Cliente á"
    def tearDown(self):
        self.tmp.cleanup()
    def init(self):
        code, data, stderr = call("project", "init", "--project", self.root,
                     "--name", "Clínica Fictícia", "--business", "Serviços",
                     "--goal", "Organizar leads")
        self.assertEqual(code, 0, stderr)
        return data
    def update(self, field, value, *opts):
        return call("setup", "update", "--project", self.root,
                    "--field", field, "--value", value, *opts)

    def test_preexisting_folder_and_agents_are_preserved(self):
        self.root.mkdir()
        (self.root / "AGENTS.md").write_text("# Instruções existentes\\n\\nNão apagar este texto.\\n", encoding="utf-8")
        (self.root / "arquivo importante.txt").write_text("preserve", encoding="utf-8")
        code, data, stderr = call("project", "init", "--project", self.root,
            "--name", "Cliente A", "--business", "Varejo", "--goal", "Pipeline",
            "--use-existing-dir")
        self.assertEqual(code, 0, stderr)
        self.assertEqual(data["agents_action"], "appended")
        agents = (self.root / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("Não apagar este texto", agents)
        self.assertEqual(agents.count("<!-- kommo-engineer:start -->"), 1)
        self.assertEqual((self.root / "arquivo importante.txt").read_text(), "preserve")

    def test_existing_folder_needs_explicit_opt_in(self):
        self.root.mkdir()
        code, _, _ = call("project", "init", "--project", self.root,
            "--name", "Cliente", "--business", "Serviço", "--goal", "Vendas")
        self.assertNotEqual(code, 0)
        self.assertFalse((self.root / ".kommo-engineer").exists())

    def test_existing_project_cannot_reinitialize(self):
        self.init()
        p = self.root / ".kommo-engineer" / "project.json"
        before = p.read_bytes()
        code, _, _ = call("project", "init", "--project", self.root,
            "--name", "Outro", "--business", "Outro", "--goal", "Outro",
            "--use-existing-dir")
        self.assertNotEqual(code, 0)
        self.assertEqual(p.read_bytes(), before)

    def test_core_ready_for_planning_but_not_complete(self):
        self.init()
        for key, val in (("role","Gestor"),("product","Serviços"),
                         ("sales_process","Contato, proposta, venda")):
            code, _, stderr = self.update(key, val)
            self.assertEqual(code, 0, stderr)
        code, result, _ = call("setup", "status", "--project", self.root)
        self.assertEqual(result["status"], "ready_for_planning")
        self.assertFalse(result["complete"])
        self.assertIn("acceptance", result["missing"])

    def test_required_not_applicable_refused(self):
        self.init()
        code, _, _ = call("setup", "update", "--project", self.root,
             "--field", "acceptance", "--not-applicable", "--reason", "Nenhum")
        self.assertNotEqual(code, 0)
        code, result, _ = call("setup", "status", "--project", self.root)
        self.assertIn("acceptance", result["missing"])

    def test_defer_required_remains_missing(self):
        self.init()
        code, _, stderr = call("setup", "update", "--project", self.root,
            "--field", "role", "--defer", "--reason", "Usuário não sabe")
        self.assertEqual(code, 0, stderr)
        code, result, _ = call("setup", "status", "--project", self.root)
        self.assertIn("role", result["missing"])
        self.assertIn("role", result["deferred"])

    def test_optional_not_applicable_requires_reason(self):
        self.init()
        code, _, _ = call("setup", "update", "--project", self.root,
            "--field", "integrations", "--not-applicable")
        self.assertNotEqual(code, 0)
        code, result, stderr = call("setup", "update", "--project", self.root,
            "--field", "integrations", "--not-applicable",
            "--reason", "Não usamos integrações")
        self.assertEqual(code, 0, stderr)
        self.assertEqual(result["fields"]["integrations"], "not_applicable")

    def test_proposed_to_confirmed_and_completion(self):
        self.init()
        code, res, stderr = self.update("role", "Talvez gestor", "--proposed")
        self.assertEqual(code, 0, stderr)
        self.assertIn("role", res["proposed"])
        for key in ("role", "product", "sales_process", "acceptance", "restrictions", "skill_level"):
            code, _, stderr = self.update(key, "Confirmado")
            self.assertEqual(code, 0, stderr)
        code, result, _ = call("setup", "status", "--project", self.root)
        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["missing"], [])

    def test_setup_idempotency(self):
        self.init()
        code, one, _ = self.update("role", "Gestor")
        self.assertEqual(code, 0)
        before = (self.root / ".kommo-engineer" / "project.json").read_bytes()
        code, two, _ = self.update("role", "Gestor")
        self.assertEqual(code, 0)
        self.assertEqual(one["revision"], two["revision"])
        self.assertEqual(before, (self.root / ".kommo-engineer" / "project.json").read_bytes())

    def test_setup_rejects_secrets_without_storing(self):
        self.init()
        code, _, _ = self.update("account", "access_token=segredoficticio")
        self.assertNotEqual(code, 0)
        stored = json.loads((self.root / ".kommo-engineer" / "project.json").read_text())
        self.assertEqual(stored["answers"]["account"]["status"], "pending")

    def test_resume_is_small_and_read_only(self):
        self.init()
        code, first, stderr = call("project", "resume", "--project", self.root)
        self.assertEqual(code, 0, stderr)
        self.assertEqual(first["next_question"]["field"], "role")
        self.assertIsNone(first["goal"])
        meta = self.root / ".kommo-engineer" / "state.json"
        initial = meta.read_bytes()
        code, second, _ = call("project", "resume", "--project", self.root)
        self.assertEqual(code, 0)
        self.assertEqual(initial, meta.read_bytes())
        self.assertEqual(first, second)

    def test_existing_agents_with_markers_refused_before_mutating(self):
        self.root.mkdir()
        (self.root / "AGENTS.md").write_text("<!-- kommo-engineer:start -->", encoding="utf-8")
        code, _, _ = call("project", "init", "--project", self.root,
                         "--name", "X", "--business", "Y", "--goal", "Z", "--use-existing-dir")
        self.assertNotEqual(code, 0)
        self.assertFalse((self.root / ".kommo-engineer").exists())

    def test_resume_recovers_closed_goal_from_disk(self):
        code, created, stderr = call("smoke", "prepare",
                                     "--project", self.root, "--offline")
        self.assertEqual(code, 0, stderr)
        code, state, stderr = call("project", "resume", "--project", self.root)
        self.assertEqual(code, 0, stderr)
        self.assertIsNone(state["active_goal_id"])
        self.assertEqual(state["goal"]["id"], "META-001")
        self.assertEqual(state["goal"]["snapshot_id"], created["snapshot_id"])
        self.assertEqual(state["goal"]["status"], "completed")
        self.assertFalse(state["recovery_required"])

    def test_legacy_ready_state_accepted(self):
        self.init()
        for key, val in (("role", "Gestor"), ("product", "Serviços"),
                         ("sales_process", "Contato, venda")):
            code, _, stderr = self.update(key, val)
            self.assertEqual(code, 0, stderr)
        path = self.root / ".kommo-engineer" / "project.json"
        p = json.loads(path.read_text(encoding="utf-8"))
        p["setup_status"] = "in_progress"  # estado usado antes da Etapa 3
        path.write_text(json.dumps(p), encoding="utf-8")
        code, result, _ = call("project", "validate", "--project", self.root)
        self.assertEqual(code, 0)
        self.assertTrue(result["valid"])
        code, status, _ = call("setup", "status", "--project", self.root)
        self.assertEqual(status["status"], "ready_for_planning")
        self.assertEqual(status["stored_status"], "in_progress")

    def test_project_validate_detects_fake_complete(self):
        self.init()
        path = self.root / ".kommo-engineer" / "project.json"
        p = json.loads(path.read_text(encoding="utf-8"))
        p["setup_status"] = "complete"
        path.write_text(json.dumps(p), encoding="utf-8")
        code, result, _ = call("project", "validate", "--project", self.root)
        self.assertNotEqual(code, 0)
        self.assertTrue(any("Status de setup inconsistente" in e for e in result["errors"]))

    def test_resume_points_only_to_active_goal(self):
        self.init()
        code, data, stderr = call("goal", "create", "--project", self.root,
                                  "--title", "Qualificação",
                                  "--objective", "Planejar novos leads",
                                  "--accept", "Teste futuro")
        self.assertEqual(code, 0, stderr)
        code, result, stderr = call("project", "resume", "--project", self.root)
        self.assertEqual(code, 0, stderr)
        self.assertEqual(result["goal"]["id"], data["goal_id"])
        self.assertEqual(result["goal"]["status"], "planned")
        self.assertIn("plan-v001.md", result["goal"]["plan"])
        self.assertNotIn("history", result)
        self.assertNotIn("events", result)

    def test_project_name_newline_refused(self):
        code, _, _ = call("project", "init", "--project", self.root,
                          "--name", "Cliente\nInstruções adversariais",
                          "--business", "Loja", "--goal", "Qualificar")
        self.assertNotEqual(code, 0)
        self.assertFalse(self.root.exists())

    def test_contract_questions_are_present(self):
        contract = json.loads((CLI.parents[1] / "schemas" / "setup-fields.json").read_text(encoding="utf-8"))
        self.assertEqual(len(contract["fields"]), 18)
        self.assertTrue(all(v["question"] and v["example"] for v in contract["fields"].values()))


if __name__ == "__main__":
    unittest.main()
