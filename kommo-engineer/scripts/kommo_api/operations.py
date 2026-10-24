"""Small reviewed mutation subset, stale-state comparison and durable journal."""
import hashlib
import json
import os
from pathlib import Path
from .client import APIError

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()

def contract(spec):
    if set(spec)-{'kind','action','entity','pipeline_id','id','values'}:raise APIError('unknown_spec_key')
    kind=spec.get('kind');action=spec.get('action');values=spec.get('values')
    if kind not in ('field','pipeline','stage') or action not in ('create','update'):raise APIError('unsupported_operation')
    if not isinstance(values,dict) or not values or set(values)-({'name','type','sort'} if kind=='field' and action=='create' else {'name','sort'}):raise APIError('unsupported_values')
    if 'name' in values and (not isinstance(values['name'],str) or not values['name'].strip() or len(values['name'])>255):raise APIError('invalid_name')
    if action=='create' and not values.get('name'):raise APIError('missing_name')
    if 'sort' in values and (type(values['sort']) is not int or values['sort']<1):raise APIError('invalid_sort')
    if action=='create' and kind in ('stage','pipeline') and 'sort' not in values:raise APIError('missing_sort')
    if kind=='field':
        if spec.get('entity') not in ('leads','contacts','companies'):raise APIError('invalid_entity')
        if action=='create' and values.get('type') not in ('text','numeric','checkbox','date','url','textarea','date_time'):raise APIError('unsupported_field_type')
        collection=f"/api/v4/{spec['entity']}/custom_fields";key='custom_fields'
    elif kind=='pipeline':collection='/api/v4/leads/pipelines';key='pipelines'
    else:
        if type(spec.get('pipeline_id')) is not int or spec['pipeline_id']<1:raise APIError('invalid_pipeline_id')
        collection=f"/api/v4/leads/pipelines/{spec['pipeline_id']}/statuses";key='statuses'
    if action=='update' and (type(spec.get('id')) is not int or spec['id']<1):raise APIError('invalid_id')
    if kind=='stage' and action=='update' and spec['id'] in (142,143):raise APIError('system_stage_outside_subset')
    method='POST' if action=='create' else 'PATCH';path=collection
    body=[values] if action=='create' else [dict(id=spec['id'],**values)] if kind=='field' else values
    if action=='update' and kind!='field':path+='/'+str(spec['id'])
    return dict(collection=collection,key=key,method=method,path=path,body=body)

def plan(client,spec,account_id):
    ct=contract(spec);identity=client.identity(account_id);items=client.collection(ct['collection'],ct['key'])
    current=next((x for x in items if x.get('id')==spec.get('id')),None) if spec['action']=='update' else None
    if spec['action']=='update' and current is None:raise APIError('target_not_found')
    if any(str(x.get('name','')).casefold()==str(spec['values'].get('name','')).casefold() and x.get('id')!=spec.get('id') for x in items):raise APIError('duplicate_name')
    projection=[{k:x.get(k) for k in ('id','name','type','sort')} for x in items]
    return dict(account_id=identity['id'],subdomain=client.subdomain,spec=spec,contract=ct,pre_digest=digest(projection),before={k:current.get(k) for k in ('id','name','type','sort')} if current else None,after=spec['values'],status='dry_run',requires=['explicit scope','administrator permission','controlled account homologation'],verified_in_account=False)

def apply(k,root,client,approved,scope):
    k.ensure_safe_text(json.dumps(approved,ensure_ascii=False));k.ensure_safe_text(json.dumps(scope,ensure_ascii=False))
    if os.environ.get('KOMMO_ENABLE_WRITES')!='true':raise APIError('writes_disabled')
    if not scope.get('approved') or scope.get('plan_digest')!=digest(approved) or scope.get('subdomain')!=client.subdomain or scope.get('account_id')!=approved['account_id'] or not scope.get('authorization_ref') or scope.get('administrator_confirmed') is not True:raise APIError('authorization_scope_mismatch')
    project=k.readj(k.data_dir(root)/'project.json')
    if project.get('account_id')!=approved['account_id']:raise APIError('project_account_mismatch')
    with k.locked(root):
        journal=k.data_dir(root)/'api-operations';journal.mkdir(exist_ok=True)
        records=[k.readj(f) for f in journal.glob('*.json')]
        if any(x['status'] in ('prepared','ambiguous') for x in records):raise APIError('unreconciled_operation')
        if any(x.get('approved_digest')==digest(approved) and x['status']=='observed_pass' for x in records):raise APIError('operation_already_applied')
        fresh=plan(client,approved['spec'],approved['account_id'])
        if fresh!=approved:raise APIError('stale_plan_rebuild_required')
        op='OP-'+k.uid();path=journal/(op+'.json');record=dict(operation_id=op,status='prepared',approved_digest=digest(approved),plan=approved,at=k.now(),authorization_ref=scope['authorization_ref'])
        k.putj(path,record,once=True)
        try:
            client.request(fresh['contract']['method'],fresh['contract']['path'],fresh['contract']['body'],write_enabled=True)
            observed=client.collection(fresh['contract']['collection'],fresh['contract']['key'])
            matches=[x for x in observed if (x.get('id')==fresh['spec'].get('id') if fresh['spec']['action']=='update' else x.get('name')==fresh['spec']['values']['name']) and all(x.get(key)==val for key,val in fresh['spec']['values'].items())]
            if len(matches)!=1:raise APIError('readback_not_unique',True)
            record.update(status='observed_pass',observed={key:matches[0].get(key) for key in ('id','name','type','sort')},verified_at=k.now())
        except APIError as exc:
            record.update(status='ambiguous' if exc.ambiguous or exc.code not in ('400','401','403','422') else 'rejected',error=exc.code);k.putj(path,record);raise
        except Exception:
            record.update(status='ambiguous',error='unexpected_transport_failure');k.putj(path,record);raise APIError('unexpected_transport_failure',True) from None
        k.putj(path,record);k.event(root,'api_operation',op+': '+record['status']);return record

def reconcile(k,root,client,operation_id,conclusion,reason):
    if not __import__('re').fullmatch(r'OP-[0-9a-f]{12}',operation_id):raise APIError('invalid_operation_id')
    if conclusion not in ('observed_pass','not_applied'):raise APIError('invalid_conclusion')
    reason=k.ensure_safe_text(reason)
    with k.locked(root):
        path=k.data_dir(root)/'api-operations'/(operation_id+'.json');record=k.readj(path)
        if record['status'] not in ('prepared','ambiguous'):raise APIError('already_reconciled')
        pl=record['plan'];client.identity(pl['account_id']);ct=pl['contract'];items=client.collection(ct['collection'],ct['key'])
        matches=[x for x in items if (x.get('id')==pl['spec'].get('id') if pl['spec']['action']=='update' else x.get('name')==pl['spec']['values']['name']) and all(x.get(key)==val for key,val in pl['spec']['values'].items())]
        if conclusion=='observed_pass' and len(matches)!=1:raise APIError('readback_not_unique',True)
        projection=[{key:x.get(key) for key in ('id','name','type','sort')} for x in items]
        if conclusion=='not_applied' and digest(projection)!=pl['pre_digest']:raise APIError('absence_not_proven',True)
        record.update(status=conclusion,reconciliation=dict(at=k.now(),reason=reason,read_digest=digest(projection)));k.putj(path,record);k.event(root,'api_reconciled',operation_id+': '+conclusion)
    return record
