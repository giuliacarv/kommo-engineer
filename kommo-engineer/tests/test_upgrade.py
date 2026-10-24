import ast
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import ke
import ke_extended as ext
from test_cli import call

class Upgrade(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name).resolve()/'Cliente á'
        ke.create_project(self.root,'Fixture','Serviço','Melhorar triagem')
        self.gid=ke.goal_create(self.root,'Primeira','Fixture',['Artefato local coerente'])['goal_id']
    def tearDown(self):self.tmp.cleanup()
    def cmd(self,*args):return call(*args,'--project',self.root)
    def file(self,name,obj):
        p=self.root/name;p.write_text(json.dumps(obj,ensure_ascii=False),encoding='utf-8');return p
    def observed(self):
        p=self.file('evidence.json',{'synthetic':True});ke.goal_accept(self.root,self.gid,1,str(p))
        ext.observe(ke,self.root,self.gid,1,'Fixture JSON','Valor synthetic=true','offline')
    def test_no_cursor_hijack(self):
        ke.goal_create(self.root,'Outra','Escopo independente',['Outro'])
        self.assertEqual(ke.readj(ke.data_dir(self.root)/'state.json')['active_goal_id'],self.gid)
    def test_attachment_is_not_pass(self):
        p=self.file('evidence.json',{'synthetic':True});out=ke.goal_accept(self.root,self.gid,1,str(p))
        self.assertEqual(out['status'],'evidence_attached')
        with self.assertRaises(ke.KEError):ke.goal_close(self.root,self.gid)
        self.assertFalse((ke.data_dir(self.root)/'.runtime/pending-operation.json').exists())
    def test_reopen_keeps_snapshot(self):
        self.observed();first=ke.goal_close(self.root,self.gid)
        code,_,err=self.cmd('goal','reopen','--goal',self.gid,'--reason','Novo escopo');self.assertEqual(code,0,err)
        self.observed();second=ke.goal_close(self.root,self.gid)
        self.assertNotEqual(first['snapshot_id'],second['snapshot_id'])
        self.assertTrue(ke.snapshot_verify(self.root,self.gid)['all_valid'])
    def test_three_goals_decisions_and_handoff(self):
        second=ke.goal_create(self.root,'Adiada','Esperar',['Critério'])['goal_id']
        third=ke.goal_create(self.root,'Descartada','Não executar',['Critério'])['goal_id']
        for action,gid in [('defer',second),('cancel',third)]:
            code,_,err=self.cmd('goal',action,'--goal',gid,'--reason','Decisão humana');self.assertEqual(code,0,err)
        code,record,err=self.cmd('goal','decision','add','--goal',third,'--summary','Descartar','--reason','Sem demanda','--impact','Não vira pendência','--disposition','rejected');self.assertEqual(code,0,err)
        before=(ke.data_dir(self.root)/'decisions.jsonl').read_bytes()
        self.observed();ke.goal_close(self.root,self.gid)
        code,result,err=self.cmd('goal','handoff','--goal',second);self.assertEqual(code,0,err)
        self.assertIn(str(self.root),result['prompt']);self.assertIn('deferred',result['prompt'])
        self.assertEqual(before,(ke.data_dir(self.root)/'decisions.jsonl').read_bytes())
        self.assertEqual([g['status'] for g in ke.list_goals(self.root)],['completed','deferred','cancelled'])
    def test_plan_revision_conflict(self):
        p=self.root/'new-plan.md';p.write_text('# Novo plano\nEscopo novo',encoding='utf-8')
        original=(ke.gp(self.root,self.gid)/'plan-v001.md').read_bytes()
        args=('goal','plan','revise','--goal',self.gid,'--file',p,'--reason','Mudança','--expected-version','1')
        self.assertEqual(self.cmd(*args)[0],0);self.assertNotEqual(self.cmd(*args)[0],0)
        self.assertEqual(original,(ke.gp(self.root,self.gid)/'plan-v001.md').read_bytes())
    def test_step_revision(self):
        obj=dict(objective='Testar',inputs=[],prerequisites=[],actions=['ler'],exceptions=[],status='planned',evidence=[],logs=[],next_action='Conferir')
        f=self.file('step.json',obj)
        code,step,err=self.cmd('goal','step','add','--goal',self.gid,'--file',f);self.assertEqual(code,0,err)
        self.assertEqual(step['id'],self.gid+'/E00')
        self.assertNotEqual(self.cmd('goal','step','update','--goal',self.gid,'--step','E00','--file',f,'--expected-revision','99')[0],0)
    def test_dependencies_waiver_and_cycle(self):
        other=ke.goal_create(self.root,'Outra','Contrato',['X'])['goal_id']
        f=self.file('deps.json',[dict(goal_id=other,resolution='waived',reason='Contrato dispensado')])
        code,out,err=self.cmd('goal','dependencies','--goal',self.gid,'--file',f);self.assertEqual(code,0,err);self.assertFalse(out['blocked'])
        f=self.file('cycle.json',[self.gid]);self.assertNotEqual(self.cmd('goal','dependencies','--goal',other,'--file',f)[0],0)
    def test_migration_preserves_files(self):
        p=ke.data_dir(self.root)/'project.json';legacy=ke.readj(p);legacy['schema_version']=1;ke.putj(p,legacy)
        original=(ke.data_dir(self.root)/'project.json').read_bytes()
        code,out,err=self.cmd('project','migrate');self.assertEqual(code,0,err)
        self.assertEqual(original,(Path(out['backup'])/'project.json').read_bytes())
        self.assertEqual(ke.readj(ke.data_dir(self.root)/'project.json')['schema_version'],2)
        self.assertFalse(self.cmd('project','migrate')[1]['migrated'])
    def test_reports_are_immutable(self):
        a=ke.report_build(self.root);b=ke.report_build(self.root)
        self.assertNotEqual(a['release'],b['release']);self.assertTrue(Path(a['files'][0]).exists())
    def test_runtime_rejects_invalid_revision(self):
        p=ke.data_dir(self.root)/'state.json';s=ke.readj(p);s['revision']='corrupt';ke.putj(p,s)
        self.assertFalse(ke.project_validate(self.root)['valid'])
    def test_python311_grammar(self):
        for p in (ROOT/'scripts').rglob('*.py'):ast.parse(p.read_text(encoding='utf-8'),feature_version=(3,11))
    def test_visual_retrieval_has_images_and_gaps(self):
        from knowledge import find,validate
        a=find('configurar Condição > Definir campo > Contato')[0]
        self.assertEqual(a['id'],'UI-CONDICAO-CAMPO');self.assertTrue(a['screenshots']);self.assertTrue(a['gaps'])
        self.assertEqual(find('qual gatilho escolher?')[0]['id'],'UI-GATILHOS')
        self.assertTrue(validate()['valid'])

if __name__=='__main__':unittest.main()
