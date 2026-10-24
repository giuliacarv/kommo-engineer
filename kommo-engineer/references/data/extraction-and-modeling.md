# Engenharia de dados Kommo: extração, modelos e eventos

Use para inventário amplo, exportação, BI, DataFrame, migração analítica ou atualização incremental. Aprofunda [modelo de CRM](../crm/crm-design.md), [execução](../crm/safe-execution.md) e [RevOps](../strategy/revops-and-pipeline.md). Uma lista tabular não prova que toda a conta foi lida.

## Contrato e cobertura da extração

Registre conta, entidade, filtros, `with` suportado, ordenação, janela, início/fim, páginas, registros únicos, erros e estado de completude. Confira no contrato atual quais relações são embutidas e quais precisam de leitura separada. Solicitar contatos ou catálogo não assegura todos os dados desses objetos.

Separe página vazia/fim documentado de falha de rede, 401/403, 429, resposta inválida ou erro de modelo. Um SDK que devolve `None` em várias situações não permite inferir coleção completa sem evidência adicional. Não avance o cursor nem produza contagem final silenciosa quando houver página ausente.

Controle taxa agregada e paralelismo. Dormir por worker ou limitar quantidade de threads não comprova taxa por conta. Páginas lidas fora de ordem e dados alterados durante a paginação podem gerar lacunas/duplicatas; use ordenação, deduplicação e reconciliação suportadas, declarando que uma extração longa não é snapshot transacional.

## Camadas e modelo tabular

Preserve resposta bruta necessária em área privada, com origem e hash; gere tabelas derivadas de forma reproduzível. O dado bruto permite revisar perda causada por parsing sem refazer toda leitura. Colete só o necessário e evite payload pessoal em logs.

| Conjunto | Chave e semântica a preservar |
|---|---|
| Lead, contato, empresa | Conta+entidade+ID; fatos próprios de cada entidade |
| Relações | IDs de ambas as pontas, tipo e evidência de vínculo; não inferir relação pelo nome |
| Campo e enum | Entidade, field_id, enum_id, tipo e versão; rótulo pode mudar |
| Valor personalizado | Entidade/ID, field_id, enum quando houver e multiplicidade dos valores |
| Pipeline e etapa | Pipeline_id+status_id e semântica local; histórico de nome quando necessário |
| Evento | Conta+ID/tipo, entidade, timestamp, autor e valores antes/depois disponíveis |
| Tag, catálogo e associação | IDs e ponte de associação; evitar multiplicar métricas ao fazer join |

`to_dataframe` converte a representação do SDK, não recupera campos que ele descartou nem verifica completude. Ao expandir listas ou joins, explique o grão: uma linha por lead, por valor de campo ou por associação. Somar receita depois de juntar vários contatos pode duplicar o valor do mesmo negócio.

## Tipos e evolução de schema

Defina ausência, `null`, vazio, zero e false. Preserve telefone/ID como string quando necessário e datas com unidade/fuso. Enum não reconhecido, campo novo e atributo adicional devem gerar tratamento explícito: compatível, quarentena ou erro recuperável; não eliminar informação silenciosamente.

Modelo Pydantic estrito pode ajudar a detectar drift, mas também rejeitar um dado válido adicionado pela API. Capture a causa e a cobertura afetada, preserve a versão bruta pertinente e revise o modelo. Não trate exceção de parsing como fim de dados.

## Incremental e reconciliação

Escolha watermark/evento e filtro pela documentação atual. Armazene cursor junto com a confirmação da carga correspondente; sobreposição e deduplicação podem cobrir timestamps iguais e eventos tardios. Nunca “pule alguns segundos” para evitar repetição sem provar ausência de dados no intervalo.

Considere objetos alterados após o início, eventos fora de ordem, reentradas, vínculos removidos, exclusões e restauração. Se a API não fornecer exclusões na leitura escolhida, declare essa cobertura e use reconciliação periódica proporcional. Ausência em uma página não é tombstone.

Em falha parcial, preserve páginas/resultados confirmados, marque intervalo pendente e recomece de um ponto conciliável. Não declare carga bem-sucedida só porque algumas listas internas foram preenchidas.

## Aceite e uso analítico

Reconcilie contagens por entidade, IDs únicos, amostra de multiselect/relacionamentos, enums, datas e cobertura de páginas. Reexecute um intervalo para comprovar idempotência quando houver persistência. Antes de calcular métricas, confira o grão e o instante do fato; proprietário atual não reconstrói atribuição histórica.

Use [tempo por etapa](../analytics/stage-time-and-sla.md) para reconstrução temporal e [sincronização com Sheets](../integrations/google-sheets-sync.md) quando a tabela também for editável. Origem metodológica: [EXT-008](../external-sources.md#ext-008). Nenhum SDK ou dependência pandas/Pydantic foi instalado por esta manutenção.
