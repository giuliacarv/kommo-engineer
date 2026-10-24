# Operação Kommo — consultor e executor
Use `knowledge find --query "..."` e abra um único procedimento por vez.

## Dados e autorização
Kommo distingue leads, contatos e empresas; campos personalizados têm entidade e tipo.
IDs e estágios de sistema requerem cuidado. Antes de enviar dados de produção, confirme alvo.

## Digital Pipeline e Salesbot
Confirme gatilho, canal, plano, entrada, condições, campos (lead/contato/empresa), caminho alternativo,
handoff humano, encerramento e prevenção de duplicidade.
Editor visual, código-fonte Salesbot e widget SDK são contratos diferentes.
Nunca transforme JSON de API ou n8n em script Salesbot.

## Integração
Identifique origem do evento, Content-Type real, autenticação, headers, limites, idempotência,
timeout, erros 401/403/429/5xx, logs sem segredos, atualização concorrente e replay.
Webhooks gerais Kommo usam x-www-form-urlencoded; parseie segundo documentação.

## Resultado
Considere entregue somente com evidência observável, método e ambiente identificados.

Detalhes: [engenharia de conta](crm/account-engineering.md), [integrações](crm/automation-integrations.md), [conexão](crm/connection.md), [execução](crm/safe-execution.md) e [MCP](integrations/kommo-mcp.md).
