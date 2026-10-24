# Escolha funcional e implantação

Compare primeiro a solução: nativo (estado determinístico), Salesbot (sequência explícita), IA (linguagem), Marketplace (capacidade de fornecedor), n8n (orquestração), custom (controle). Separadamente escolha API, contrato JSON do editor, UI assistida ou navegador. API não é uma arquitetura de negócio.

`method choose --operation create-field|edit-visual-node|salesbot-json|pipeline|integration [--account-verified --permission-verified] [--attempts 2]` devolve método condicional, alternativas e necessidade de replanejar. As flags são contexto declarado, não provas. Em campo/funil prefira API documentada após conferir identidade/permissão; para nó visual sem API use interface. JSON de especificação não é REST nem arquivo importável.

Cada tarefa: receita local → pré-requisitos → método → teste → readback. Uma falha: classificar, mudar uma hipótese. Duas falhas da mesma hipótese: suspender essa tentativa e replanejar. Registre chamada, hipótese, resultado e retrabalho em events; tokens só se houver telemetria da ferramenta. Não estime tokens a partir do tamanho de arquivo como consumo real.

## Capacidade

A matriz machine-readable fica em [capabilities.json](knowledge/contracts/capabilities.json). Documentação pública não prova plano, permissão, canal ou conta. Planos, canais e permissões permanecem unknown até evidência local. Listar bots não prova criar/editar definições completas. O executor desta versão não inicia bots, envia mensagens nem apaga recursos.
