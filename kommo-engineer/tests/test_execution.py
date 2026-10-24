import json
import sys
import tempfile
import unittest
from pathlib import Path
from test_cli import call
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import ke

class Execution(unittest.TestCase):
    def test_method_does_not_confuse_api_and_editor(self):
        for operation,expected in [('create-field','API oficial'),('edit-visual-node','Interface documentada')]:
            code,out,err=call('method','choose','--operation',operation,'--attempts','2')
            self.assertEqual(code,0,err);self.assertEqual(out['execution_method'],expected);self.assertTrue(out['replan']);self.assertIsNone(out['token_usage'])
    def test_release_cannot_claim_1_0(self):
        code,out,err=call('release','check');self.assertEqual(code,0,err);self.assertFalse(out['release_1_0_allowed'])
    def test_spec_not_importable_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve()/'Fixture';ke.create_project(root,'Fixture','Serviço','Triagem')
            args=('salesbot','spec','--project',root,'--recipe','manual','--channel','Instagram','--output','manual.json')
            code,out,err=call(*args);self.assertEqual(code,0,err);self.assertFalse(out['importable'])
            value=json.loads((root/'manual.json').read_text(encoding='utf-8'));self.assertFalse(value['activation_enabled']);self.assertIsNone(value['account_id'])
            self.assertNotEqual(call(*args)[0],0)
    def test_menu_does_not_create_project(self):
        code,out,err=call('menu','--intent','Dúvida pontual');self.assertEqual(code,0,err);self.assertIsNone(out['project'])
    def test_runtime_subset_fails_unknown_keyword(self):
        from schema_runtime import validate
        with self.assertRaises(ValueError):validate({},dict(type='object',oneOf=[]))

if __name__=='__main__':unittest.main()
