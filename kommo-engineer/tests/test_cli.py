import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE=Path(__file__).resolve().parents[1]
CLI=HERE/"scripts"/"ke.py"

def call(*args):
    p=subprocess.run([sys.executable,"-S",str(CLI),*map(str,args)],capture_output=True,text=True)
    # Site-level startup messages from third-party environment are ignored; tests rely on status/stdout.
    output=None
    if p.stdout.strip().startswith(("{","[")):
        output=json.loads(p.stdout)
    return p.returncode,output,p.stderr

class TestKommoEngineer(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)/"Cliente com acentos á"
    def tearDown(self):
        self.tmp.cleanup()
    def init(self):
        code,data,_=call("project","init","--project",self.root,"--name","Loja fictícia",
                         "--business","Loja","--goal","Qualificar leads")
        self.assertEqual(code,0)
        return data
    def goal(self):
        code,data,_=call("goal","create","--project",self.root,
                         "--title","Pipeline A","--objective","Criar pipeline",
                         "--accept","Recurso verificado")
        self.assertEqual(code,0)
        return data["goal_id"]
    def test_doctor(self):
        code,data,_=call("doctor")
        self.assertEqual(code,0)
        self.assertTrue(data["compatible"])
        self.assertTrue(data["local_only"])
    def test_smoke_and_independent_read(self):
        code,data,_=call("smoke","prepare","--project",self.root,"--offline")
        self.assertEqual(code,0)
        self.assertTrue(data["snapshot_verified"])
        code,restored,_=call("smoke","verify","--project",self.root,"--offline")
        self.assertEqual(code,0)
        self.assertEqual(restored["marker"],data["marker"])
        self.assertTrue(restored["valid"])
    def test_smoke_refuses_existing_project(self):
        self.init()
        code,_,_=call("smoke","prepare","--project",self.root,"--offline")
        self.assertNotEqual(code,0)
    def test_smoke_requires_offline(self):
        code,_,_=call("smoke","prepare","--project",self.root)
        self.assertNotEqual(code,0)
    def test_duplicate_init_refused(self):
        self.init()
        code,_,_=call("project","init","--project",self.root,"--name","X","--business","Y","--goal","Z")
        self.assertNotEqual(code,0)
    def test_setup_update_and_status(self):
        self.init()
        for field in ["role","product","sales_process","acceptance","restrictions","skill_level"]:
            code,_,_=call("setup","update","--project",self.root,"--field",field,"--value","Confirmado")
            self.assertEqual(code,0)
        code,data,_=call("setup","status","--project",self.root)
        self.assertEqual(data["status"],"complete")
        self.assertEqual(data["missing"],[])
    def test_setup_proposed_not_confirmed(self):
        self.init()
        code,data,_=call("setup","update","--project",self.root,"--field","role",
                         "--value","Talvez gerente","--proposed")
        self.assertIn("role",data["missing"])
    def test_goal_creation_does_not_remove_previous(self):
        self.init()
        a=self.goal()
        b=self.goal()
        self.assertNotEqual(a,b)
        code,data,_=call("goal","status","--project",self.root)
        self.assertEqual(len(data),2)
    def test_goal_full_lifecycle(self):
        self.init()
        goal=self.goal()
        data=self.root/".kommo-engineer"/"evidence.txt"
        data.write_text("Verificado manualmente em fixture local",encoding="utf-8")
        code,_,_=call("goal","record","--project",self.root,"--goal",goal,"--summary","Verificação local")
        self.assertEqual(code,0)
        code,_,_=call("goal","accept","--project",self.root,"--goal",goal,
                      "--criterion","1","--evidence",data)
        self.assertEqual(code,0)
        code,closed,_=call("goal","close","--project",self.root,"--goal",goal)
        self.assertEqual(code,0)
        self.assertTrue(closed["snapshot_verified"])
        code,out,_=call("snapshot","verify","--project",self.root,"--goal",goal)
        self.assertEqual(code,0)
        self.assertTrue(out["all_valid"])
    def test_close_requires_evidence(self):
        self.init()
        goal=self.goal()
        code,_,_=call("goal","close","--project",self.root,"--goal",goal)
        self.assertNotEqual(code,0)
    def test_evidence_cannot_escape_project(self):
        self.init()
        goal=self.goal()
        foreign=Path(self.tmp.name)/"outside.txt"
        foreign.write_text("Fora",encoding="utf-8")
        code,_,_=call("goal","accept","--project",self.root,"--goal",goal,
                      "--criterion","1","--evidence",foreign)
        self.assertNotEqual(code,0)
    def test_secret_detection(self):
        self.init()
        goal=self.goal()
        data=self.root/"suspect.txt"
        data.write_text("access_token=verySensitiveTestValue",encoding="utf-8")
        code,_,_=call("goal","accept","--project",self.root,"--goal",goal,
                      "--criterion","1","--evidence",data)
        self.assertNotEqual(code,0)
    def test_lock_blocks_writes(self):
        self.init()
        runtime=self.root/".kommo-engineer"/".runtime"
        runtime.mkdir(parents=True,exist_ok=True)
        (runtime/"write.lock").write_text("busy")
        code,_,_=call("setup","update","--project",self.root,"--field","role","--value","X")
        self.assertNotEqual(code,0)
    def test_pending_marker_blocks_writes(self):
        self.init()
        runtime=self.root/".kommo-engineer"/".runtime"
        runtime.mkdir(parents=True,exist_ok=True)
        (runtime/"pending-operation.json").write_text("{}")
        code,_,_=call("setup","update","--project",self.root,"--field","role","--value","X")
        self.assertNotEqual(code,0)
    def test_snapshot_corruption_detected(self):
        code,data,_=call("smoke","prepare","--project",self.root,"--offline")
        self.assertEqual(code,0)
        snap=self.root/".kommo-engineer"/"snapshots"/data["snapshot_id"]
        m=json.loads((snap/"manifest.json").read_text(encoding="utf-8"))
        damaged=snap/m["documents"][0]["path"]
        damaged.write_text("corrompido",encoding="utf-8")
        code,result,_=call("snapshot","verify","--project",self.root)
        self.assertNotEqual(code,0)
        self.assertFalse(result["all_valid"])
    def test_reports_no_fake_results(self):
        self.init()
        code,data,_=call("report","build","--project",self.root)
        self.assertEqual(code,0)
        report=(self.root/".kommo-engineer"/"deliveries"/"relatorio.md").read_text(encoding="utf-8")
        self.assertIn("Nenhuma meta",report)
    def test_knowledge_find(self):
        code,data,_=call("knowledge","find","--query","salesbot")
        self.assertEqual(code,0)
        self.assertTrue(data and data[0]["id"]=="PROC-KOMMO-005")
    def test_skills_structure(self):
        txt=(HERE/"SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(txt.startswith("---\nname: kommo-engineer\n"))
        self.assertIn("description:",txt)
        for match in __import__("re").findall(r"\]\((references/[^)]+)\)",txt):
            self.assertTrue((HERE/match).exists(),match)

if __name__=="__main__":
    unittest.main()
