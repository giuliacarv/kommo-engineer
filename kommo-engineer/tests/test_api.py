import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from kommo_api.client import Client,APIError
from kommo_api.operations import contract,plan,apply,digest,reconcile
import test_upgrade
import ke

class Fake:
    def __init__(self):self.items=[];self.calls=[];self.fail_after_post=False;self.fail_readback=False
    def __call__(self,method,path,payload):
        self.calls.append((method,path,payload))
        if path=='/api/v4/account':return dict(id=42,subdomain='test-tenant')
        if method=='GET':
            if self.fail_readback and self.items:raise APIError('503')
            return dict(_embedded=dict(custom_fields=self.items,pipelines=self.items,statuses=self.items,items=self.items))
        if method=='POST':
            self.items += [dict(id=101,**payload[0])]
            if self.fail_after_post:raise APIError('network_timeout',True)
            return {}
        return {}

class ClientTests(unittest.TestCase):
    def test_host_validation(self):
        for host in ('https://evil','x.kommo.com','x@evil','../x','x/','X'):
            with self.assertRaises(APIError):Client(host,token='fixture')
    def test_no_credential_in_repr_or_error(self):
        c=Client('test-tenant',token='fixture-sensitive',transport=Fake())
        self.assertNotIn('fixture-sensitive',repr(c))
        with patch.dict(os.environ,{},clear=True):
            with self.assertRaises(APIError):Client('test-tenant',token='')
    def test_account_mismatch(self):
        c=Client('test-tenant',token='fixture',transport=Fake())
        with self.assertRaises(APIError):c.identity(99)
    def test_redirect_endpoint_and_writes_blocked(self):
        c=Client('test-tenant',token='fixture',transport=Fake())
        for path in ('https://evil','/api/v4/bots/run','/api/v4/account?access_token=x'):
            with self.assertRaises(APIError):c.request('GET',path)
        with patch.dict(os.environ,{},clear=True):
            with self.assertRaises(APIError):c.request('POST','/api/v4/leads/pipelines',[],write_enabled=True)
    def test_error_policy(self):
        for code,attempts in [('401',1),('403',1),('429',3),('500',3),('network_timeout',3)]:
            count=[]
            def fail(*args):count.append(1);raise APIError(code)
            c=Client('test-tenant',token='fixture',transport=fail,sleep=lambda _:None)
            with self.assertRaises(APIError):c.request('GET','/api/v4/account')
            self.assertEqual(len(count),attempts)
    def test_no_blind_post_retry(self):
        count=[]
        def fail(*args):count.append(1);raise APIError('network_timeout',True)
        c=Client('test-tenant',token='fixture',transport=fail,sleep=lambda _:None)
        with patch.dict(os.environ,{'KOMMO_ENABLE_WRITES':'true'}):
            with self.assertRaises(APIError):c.request('POST','/api/v4/leads/pipelines',[],write_enabled=True)
        self.assertEqual(len(count),1)
    def test_paginated_inventory_and_bot_key(self):
        def pages(method,path,payload):
            return {'_embedded':{'items':[{'id':1}]},'_links':{'next':{'href':'ignored'}}} if 'page=1' in path else {'_embedded':{'items':[{'id':2}]}}
        c=Client('test-tenant',token='fixture',transport=pages)
        self.assertEqual([x['id'] for x in c.collection('/api/v4/bots','items')],[1,2])
    def test_unsupported_operation(self):
        with self.assertRaises(APIError):contract(dict(kind='salesbot',action='create',values={'name':'X'}))

class MutationTests(unittest.TestCase):
    def setUp(self):
        test_upgrade.Upgrade.setUp(self);self.fake=Fake();self.client=Client('test-tenant',token='fixture',transport=self.fake,sleep=lambda _:None)
        p=ke.data_dir(self.root)/'project.json';v=ke.readj(p);v['account_id']=42;ke.putj(p,v)
        self.spec=dict(kind='field',action='create',entity='leads',values={'name':'Fixture field','type':'text'})
    def tearDown(self):self.tmp.cleanup()
    def approved(self):
        pl=plan(self.client,self.spec,42)
        scope=dict(approved=True,plan_digest=digest(pl),subdomain='test-tenant',account_id=42,authorization_ref='offline-test',administrator_confirmed=True)
        return pl,scope
    def test_apply_readback_and_duplicate_operation(self):
        pl,scope=self.approved()
        with patch.dict(os.environ,{'KOMMO_ENABLE_WRITES':'true'}):
            out=apply(ke,self.root,self.client,pl,scope);self.assertEqual(out['status'],'observed_pass')
            with self.assertRaises(APIError):apply(ke,self.root,self.client,pl,scope)
        self.assertEqual(len(self.fake.items),1)
    def test_stale_plan_and_authorization(self):
        pl,scope=self.approved();self.fake.items.append(dict(id=50,name='Other'))
        with patch.dict(os.environ,{'KOMMO_ENABLE_WRITES':'true'}):
            with self.assertRaises(APIError):apply(ke,self.root,self.client,pl,scope)
        self.assertFalse(any(c[0]=='POST' for c in self.fake.calls))
    def test_timeout_blocks_until_reconcile(self):
        pl,scope=self.approved();self.fake.fail_after_post=True
        with patch.dict(os.environ,{'KOMMO_ENABLE_WRITES':'true'}):
            with self.assertRaises(APIError):apply(ke,self.root,self.client,pl,scope)
            with self.assertRaises(APIError):apply(ke,self.root,self.client,pl,scope)
        journal=next((ke.data_dir(self.root)/'api-operations').glob('*.json'));rec=ke.readj(journal)
        self.assertEqual(rec['status'],'ambiguous')
        out=reconcile(ke,self.root,self.client,rec['operation_id'],'observed_pass','Fixture conferida')
        self.assertEqual(out['status'],'observed_pass');self.assertEqual(len(self.fake.items),1)

if __name__=='__main__':unittest.main()
