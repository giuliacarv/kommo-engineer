# Workflow operacional 0.5 RC

Execute `python -X utf8 <SKILL>/scripts/ke.py <comando>`. Caminhos de evidência/arquivo de entrada ficam dentro do projeto. No Windows, use `python` disponível; não pressuponha o launcher `py`.

## Setup

`menu [--project PATH]`; `setup interview|summary|backlog --project PATH`. A entrevista começa pelo resultado desejado, adapta ordem/exemplos e conserva todos os 18 campos. Propostas precisam de confirmação humana. `summary` é uma visão derivada, nunca outro estado autoritativo. Backlog propõe metas; não cria promessas de execução. Campo técnico desconhecido bloqueia somente tarefa que depende dele.

## Metas e etapas

Todas as ações abaixo exigem `--project PATH --goal META-NNN`:

- `goal select`: muda explicitamente a seleção; criar segunda meta conserva o cursor anterior.
- `goal step add --file step.json`; `goal step status --step E00`; `goal step update --step E00 --file step.json --expected-revision 1`.
- Contrato de etapa: objective, inputs[], prerequisites[], actions[], exceptions[], status, evidence[], logs[], next_action. IDs persistidos META-NNN/E00. Estado done exige referência local de evidência; não significa homologação.
- `goal plan revise --file plano.md --reason TEXTO --expected-version 1`: escreve plan-v002 sem apagar v001; conflitos bloqueiam.
- `goal decision add --summary TEXTO --reason TEXTO --impact TEXTO --disposition accepted|rejected|deferred|superseded [--supersedes DEC-ID]`: append-only em decisions.jsonl. Rejeitado não vira pendência; substituição exige relação com decisão anterior.
- `goal defer|cancel|reopen --reason TEXTO`: reabertura preserva snapshots históricos, invalida aceite atual e exige nova observação. Adiar/cancelar limpa somente seleção dessa meta.
- `goal dependencies [--file deps.json]`: lista ou revisa contratos. Exemplo: [{"goal_id":"META-001","criteria":[1],"resolution":"waived","reason":"Interface dispensada pelo responsável"}]. Sem dispensa explícita, predecessor cancelado não é entrega; ciclos bloqueiam. Consulte só critérios da interface necessária.
- `goal handoff`: gera prompt com caminhos, versão, estado e dependências reais; não envia mensagens nem cria chats automaticamente.

## Aceite e continuidade

`goal accept --criterion 1 --evidence arquivo` agora registra **evidence_attached**. Não fecha a meta. Após executar teste e conferir conteúdo, use `goal observe --criterion 1 --method TEXTO --result TEXTO --level offline|account|deployed [--account-id ID --scope-ref REF] [--human-approved]`. Observações remotas exigem vínculo de conta do projeto e referência do escopo autorizado. Esse comando registra declaração do operador, não autentica a verdade semântica do resultado. Não use offline como homologação de CRM.

`goal close` exige observação por critério, dependências satisfeitas e hashes íntegros. Snapshot conserva documentos, etapas e decisões; não restaura conta Kommo. Falha de precondição não abandona bloqueio de recuperação; falha durante múltiplas escritas conserva pending-operation para diagnóstico.

## Migração

`project migrate --project PATH` conserva cópia e hashes antes de migrar v1→v2. Não toca snapshots. Evidência legada verified vira legacy_unreviewed; histórico concluído não é silenciosamente homologado. Rollback documental: suspender escritas e restaurar arquivos do manifesto de migração, conservando eventos e snapshots. Não converter esquema por simples substituição de nomes.

## Entregas cumulativas

`report add --project PATH --goal META-NNN --file entrega.json`: title, before, objective, solution, role, daily_tasks, common_errors, faq, level e evidence[]. Níveis documentado/offline não viram recurso implantado. `report build` gera releases imutáveis e aliases correntes; treinamento só ensina como ativo o que tem meta concluída e observações na conta. Resultado comercial e ROI continuam a medir.
