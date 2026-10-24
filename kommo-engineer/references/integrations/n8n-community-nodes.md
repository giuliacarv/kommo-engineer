# n8n: nó Kommo, tipos, itens e isolamento

Use quando a solução depender de um nó community Kommo, sua autenticação, campos dinâmicos, operação em lote ou resultado por item. Complementa [integrações](../crm/automation-integrations.md). Não instala nem ativa workflows.

## Identificar a superfície instalada

Registre versão do n8n, pacote do nó, versão/typeVersion da operação, modo de credencial e conta alvo. A existência de um nó Kommo não comprova cobertura de Salesbot, chat ou editor. Consulte recurso e operação específicos. Quando faltar uma operação, compare um HTTP Request com API suportada ou outro adaptador; não invente uma opção no nó.

Preserve o formato real de entrada/saída. O código consultado agrega páginas HAL e associa saídas aos itens de origem. Expressões que selecionam o primeiro item podem reaplicar todos os registros ao mesmo lead; cada ação precisa manter sua identidade ao atravessar divisão, merge e erro.

## Dados que não podem mudar silenciosamente

| Valor | Regra de transformação |
|---|---|
| Número zero | Valor válido quando o campo permite; não confundir com ausente por teste de truthiness |
| `false` | Estado explícito; não remover como vazio |
| Campo ausente | Não atualizar por padrão; distinto de uma solicitação de limpeza |
| `null`, texto vazio ou array vazio | Semântica deve vir do contrato do campo/operação, não de um limpador genérico |
| Array de objetos | Preservar ordem/estrutura esperada; não converter seus índices em propriedades de objeto |
| Select/multiselect | Resolver IDs de enum na conta e entidade corretas, sem misturar rótulo e ID |
| Data | Definir formato, fuso e unidade; evitar converter um agendamento em meia-noite por fallback |

Na fonte, `clearNullableProps` usa truthiness e recursão de objetos que pode remover zero e reconstruir arrays. Trate isso como comportamento a testar na versão usada; não adote o helper como sanitização universal. Registre dados recusados e razão, preservando o valor original na área privada.

## Opções e cache

Dropdown de responsável, pipeline, etapa ou enum deve corresponder à credencial selecionada. Chave de cache precisa distinguir servidor/conta/credencial, recurso e parâmetros relevantes; expiração curta não evita vazamento entre contas.

O helper consultado usa o nome da função como chave. Antes de usar a mesma instância n8n para vários clientes, teste troca de credencial, enum duplicado por nome e carregamentos simultâneos. Não presuma que opção exibida prova ID válido para a escrita atual.

## Execução por item e falha parcial

Mantenha `itemIndex`/item linking ou equivalente da versão, chave do registro, operação e resultado. `continueOnFail` pode produzir um item com erro em vez de lançar exceção; o próximo nó precisa verificar esse estado antes de enviar mensagem, atualizar planilha ou marcar conclusão.

Confronte contagens: recebidos, elegíveis, aplicados, rejeitados, incertos e reconciliados. Não contabilize saída com objeto de erro como sucesso. Para retry, use chave de evento/operação e journal; o mecanismo de reexecução do n8n pode repetir itens cujo efeito já ocorreu.

Confira se “todos” realmente percorre páginas até o critério documentado, se a saída contém páginas ou entidades e se o limite do nó é amostra ou corte. Um mutex serializa chamadas desse processo; ele não comprova uma taxa global nem substitui backoff/coordenação da conta.

## Autenticação e aceite

OAuth e token de longa duração são opções distintas; a Redirect URL precisa corresponder ao cliente e integração corretos. O credenciamento fica no armazenamento do n8n. Exporte workflow com referências de credencial, sem valor de segredo; não copie a configuração privada para a skill.

Casos relevantes: dois itens de leads diferentes; zero/false; select e array; conta A seguida de B; página extra; erro de um item; timeout após efeito; replay sem duplicação. Compare payload saneado, resposta e leitura de volta. Um nó verde isolado não prova entrega no canal.

O [contrato reutilizável](../../assets/templates/integration-contract.json) ajuda a definir identidade, mapeamento e reconciliação. Origem metodológica: [EXT-003](../external-sources.md#ext-003). Nenhum pacote community foi instalado ou executado.
