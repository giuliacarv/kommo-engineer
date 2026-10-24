# Tempo por etapa, reentrada, responsável e SLA

Use para aging, gargalo de funil, duração de visitas, comparação de equipes ou painel de SLA. Aprofunda [RevOps](../strategy/revops-and-pipeline.md), [operações](../crm/operations-optimization.md) e [extração de eventos](../data/extraction-and-modeling.md).

## Definir o relógio e a unidade de análise

Separe tempo desde criação do lead, tempo desde entrada na etapa atual, duração de uma visita concluída, soma de várias visitas e tempo até um resultado comercial. `created_at` não comprova quando a oportunidade entrou na etapa atual.

Defina janela, fuso, calendário corrido ou horário útil, pausas e exclusões segundo a operação. Sem política confirmada, apresente duração em unidade explícita e evite rotular atraso por limites herdados.

## Reconstruir visitas e intervalos

Uma visita deve identificar conta, lead, pipeline, etapa, entrada, saída ou instante de observação, origem e qualidade da evidência. Ao sair e retornar à mesma etapa, abra outra visita; não sobrescreva a anterior. Se o pipeline mudar, preserve o par pipeline/etapa de cada visita.

Ordene eventos por timestamp e desempate confiável, deduplique IDs e confira continuidade antes/depois. Eventos fora de ordem podem exigir recomputar os intervalos afetados. Sem histórico suficiente, informe início desconhecido ou observado, em vez de assumir criação ou instalação como entrada real.

Mudança de responsável dentro da mesma etapa exige intervalos próprios para atribuir tempo por pessoa. Somente atualizar o owner atual perde a distribuição histórica; não atribua toda a espera ao último vendedor. Diferencie owner atual, owner da entrada e contribuição durante o intervalo.

## Qualidade de cobertura

| Fonte | O que pode sustentar | Limite relevante |
|---|---|---|
| Histórico/eventos com cobertura conhecida | Transições e responsáveis no intervalo coberto | Retenção, paginação e eventos ausentes podem limitar retroatividade |
| Webhooks persistidos | Transições observadas desde a captura | Repetição, ordem e falha de recepção precisam de reconciliação |
| Polling | Estado nos instantes das leituras | Pode perder uma etapa atravessada entre duas consultas |
| localStorage do navegador | Histórico observado naquele navegador e origem | Aba fechada, limpeza, outro usuário/dispositivo e quota quebram continuidade |

Considere casos censurados: lead já estava na etapa quando começou a observação; visita segue aberta no fechamento do relatório; trecho do histórico está ausente. Identifique-os e evite misturá-los a durações completas sem explicação. Não prometa histórico retroativo usando apenas o estado atual.

Para um monitor contínuo, avalie captura e persistência no backend, chaves por conta, reconciliação e visualização. Um widget pode apresentar dados centrais, mas a presença do painel não prova cobertura contínua.

## Estatística e SLA

Mostre população e quantidade de visitas válidas, abertas, desconhecidas e excluídas. Separe duração de visitas concluídas de aging das abertas. Média misturada pode parecer melhoria quando vários leads recém-criados entram na amostra. Use mediana/percentis quando ajudarem e houver amostra suficiente, com o cálculo identificado.

Compare coortes, etapas e condições equivalentes antes de concluir que um responsável é lento. Controle reentrada, mix de complexidade, backlog herdado e horário útil quando relevantes. Tempo alto é sinal para investigar o processo; não prova causa ou desempenho individual por si só.

Defina limites ordenados, unidades e condições sem lacunas ou sobreposição. Teste exatamente em cada limite, imediatamente antes/depois, configuração ausente, zero e valor inválido. Um campo configurável de SLA só funciona se o código o utiliza.

## Limitações concretas da referência inspecionada

No ZIP fornecido, o script consulta leads com `page:1`, mantém dados em localStorage e depende do intervalo com a aba aberta. Inicializa o início da etapa com criação do lead; alterações de owner atualizam o responsável corrente sem registrar um novo intervalo. A visão agregada mistura histórico encerrado e duração ainda aberta.

O código lê um parâmetro vermelho, mas a função de cor usa verde, amarelo e um caso final vermelho; portanto, mudar o terceiro parâmetro não altera essa função. Nome de arquivo ZIP, versão declarada e comportamento também devem ser conferidos nos artefatos reais. Esses achados limitam o que o painel pode provar; os valores padrão da fonte não são SLA da empresa.

Aceite: reconstrução de um caso com entrada/saída conhecida, reentrada, troca de responsável, mudança de pipeline, leitura faltante e visita aberta; contagens e fórmulas reproduzíveis; fronteiras de SLA verificadas. Não implante nem altere widget para concluir uma análise documental.

Origem metodológica: [EXT-009](../external-sources.md#ext-009). ZIP inspecionado em memória, sem instalação ou execução do JavaScript.
