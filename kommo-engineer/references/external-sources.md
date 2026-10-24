# Fontes externas e conhecimento incorporado

Revisão estática local de nove repositórios fornecidos pelo usuário em 23/10/2026. As referências abaixo são sínteses próprias em português, aprofundadas por decisões da Kommo Engineer. Nenhum repositório, dependência, serviço de IA, widget ou workflow foi instalado ou executado.

O commit e os arquivos identificam o material consultado. Não são garantia de versão atual, direito operacional ou recurso disponível na conta. Licença não localizada ou declaração em README não foi tratada como licença irrestrita para copiar código; esta expansão não redistribui implementações externas.

<a id="ext-001"></a>

## EXT-001 — Kommo-MCP

Fonte: [Miguelgbastos/Kommo-MCP](https://github.com/Miguelgbastos/Kommo-MCP/tree/97eaab686ad6a19c10b074cdad2d57cdaa74d915). Licença observada: MIT, arquivo LICENSE presente.

Conhecimento próprio: [MCP: transportes, capacidades e relatórios](integrations/mcp-transport-and-capabilities.md).

Já coberto: Identidade por leitura, ferramentas disponíveis e segurança de credenciais; Retries e evidência de execução.

Aprofundado: Perfis de servidores MCP, stdio/HTTP e matriz de compatibilidade; Health/readiness versus identidade autenticada; Relatório calculado: população, fechamento, fuso e denominador.

Limites observados: Nomes e schemas deste servidor diferem de runitsolutions/kommo-mcp; Compatibilidade automatizada declarada não é validação neste Codex.

Evidência local identificada: [README.md](https://github.com/Miguelgbastos/Kommo-MCP/blob/97eaab686ad6a19c10b074cdad2d57cdaa74d915/README.md), [LICENSE](https://github.com/Miguelgbastos/Kommo-MCP/blob/97eaab686ad6a19c10b074cdad2d57cdaa74d915/LICENSE), [src/kommo-api.ts](https://github.com/Miguelgbastos/Kommo-MCP/blob/97eaab686ad6a19c10b074cdad2d57cdaa74d915/src/kommo-api.ts), [src/mcp/tool-definitions.ts](https://github.com/Miguelgbastos/Kommo-MCP/blob/97eaab686ad6a19c10b074cdad2d57cdaa74d915/src/mcp/tool-definitions.ts), [src/mcp/tool-handlers.ts](https://github.com/Miguelgbastos/Kommo-MCP/blob/97eaab686ad6a19c10b074cdad2d57cdaa74d915/src/mcp/tool-handlers.ts).

<a id="ext-002"></a>

## EXT-002 — create-kommo-integration

Fonte: [kommo-crm/create-kommo-integration](https://github.com/kommo-crm/create-kommo-integration/tree/421df75de1b9ce9d608d7c64da4f7b6424c21f92). Licença observada: Licença customizada QSOFT baseada em MIT, com restrições adicionais no arquivo LICENCE.

Conhecimento próprio: [Widgets React, callbacks e empacotamento](engineering/widgets-and-react.md).

Já coberto: SDK público, segredo no backend e teste de lifecycle.

Aprofundado: Manifest, locais, i18n e bundle de produção como contratos separados; Callback do SDK versus adaptação do wrapper React; Desmontagem, isolamento da UI e retorno de Salesbot validado.

Limites observados: Gerador instala dependências; ler o projeto não autoriza executá-lo; Servidor exemplo armazena token em JSON e faz POST para return_url recebido; não transportar como padrão de produção.

Evidência local identificada: [README.md](https://github.com/kommo-crm/create-kommo-integration/blob/421df75de1b9ce9d608d7c64da4f7b6424c21f92/README.md), [LICENCE](https://github.com/kommo-crm/create-kommo-integration/blob/421df75de1b9ce9d608d7c64da4f7b6424c21f92/LICENCE), [cli/build.ts](https://github.com/kommo-crm/create-kommo-integration/blob/421df75de1b9ce9d608d7c64da4f7b6424c21f92/cli/build.ts), [templates/kommo-react-integration/client/src/integration.ts](https://github.com/kommo-crm/create-kommo-integration/blob/421df75de1b9ce9d608d7c64da4f7b6424c21f92/templates/kommo-react-integration/client/src/integration.ts), [templates/kommo-react-integration/client/src/__emptyCallbacks__/destroyCallback/destroyCallback.tsx](https://github.com/kommo-crm/create-kommo-integration/blob/421df75de1b9ce9d608d7c64da4f7b6424c21f92/templates/kommo-react-integration/client/src/__emptyCallbacks__/destroyCallback/destroyCallback.tsx).

<a id="ext-003"></a>

## EXT-003 — n8n-nodes-kommo

Fonte: [yatolstoy/n8n-nodes-kommo](https://github.com/yatolstoy/n8n-nodes-kommo/tree/8d8c993c2fbca8ad64fc59bfcf0953f03f08705d). Licença observada: Texto permissivo no LICENSE.md; atribuição n8n no arquivo.

Conhecimento próprio: [Nós n8n, itens, tipos e isolamento](integrations/n8n-community-nodes.md).

Já coberto: Webhooks, n8n, idempotência e fila de erro.

Aprofundado: Contrato do nó community e item linking; Preservação de zero, false, arrays e intenção de limpar campos; Cache por conta/credencial, paginação e erro por item.

Limites observados: Helper clearNullableProps descarta zero e reconstrói arrays não vazios como objetos; Cache consultado usa nome da função como chave, sem conta/credencial.

Evidência local identificada: [README.md](https://github.com/yatolstoy/n8n-nodes-kommo/blob/8d8c993c2fbca8ad64fc59bfcf0953f03f08705d/README.md), [LICENSE.md](https://github.com/yatolstoy/n8n-nodes-kommo/blob/8d8c993c2fbca8ad64fc59bfcf0953f03f08705d/LICENSE.md), [credentials/kommoOAuth2Api.credentials.ts](https://github.com/yatolstoy/n8n-nodes-kommo/blob/8d8c993c2fbca8ad64fc59bfcf0953f03f08705d/credentials/kommoOAuth2Api.credentials.ts), [nodes/Kommo/V1/KommoV1.node.ts](https://github.com/yatolstoy/n8n-nodes-kommo/blob/8d8c993c2fbca8ad64fc59bfcf0953f03f08705d/nodes/Kommo/V1/KommoV1.node.ts), [nodes/Kommo/V1/transport/index.ts](https://github.com/yatolstoy/n8n-nodes-kommo/blob/8d8c993c2fbca8ad64fc59bfcf0953f03f08705d/nodes/Kommo/V1/transport/index.ts).

<a id="ext-004"></a>

## EXT-004 — kommo-crm-audit

Fonte: [tamibot/kommo-crm-audit](https://github.com/tamibot/kommo-crm-audit/tree/7ca3ff0e7146c3994e9c78af64132e70b927d16c). Licença observada: README declara MIT; arquivo de licença não encontrado no snapshot.

Conhecimento próprio: [Auditoria estrutural e funcional de Salesbots](automation/salesbot-graph-audit.md).

Já coberto: Gatilhos, dependências, cenários negativos e readback.

Aprofundado: Grafo de passos e grafo entre bots; Alcançabilidade, referências, ciclos limitados e inventário de consumidores; Achado rastreável e armazenamento relacional opcional com snapshot.

Limites observados: Formato model.text/_start/_stop do exemplo não define todo Salesbot; Validador sinaliza goto para número menor; isso não prova ciclo infinito nem cobertura completa; Fonte sugere capturar chamadas internas; usar como evidência, sem transformá-las em API suportada.

Evidência local identificada: [README.md](https://github.com/tamibot/kommo-crm-audit/blob/7ca3ff0e7146c3994e9c78af64132e70b927d16c/README.md), [docs/metodologia_analisis.md](https://github.com/tamibot/kommo-crm-audit/blob/7ca3ff0e7146c3994e9c78af64132e70b927d16c/docs/metodologia_analisis.md), [scripts/validar_bot.py](https://github.com/tamibot/kommo-crm-audit/blob/7ca3ff0e7146c3994e9c78af64132e70b927d16c/scripts/validar_bot.py), [scripts/analizar.py](https://github.com/tamibot/kommo-crm-audit/blob/7ca3ff0e7146c3994e9c78af64132e70b927d16c/scripts/analizar.py).

<a id="ext-005"></a>

## EXT-005 — kommoCRM-GS-API-sync

Fonte: [by-dujiy/kommoCRM-GS-API-sync](https://github.com/by-dujiy/kommoCRM-GS-API-sync/tree/832e6a56ba7004ecd4aa8de6d746740c34841322). Licença observada: MIT, arquivo LICENSE presente.

Conhecimento próprio: [Sincronização CRM e Google Sheets](integrations/google-sheets-sync.md).

Já coberto: Fonte por campo, identidade, direção e reconciliação.

Aprofundado: Comparação com baseline por registro e campo para sincronização bilateral; Identidade estável da linha, fórmulas, locale e distinção de vazio; Cursor confirmado após persistência, sobreposição e recuperação de falha parcial.

Limites observados: Exemplo é específico de agenda clínica; não herdar entidades ou campos desse negócio; Cursor max_updated+10 pode deixar intervalo não lido; Loops sem limite e logs de payload não viram padrão de implementação.

Evidência local identificada: [README.md](https://github.com/by-dujiy/kommoCRM-GS-API-sync/blob/832e6a56ba7004ecd4aa8de6d746740c34841322/README.md), [LICENSE](https://github.com/by-dujiy/kommoCRM-GS-API-sync/blob/832e6a56ba7004ecd4aa8de6d746740c34841322/LICENSE), [run_app.py](https://github.com/by-dujiy/kommoCRM-GS-API-sync/blob/832e6a56ba7004ecd4aa8de6d746740c34841322/run_app.py), [src/gs_api.py](https://github.com/by-dujiy/kommoCRM-GS-API-sync/blob/832e6a56ba7004ecd4aa8de6d746740c34841322/src/gs_api.py), [src/kommo_api.py](https://github.com/by-dujiy/kommoCRM-GS-API-sync/blob/832e6a56ba7004ecd4aa8de6d746740c34841322/src/kommo_api.py).

<a id="ext-006"></a>

## EXT-006 — kommo-onboarding

Fonte: [tamibot/kommo-onboarding](https://github.com/tamibot/kommo-onboarding/tree/e7bcbdc80976d82cd4f795026d2c4c2a2ef1c98a). Licença observada: MIT, arquivo LICENSE presente.

Conhecimento próprio: [Onboarding baseado em conversas e desenho tipado](strategy/conversation-led-onboarding.md).

Já coberto: Setup guiado, proposta, campos, metas e autorização.

Aprofundado: Amostragem de conversas com evidência e separação de papéis; Contrato de desenho antes de planilha ou implantação; Mapeamento por chave lógica e IDs reais, plano por dependências e compensação.

Limites observados: Deployer usa setTimeout e gera IDs simulados, sem executar os POST comentados; Rollback imprime exclusões e remove o mapeamento local, sem DELETE remoto; Modelo injeta etapas/campos fixos e lê credenciais de planilha; esses padrões não foram incorporados.

Evidência local identificada: [README.md](https://github.com/tamibot/kommo-onboarding/blob/e7bcbdc80976d82cd4f795026d2c4c2a2ef1c98a/README.md), [LICENSE](https://github.com/tamibot/kommo-onboarding/blob/e7bcbdc80976d82cd4f795026d2c4c2a2ef1c98a/LICENSE), [apps/onboarding-engine/src/chatParser.js](https://github.com/tamibot/kommo-onboarding/blob/e7bcbdc80976d82cd4f795026d2c4c2a2ef1c98a/apps/onboarding-engine/src/chatParser.js), [apps/onboarding-engine/src/kommoDeployer.js](https://github.com/tamibot/kommo-onboarding/blob/e7bcbdc80976d82cd4f795026d2c4c2a2ef1c98a/apps/onboarding-engine/src/kommoDeployer.js), [apps/onboarding-engine/src/kommoRollback.js](https://github.com/tamibot/kommo-onboarding/blob/e7bcbdc80976d82cd4f795026d2c4c2a2ef1c98a/apps/onboarding-engine/src/kommoRollback.js).

<a id="ext-007"></a>

## EXT-007 — Agente-Conversacional-Kommo-CRM-LMStudio-VS-OpenAI

Fonte: [KevinInoCol/Agente-Conversacional-Kommo-CRM-LMStudio-VS-OpenAI](https://github.com/KevinInoCol/Agente-Conversacional-Kommo-CRM-LMStudio-VS-OpenAI/tree/20bccb881c5fe8f5dd2a7417448d4aadac1c807c). Licença observada: Arquivo de licença não encontrado no snapshot.

Conhecimento próprio: [Agentes externos, RAG, memória e áudio](ai/external-rag-agents.md).

Já coberto: Agente nativo, fontes, limites, ações e handoff.

Aprofundado: Arquitetura externa distinta do agente nativo Kommo; Compatibilidade de tool calling, memória por conta/canal/conversa e recuperação RAG; Recepção durável, outbox, áudio e controle de envio.

Limites observados: Deduplicação em memória por lead:text e BackgroundTasks não garantem recuperação entre processos; Thread apenas por lead não basta para isolar múltiplas contas/canais; Downloader tenta reenviar Bearer após 401/403 da URL recebida; requer verificação do destino; Trocar o LLM por local não torna embeddings/parser/transcrição locais.

Evidência local identificada: [README.md](https://github.com/KevinInoCol/Agente-Conversacional-Kommo-CRM-LMStudio-VS-OpenAI/blob/20bccb881c5fe8f5dd2a7417448d4aadac1c807c/README.md), [app.py](https://github.com/KevinInoCol/Agente-Conversacional-Kommo-CRM-LMStudio-VS-OpenAI/blob/20bccb881c5fe8f5dd2a7417448d4aadac1c807c/app.py), [agent.py](https://github.com/KevinInoCol/Agente-Conversacional-Kommo-CRM-LMStudio-VS-OpenAI/blob/20bccb881c5fe8f5dd2a7417448d4aadac1c807c/agent.py), [chat_history/postgres_store.py](https://github.com/KevinInoCol/Agente-Conversacional-Kommo-CRM-LMStudio-VS-OpenAI/blob/20bccb881c5fe8f5dd2a7417448d4aadac1c807c/chat_history/postgres_store.py), [tools/retrieval.py](https://github.com/KevinInoCol/Agente-Conversacional-Kommo-CRM-LMStudio-VS-OpenAI/blob/20bccb881c5fe8f5dd2a7417448d4aadac1c807c/tools/retrieval.py).

<a id="ext-008"></a>

## EXT-008 — kommo-sdk-data-engineer

Fonte: [nascin/kommo-sdk-data-engineer](https://github.com/nascin/kommo-sdk-data-engineer/tree/6a2fcd548fef1af93472a91160d20d35b1115ca0). Licença observada: Arquivo LICENSE permissivo com cabeçalho Python Packaging Authority; não presume auditoria de autoria.

Conhecimento próprio: [Extração, modelos, eventos e qualidade de dados](data/extraction-and-modeling.md).

Já coberto: Paginação, tipos, cobertura e métricas com fontes.

Aprofundado: Camada bruta e tabelas de entidades, relações e campos multivalorados; Schema drift, saída tabular e semântica de None/erro/página vazia; Incremental com watermark e reconciliação de exclusões, reentradas e páginas.

Limites observados: Retorno None pode representar fim ou exceção em métodos observados; Paralelismo e sleeps por worker não comprovam limite agregado; Páginas parciais acumuladas e exceções internas não podem ser declaradas exportação completa.

Evidência local identificada: [README.md](https://github.com/nascin/kommo-sdk-data-engineer/blob/6a2fcd548fef1af93472a91160d20d35b1115ca0/README.md), [LICENSE](https://github.com/nascin/kommo-sdk-data-engineer/blob/6a2fcd548fef1af93472a91160d20d35b1115ca0/LICENSE), [kommo_sdk_data_engineer/kommo.py](https://github.com/nascin/kommo-sdk-data-engineer/blob/6a2fcd548fef1af93472a91160d20d35b1115ca0/kommo_sdk_data_engineer/kommo.py), [kommo_sdk_data_engineer/endpoints/leads.py](https://github.com/nascin/kommo-sdk-data-engineer/blob/6a2fcd548fef1af93472a91160d20d35b1115ca0/kommo_sdk_data_engineer/endpoints/leads.py), [kommo_sdk_data_engineer/endpoints/events.py](https://github.com/nascin/kommo-sdk-data-engineer/blob/6a2fcd548fef1af93472a91160d20d35b1115ca0/kommo_sdk_data_engineer/endpoints/events.py).

<a id="ext-009"></a>

## EXT-009 — KommoCRM-Integracao-de-analise-de-tempo-por-etapa-kmm

Fonte: [guilhermeDaviDev/KommoCRM-Integracao-de-analise-de-tempo-por-etapa-kmm](https://github.com/guilhermeDaviDev/KommoCRM-Integracao-de-analise-de-tempo-por-etapa-kmm/tree/e704952fa5de6b13609e63e75190847f1d0195af). Licença observada: Arquivo de licença não encontrado no snapshot.

Conhecimento próprio: [Tempo por etapa, reentrada e SLA](analytics/stage-time-and-sla.md).

Já coberto: Aging, tempo entre marcos e critérios locais de SLA.

Aprofundado: Visitas de etapa e intervalos de responsável, cobertura temporal e censura; Durabilidade central versus observação de navegador; Média, percentis, aging aberto e limites sem lacunas.

Limites observados: ZIP consulta leads com page:1 e limit:250 e depende de aba aberta/localStorage; Inicialização usa created_at como início da etapa, sem provar entrada nela; Limite vermelho é lido mas não usado no cálculo da cor; alteração de owner sobrescreve o intervalo corrente; Agregação observada mistura durações encerradas e abertas.

Evidência local identificada: [README.md](https://github.com/guilhermeDaviDev/KommoCRM-Integracao-de-analise-de-tempo-por-etapa-kmm/blob/e704952fa5de6b13609e63e75190847f1d0195af/README.md), [2.0.zip](https://github.com/guilhermeDaviDev/KommoCRM-Integracao-de-analise-de-tempo-por-etapa-kmm/blob/e704952fa5de6b13609e63e75190847f1d0195af/2.0.zip).

## Uso e manutenção

Leia primeiro a referência da tarefa. O registro de fontes serve para proveniência e revisão, sem exigir nova pesquisa de todos os repositórios em cada consulta. Revalide somente contratos mutáveis e capacidades necessárias à implementação. Exemplos de negócios, modelos, IDs, SLAs, APIs internas e promessas de automação das fontes não são regras da conta do usuário.
