# Schemas JSON — estado de uso

Os arquivos `*.schema.json` documentam o formato pretendido para os registros locais do Kommo Engineer. Eles são referências de projeto nesta versão e não são aplicados pela CLI. O arquivo `setup-fields.json` é diferente: ele é o contrato de campos do onboarding e é carregado pela CLI.

## O que a CLI valida

A CLI **não carrega nem aplica** os schemas JSON ao ler ou gravar arquivos. `project validate` executa verificações estruturais implementadas diretamente no código, como consistência do `project_id`, do setup e das referências de snapshots. Essa verificação não equivale à validação completa contra JSON Schema.

Não use a presença destes arquivos, nem uma resposta bem-sucedida de `project validate`, como prova de que todos os dados satisfazem os schemas. A integração de um validador JSON Schema para os registros de metas, eventos e snapshots continua pendente.

`setup-fields.json` define campos, grupos, obrigatoriedade, núcleo de planejamento, perguntas e exemplos. A CLI usa este arquivo para calcular o status do setup e as próximas perguntas; preserve compatibilidade do contrato ao editá-lo.

## Compatibilidade

Os schemas declaram JSON Schema Draft 2020-12. Alterações neles não mudam por si só o comportamento da CLI; qualquer mudança de contrato deve atualizar a implementação e os critérios de aceitação correspondentes.


## Atualização 0.5 RC

Consulte [workflow operacional](../references/operational-workflow.md). O aceite por arquivo foi substituído por anexo + teste/observação explícitos. Schemas são validados em runtime no subconjunto documentado; relatórios têm releases imutáveis.
