# Aplicação do plano — 0.5.0-rc.1

O documento foi adotado como escopo de evolução, preservando a biblioteca anterior, os 18 campos e scripts existentes. Implementação incremental em branches/PRs, sem merge automático em main. Baseline: 130 arquivos, 39 testes existentes e 4 falhas Windows reproduzidas; após correção os 39 passaram.

Entregas: menu/entrevista e resumo derivado, metas/etapas/decisões/handoff, planos com controle de versão, migração com backup, aceite com observação por nível, snapshots históricos, relatórios cumulativos imutáveis; índice de 39 imagens/26 hashes únicos, 17 nós Salesbot e busca com lacunas; escolha de método separada de solução; cliente API, inventário e dry-run; fatia de escrita desligada, reconciliação e mocks; desenhos de 7 receitas e contrato composto; adaptadores documentados.

## Critério de lançamento

[Certificação por marco](certification.json) e `release check` mantêm 1.0 bloqueada até E2E em conta autorizada, dois chats em cada produto e três tarefas por usuário leigo. O gerador de Salesbot produz especificação, não JSON importável. Não há instalação automática n8n, ativação de automações ou envio de mensagens. A referência visual conserva lacunas; nome de captura não é inspeção de todos os pixels.

## Compatibilidade

CLI anterior continua disponível. Mudança intencional: goal accept anexa evidência; goal observe registra teste/método/resultado antes de close. Projetos v1 são migrados explicitamente; snapshots antigos permanecem intocados. Artefatos de comparação no docs/upgrade-baseline.json. A instalação global só recebe candidato com inventário/hash conferidos e backup prévio.

## Métricas

Sem telemetria de tokens nem implantação de teste concluída: consumo, custo por tarefa aceita e primeiro acerto real permanecem não medidos. Contagens de testes não equivalem a homologação de CRM. Cenários C01-C10 estão mapeados em tests/upgrade-acceptance.md, com pendências explícitas.
