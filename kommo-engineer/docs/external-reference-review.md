# Expansão da Kommo Engineer por fontes externas

Revisão local em 23/10/2026. Foram examinados individualmente nove repositórios da pasta fornecida. Não havia `SKILL.md` nesses snapshots: o aproveitamento é de conhecimento e padrões de engenharia, com redação própria e aplicação ao domínio da skill.

## Aproveitamento por fonte

| Fonte | Já existia na Kommo Engineer | Aprofundamento próprio |
|---|---|---|
| EXT-001 — Kommo-MCP | Identidade por leitura, ferramentas disponíveis e segurança de credenciais; Retries e evidência de execução | [MCP: transportes, capacidades e relatórios](../references/integrations/mcp-transport-and-capabilities.md) |
| EXT-002 — create-kommo-integration | SDK público, segredo no backend e teste de lifecycle | [Widgets React, callbacks e empacotamento](../references/engineering/widgets-and-react.md) |
| EXT-003 — n8n-nodes-kommo | Webhooks, n8n, idempotência e fila de erro | [Nós n8n, itens, tipos e isolamento](../references/integrations/n8n-community-nodes.md) |
| EXT-004 — kommo-crm-audit | Gatilhos, dependências, cenários negativos e readback | [Auditoria estrutural e funcional de Salesbots](../references/automation/salesbot-graph-audit.md) |
| EXT-005 — kommoCRM-GS-API-sync | Fonte por campo, identidade, direção e reconciliação | [Sincronização CRM e Google Sheets](../references/integrations/google-sheets-sync.md) |
| EXT-006 — kommo-onboarding | Setup guiado, proposta, campos, metas e autorização | [Onboarding baseado em conversas e desenho tipado](../references/strategy/conversation-led-onboarding.md) |
| EXT-007 — Agente-Conversacional-Kommo-CRM-LMStudio-VS-OpenAI | Agente nativo, fontes, limites, ações e handoff | [Agentes externos, RAG, memória e áudio](../references/ai/external-rag-agents.md) |
| EXT-008 — kommo-sdk-data-engineer | Paginação, tipos, cobertura e métricas com fontes | [Extração, modelos, eventos e qualidade de dados](../references/data/extraction-and-modeling.md) |
| EXT-009 — KommoCRM-Integracao-de-analise-de-tempo-por-etapa-kmm | Aging, tempo entre marcos e critérios locais de SLA | [Tempo por etapa, reentrada e SLA](../references/analytics/stage-time-and-sla.md) |

O [registro de fontes](../references/external-sources.md) detalha commits, licenças observadas, evidências e limites. O [registro técnico](external-reference-review.json) guarda inventários e hashes, arquivos inspecionados e cobertura por fonte.

## Preservação e validação

Todos os arquivos anteriores permanecem no pacote. Guias existentes foram expandidos por acréscimo; os utilitários, testes, schemas, templates e imagens anteriores mantêm seus bytes. O catálogo preserva todas as entradas anteriores. A validação final, o backup e a sincronização da instalação são registrados no arquivo técnico ao concluir a revisão.

Código externo não foi copiado nem executado, e não foram instaladas dependências ou feitas chamadas de IA/CRM. Os novos guias são conhecimento documentado, não conectores ou automações homologadas. As quatro falhas preexistentes da suíte CLI Windows, registradas na revisão anterior, continuam sendo uma limitação conhecida do código original preservado.

## Resultado da conferência

- Nove fontes e 64 artefatos de evidência identificados; nove guias próprios adicionados.
- Dos 117 arquivos anteriores, 102 mantêm os mesmos bytes e 13 documentos preservam integralmente o conteúdo anterior com acréscimos ao final. Manifesto e catálogo foram atualizados; as 16 entradas anteriores do catálogo permanecem e o total passa a 25.
- Validador skill-creator aprovado; integridade Python 3/3; buscas por nove especialidades 9/9; 257 links locais resolvidos. Esses checks validam pacote e descoberta, sem homologar integrações externas.
- Backup anterior da fonte e da instalação: `C:\Users\Usuário\Documents\Codex\Skill_KommoEngineer\legado\backup-kommo-engineer-referencias-20261023-215155-utc`. A instalação global é sincronizada com esta fonte por comparação de inventário e hashes.
