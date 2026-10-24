"""Derived reports: immutable releases and cumulative delivery records."""
def build(k,root):
    d=k.data_dir(root)/'deliveries';records=[k.readj(f) for f in sorted((d/'records').glob('*.json'))]
    complete=[g for g in k.list_goals(root) if g['status']=='completed']
    lines=['# Relatório de implementação','','Fonte: registros locais. Resultado comercial e ROI: a medir.','']
    if not complete:lines+=['Nenhuma meta foi concluída com observação registrada.','']
    for g in complete:lines += [f"## {g['id']} — {g['title']}",'','Concluída no nível de observação registrado; isso pode ser somente offline.','']
    train=['# Treinamento operacional','','Conteúdo remoto exige evidência da conta. Registros offline aparecem apenas como preparação.','']
    for rec in records:
        state=k.readj(k.gp(root,rec['goal_id'])/'state.json')
        acc=k.readj(k.gp(root,rec['goal_id'])/'acceptance.json')['criteria']
        demonstrated=state['status']=='completed' and all(x.get('observation',{}).get('level') in ('account','deployed') and x['status'] in ('observed_pass','human_approved') for x in acc)
        approved=rec['level'] in ('account','deployed') and demonstrated
        label='Homologado segundo evidências registradas' if approved else 'Preparado; homologação pendente'
        lines += [f"## {rec['title']}",'',label,f"Antes: {rec['before']}",f"Objetivo: {rec['objective']}",f"Solução: {rec['solution']}",'Evidências: '+', '.join(rec['evidence']),'']
        if approved:
            train += [f"## {rec['title']} — {rec['role']}",'',str(rec['daily_tasks']), 'Erros comuns: '+str(rec['common_errors']),'FAQ: '+str(rec['faq']),'']
        else:train += [f"- {rec['title']}: preparação, ainda não ensinar como implantação ativa.",'']
    with k.locked(root):
        release=d/'releases'/('REL-'+k.uid());release.mkdir(parents=True)
        files=[]
        for name,content in [('relatorio.md',lines),('treinamento.md',train),('playbook.md',['# Playbook','','Uso diário: seguir somente recursos homologados e respeitar o papel de cada usuário.','']+lines+['---']+train)]:
            raw=('\n'.join(content)+'\n').encode('utf-8');k.write_bytes_once(release/name,raw);k.atomic_write(d/name,raw);files.append(str(release/name))
        k.putj(release/'manifest.json',dict(at=k.now(),records=len(records),files={n:k.sha(release/n) for n in ('relatorio.md','treinamento.md','playbook.md')}),once=True)
        k.event(root,'report_built',release.name)
    return dict(files=files,completed_goals=len(complete),delivery_records=len(records),release=str(release))
