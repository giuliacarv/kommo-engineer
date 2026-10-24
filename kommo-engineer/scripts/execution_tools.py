import json
from pathlib import Path
from kommo_api.client import Client,APIError
from kommo_api.operations import plan,apply,reconcile,digest

def configure(sub):
    p=sub.add_parser('method');s=p.add_subparsers(dest='action',required=True);q=s.add_parser('choose')
    q.add_argument('--operation',choices=['create-field','edit-visual-node','salesbot-json','pipeline','integration'],required=True)
    q.add_argument('--account-verified',action='store_true');q.add_argument('--permission-verified',action='store_true');q.add_argument('--attempts',type=int,default=0)
    p=sub.add_parser('api');s=p.add_subparsers(dest='action',required=True)
    for action in ('doctor','read','inventory','bind','plan','apply','reconcile'):
        q=s.add_parser(action);q.add_argument('--subdomain',required=True)
        q.add_argument('--account-id',type=int,required=action!='doctor')
        if action in ('inventory','bind','plan','apply','reconcile'):q.add_argument('--project',required=True)
        if action=='read':q.add_argument('--resource',choices=['leads','contacts','companies','fields-leads','fields-contacts','fields-companies','pipelines','statuses','bots'],required=True);q.add_argument('--pipeline-id',type=int)
        if action in ('plan','apply'):q.add_argument('--file',required=True)
        if action=='apply':q.add_argument('--scope',required=True)
        if action=='reconcile':q.add_argument('--operation-id',required=True);q.add_argument('--conclusion',choices=['observed_pass','not_applied'],required=True);q.add_argument('--reason',required=True)
    p=sub.add_parser('salesbot');s=p.add_subparsers(dest='action',required=True);q=s.add_parser('spec')
    q.add_argument('--recipe',choices=['triage','qualification','followup','instagram','manual','ai-handoff','seller-macro'],required=True)
    q.add_argument('--project',required=True);q.add_argument('--output',required=True);q.add_argument('--channel',required=True)
    p=sub.add_parser('release');s=p.add_subparsers(dest='action',required=True);s.add_parser('check')

def run(a,k):
    if a.command=='method':
        supported=a.operation in ('create-field','pipeline')
        ready=a.account_verified and a.permission_verified
        return dict(operation=a.operation,functional_solution='Kommo nativo' if supported else 'Salesbot' if a.operation in ('edit-visual-node','salesbot-json') else 'Contrato nativo/integrador a comparar',execution_method='API oficial' if supported else 'Interface documentada' if a.operation=='edit-visual-node' else 'Especificação; confirmar superfície e schema' if a.operation=='salesbot-json' else 'n8n/Marketplace após confirmar versão e operação',readiness='ready_for_scoped_test' if ready else 'conditional_on_account_and_permission',replan=a.attempts>=2,alternatives=['A — nativo e contrato conhecido','B — integrador gerenciado, manutenção adicional','C — custom, mais controle e custo'],token_usage=None,note='Dois insucessos na mesma hipótese exigem replanejamento; flags não substituem readback da conta')
    if a.command=='release':
        matrix=k.readj(k.SKILL/'docs/certification.json')
        return dict(version=k.VERSION,release_1_0_allowed=False,matrix=matrix,missing=['E2E em conta de homologação','Dois chats independentes em cada ambiente','Três tarefas por usuário leigo','Métricas comparáveis reais'],note='O comando não certifica plataformas nem CRM a partir de testes offline')
    root=k.getroot(a.project) if getattr(a,'project',None) else None
    if a.command=='salesbot':
        flows={
            'triage':['welcome','intent','route','human_handoff','stop'],
            'qualification':['welcome','qualification_questions','record_confirmed_fields','route','human_handoff','stop'],
            'followup':['check_eligibility','check_reply_and_optout','wait','send_approved_message','human_handoff','stop'],
            'instagram':['check_event_and_channel','welcome','intent','ai_or_human','stop'],
            'manual':['manual_start','seller_approved_macro','stop'],
            'ai-handoff':['eligibility','knowledge_lookup','confidence_and_scope','human_handoff','stop'],
            'seller-macro':['manual_start','validate_context','suggest_message','seller_review','stop']}
        nodes=flows[a.recipe]
        spec=dict(schema_version=1,kind='salesbot_design_spec_not_importable',recipe=a.recipe,channel=k.ensure_safe_text(a.channel),status='offline_design',activation_enabled=False,
                  account_id=None,entity_ids={},start='N01',nodes=[dict(id=f'N{i:02}',intent=n,next=f'N{i+1:02}' if i<len(nodes) else None,on_error='human_handoff',observed_editor_handler=None) for i,n in enumerate(nodes,1)],
                  preflight=['Confirmar conta/plano/canal','Resolver IDs no inventário atual','Confirmar schema exato do editor','Exportar backup antes de mudar visual/código','Revisar gatilhos/exclusões/duplicidade','Testar cada saída com contato controlado'],
                  manual_rule='Sem gatilho automático não impede início via API/outro bot quando disponível; escolha por / depende do canal e UI',
                  scenarios=[dict(input='resposta esperada',expect='rota prevista'),dict(input='resposta livre',expect='fallback humano'),dict(input='silêncio',expect='limite de espera e parada'),dict(input='opt-out',expect='suprimir novas mensagens'),dict(input='falha de envio ou integração',expect='registrar e transferir sem repetir envio cegamente')],
                  gaps=['IDs e handlers reais não resolvidos','Importação e execução não homologadas'],remote_changes=False)
        dest=(root/a.output).resolve()
        if not dest.is_relative_to(root) or dest.suffix!='.json':raise k.KEError('Saída JSON deve ficar dentro do projeto')
        with k.locked(root):k.putj(dest,spec,once=True);k.event(root,'salesbot_spec',a.recipe)
        return dict(file=str(dest),status=spec['status'],importable=False)
    try:
        client=Client(a.subdomain)
        if a.action=='doctor':return dict(account=client.identity(a.account_id),read_verified=True,write_permission='unknown',plan='unknown',calls=client.calls)
        identity=client.identity(a.account_id)
        if a.action=='bind':
            with k.locked(root):
                p=k.readj(k.data_dir(root)/'project.json')
                if p.get('account_id') not in (None,a.account_id):raise k.KEError('Projeto vinculado a outra conta; migração requer revisão explícita')
                p.update(account_id=a.account_id,account_subdomain=a.subdomain,revision=p['revision']+1,updated_at=k.now());k.putj(k.data_dir(root)/'project.json',p);k.event(root,'account_bound','Identidade lida por API; autorização de escrita não inferida')
            return dict(account=identity,bound=True)
        if a.action=='plan':
            spec=k.readj(k.ensure_safe_relative(root,Path(a.file)));k.ensure_safe_text(json.dumps(spec,ensure_ascii=False));result=plan(client,spec,a.account_id)
            dest=k.data_dir(root)/'api-plans'/('PLAN-'+k.uid()+'.json')
            with k.locked(root):k.putj(dest,result,once=True)
            return dict(file=str(dest),digest=digest(result),diff=result,changes_applied=False)
        if a.action=='apply':return apply(k,root,client,k.readj(k.ensure_safe_relative(root,Path(a.file))),k.readj(k.ensure_safe_relative(root,Path(a.scope))))
        if a.action=='reconcile':return reconcile(k,root,client,a.operation_id,a.conclusion,a.reason)
        paths={'leads':('/api/v4/leads','leads'),'contacts':('/api/v4/contacts','contacts'),'companies':('/api/v4/companies','companies'),'pipelines':('/api/v4/leads/pipelines','pipelines'),'bots':('/api/v4/bots','items')}
        paths.update({'fields-'+e:(f'/api/v4/{e}/custom_fields','custom_fields') for e in ('leads','contacts','companies')})
        if a.action=='read':
            if a.resource=='statuses':
                if not a.pipeline_id or a.pipeline_id<1:raise k.KEError('--pipeline-id positivo é obrigatório')
                path,key=f'/api/v4/leads/pipelines/{a.pipeline_id}/statuses','statuses'
            else:path,key=paths[a.resource]
            values=client.collection(path,key)
            return dict(account_id=a.account_id,resource=a.resource,items=[{key:v.get(key) for key in ('id','name','type','sort')} for v in values],calls=client.calls,contains_full_records=False)
        # Inventory deliberately excludes lead/contact records and stores only account-local metadata.
        inventory=dict(account=identity,observed_at=k.now(),invalidate_before_mutation=True,resources={})
        for res in ('fields-leads','fields-contacts','fields-companies','pipelines','bots'):
            path,key=paths[res];values=client.collection(path,key)
            inventory['resources'][res]=[{key:v.get(key) for key in ('id','name','type','sort')} for v in values]
            if res=='pipelines':
                for pipeline in values:
                    items=client.collection(f"/api/v4/leads/pipelines/{pipeline['id']}/statuses",'statuses')
                    inventory['resources']['statuses-'+str(pipeline['id'])]=[{key:v.get(key) for key in ('id','name','sort')} for v in items]
        dest=k.data_dir(root)/'inventory'/str(a.account_id)/('INV-'+k.uid()+'.json')
        with k.locked(root):k.putj(dest,inventory,once=True)
        return dict(file=str(dest),calls=client.calls,account_id=a.account_id,write_permission='unknown')
    except APIError as exc:raise k.KEError(str(exc)) from None
