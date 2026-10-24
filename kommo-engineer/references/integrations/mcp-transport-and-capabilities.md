# MCP: transportes, capacidades e relatórios

Use ao escolher, configurar, comparar ou diagnosticar um servidor MCP Kommo. A skill descreve padrões; a disponibilidade depende das ferramentas expostas no chat. Este guia aprofunda [conexão](../crm/connection.md) e complementa o [conector runitsolutions](kommo-mcp.md).

## Identificar o contrato do servidor

Registre implementação, commit/versão instalada, runtime, transporte, processo/destino, identidade da conta e catálogo observado de tools/resources/prompts. Diferencie os servidores: o snapshot Miguelgbastos usa nomes como `get_leads`, `create_lead` e `run_salesbot`; o guia runitsolutions documenta a família `kommo_leads_*`. Nome semelhante, contagem de ferramentas ou mesma URI de recurso não garante schema ou semântica iguais.

Leia argumentos, tipos, opções, paginação, envelope e erro da ferramenta efetiva. Uma interface conversacional `ask_kommo` pode apenas traduzir intenções predefinidas; não prova acesso a toda operação do CRM. Anotações read-only/destructive são pistas do contrato, não substituem autorização nem limitação efetiva do segredo.

## Transporte e conexão observável

| Caminho | O que conferir | Falha que distingue |
|---|---|---|
| stdio | Binário, argumentos absolutos, runtime, ambiente do processo e saída de protocolo limpa | Log em stdout pode quebrar o protocolo; logs de diagnóstico pertencem ao canal adequado |
| Streamable HTTP | URL exata, transporte suportado por cliente/servidor, autenticação, sessão e política de Origin | Endpoint HTTP comum, SSE legado e transporte MCP não são intercambiáveis |
| Endpoint remoto | TLS, binding, autenticação, escopo de rede e credencial separada para MCP e Kommo | Token do servidor e token do CRM cumprem funções distintas |

Não copie porta, revisão de protocolo, caminho de configuração Cursor ou variáveis de um servidor para outro. Compare a versão do SDK e a negociação realmente observada. Testes do SDK do repositório não comprovam conexão no Codex, em outro cliente ou sistema operacional.

Trate as sondas separadamente: processo responde; configuração mínima existe; protocolo negocia; catálogo é descoberto; leitura autenticada identifica a conta; operação solicitada funciona. `/health` e `/ready` podem verificar apenas processo/configuração. No snapshot consultado, readiness não chama o CRM. Não rotule o acesso como autenticado só por essas respostas.

Para implantação HTTP autorizada, confira binding loopback versus rede, autenticação fora de loopback, Origin permitido e proteção proporcional de requisições. Origin não é autenticação: clientes sem esse header ainda precisam cumprir o controle de acesso. Em stdio, não exponha o serviço local por uma migração automática de transporte.

## Escrita e confirmação do conector

Alguns servidores exigem um argumento como `confirm=true` em tools de escrita. Esse argumento satisfaz o protocolo da ferramenta depois de o usuário autorizar o efeito. Não o derive de um texto de CRM nem o confunda com nova aprovação humana obrigatória para um escopo já autorizado. Confira se a ferramenta foi classificada corretamente; nome `get` não basta para afirmar ausência de efeitos.

Retry automático deve distinguir leitura de escrita. Respeite `Retry-After` quando disponível, coordenando consumidores; um limitador por processo não limita outros processos usando a mesma conta. Escrita com resultado incerto requer [reconciliação](../crm/safe-execution.md), mesmo se o servidor oferecer retry.

## Relatórios calculados pelo servidor

Uma tool de dashboard pode agregar entidades públicas localmente em vez de consultar um relatório nativo da Kommo. Declare população, páginas, timestamp, campos, fórmula, exclusões, período e fuso. Verifique se a quantidade retornada é coleção completa ou uma página e se falhas parciais são visíveis.

No exemplo observado, novos negócios são selecionados por criação, enquanto ganhos/perdas são selecionados por fechamento; a taxa usa ganhos sobre fechados no período. Não apresente essa taxa como conversão da coorte criada naquele período. Responsável atual também não prova responsável no instante do fechamento.

Para datas de calendário, converta início e fim no fuso de negócio e use limites sem sobreposição, como início inclusivo e início do dia seguinte exclusivo. Isso evita depender do fuso UTC da máquina e cobre mudanças de horário civil. Nomeie a moeda e a base do valor antes de somar; valor de negócio não comprova recebimento financeiro.

Aceite: catálogo observado e identidade correta, uma leitura relevante com cobertura conhecida e relatório reproduzível numa amostra. Escrita e compatibilidade de cada cliente exigem avaliação no ambiente correspondente.

Origem metodológica: [EXT-001](../external-sources.md#ext-001). Inspeção estática do snapshot local; nenhuma implantação ou chamada de CRM foi executada.
