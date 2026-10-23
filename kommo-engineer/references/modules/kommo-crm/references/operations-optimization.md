# Gestão comercial, recomendações e melhoria contínua

## Operação diária

Priorize por compromisso, valor potencial e urgência observável: negociação/ação vencida, lead de bom fit que respondeu, reunião e preparo, follow-up devido, entrada sem atendimento e depois prospecção/enriquecimento. Ajuste ao modelo da conta; não deixe oportunidade com intenção real esperando para cumprir volume de mensagens.

Para lead ativo, conferir responsável, estágio coerente, último contato comprovado, compromisso atual, próxima ação e prazo. Separe fit, temperatura, prioridade, valor e probabilidade. Uma resposta não comprova qualificação; silêncio não prova desinteresse. Perda/descarte precisam de motivo factual. Oportunidade futura precisa de evento/data, motivo e próximo contato.

Antes de preparar mensagem ou cadência, ler conversa recente e ramo vigente do playbook. Resposta, recusa, opt-out, reunião, negociação ou transferência humana podem suspender a cadência. Recomendar mensagem não é autorização para enviá-la. Respeite linguagem, provas e oferta adotadas pela conta; não invente preço, resultado, urgência ou escassez.

## Métricas com contrato

Defina a população, período, timezone, timestamps/eventos usados, fórmula, exclusões e cobertura. Separe entrada, estoque, transição e fechamento. Conversão de uma coorte de entrada não deve misturar ganhos de oportunidades antigas no numerador. Marque amostra pequena, dados ausentes, oportunidade ainda aberta e atraso do ciclo.

| Indicador | Definição a adotar/validar | Cuidado |
|---|---|---|
| Tempo até primeiro atendimento | Primeiro atendimento humano relevante − entrada | Autoresposta não vira atendimento humano; relatar mediana/p90 e amostra |
| Cumprimento de SLA | Casos elegíveis atendidos no prazo / elegíveis | Horário útil, feriados e pausa explícitos |
| Conversão entre etapas | Leads da coorte que alcançaram destino / elegíveis na origem | Definir reentrada, salto de etapa e janela |
| Win rate | Ganhos / (ganhos + perdidos) da população encerrada | Relatar abertos separadamente e não chamar isso de conversão de entrada |
| Aging / ciclo | Tempo na etapa / duração até encerramento | Histórico de transições; `updated_at` não substitui entrada na etapa |
| Cobertura de próxima ação | Ativos com ação futura relevante / ativos elegíveis | Tarefa genérica no futuro pode não ser compromisso útil |
| Ticket / receita | Valor dos ganhos confirmados / quantidade; soma separada | Distinguir proposta, contratado, recebido e recorrente |
| Forecast ponderado | Soma de valor × probabilidade dos deals abertos elegíveis | Probabilidade calibrada ou explicitamente fornecida; ausente não vira chute |
| Duplicidade / completude | Critério de identidade / campos necessários por momento | Mostrar denominador, regra e conflitos |
| Aquisição → qualidade → venda | Custos e resultados ligados à origem/campanha | CPL sozinho não mede valor do lead; cobrir perdas de atribuição |

Não crie novas metas ou taxas “boas” universais. Use baseline da conta e objetivo acordado; comparação externa exige fonte atual e contexto equivalente. Se custo/valor confiável faltar, reporte a lacuna em vez de fabricar ROAS.

## Recomendar com consequência prática

Cada recomendação relevante deve responder: qual evidência mostra o problema, quem é afetado, qual resultado deve melhorar, qual mudança concreta resolve, quais dependências existem, como validar e como medir depois. Diferencie correção comprovada de hipótese experimental. Esforço/impacto estimados são aproximações.

Priorize, nesta lógica ajustável:

1. Perda de entrada, falha de atendimento, responsável ausente ou compromisso abandonado.
2. Dado errado/duplicado e automação que age sobre ele.
3. Gargalo de jornada ou fricção comercial sustentado por dados.
4. Economia de esforço recorrente e redução de erro.
5. Sofisticação adicional quando a base e o volume justificarem.

Evite criar campo, bot ou IA para compensar ausência de regra comercial. Compare opção nativa, ajuste de processo e integração externa em custo total, esforço do usuário, manutenção, cobertura e risco de duplicidade.

Para experimento, registrar hipótese, segmento, baseline, mudança, métrica principal, sinais de piora, janela compatível com ciclo e critério de decisão. Não alterar várias partes da jornada e atribuir o ganho a uma só. Scores/heurísticas podem orientar teste, mas precisam de evidência/calibração antes de automatizar decisões relevantes.

## Apoio de outras skills

Consultar a skill disponível pelo nome/caminho instalado quando a especialidade for necessária. A kommo-crm mantém o contrato de conta, dado e execução; a especialista aprofunda a tarefa, sem autorizar ações em outro sistema.

| Skill indicada pelo usuário | Contribuição para Kommo | Limite da contribuição |
|---|---|---|
| `conduzir-diagnostico-vendas` | Perguntas sobre situação, dor, impacto, decisão e próximo passo; requisitos de qualificação | Perguntar o que falta, sem questionário repetido; dado não informado continua pendente |
| `escalar-playbook-vendas` | Entrada/saída das etapas, rotas, handoff, capacitação e revisão | Cadência e número de etapas de exemplo não são regra fixa |
| `sales-enablement` | Scripts, objeções, materiais e demo dentro da jornada | Provas/ROI/oferta exigem fonte da conta; não inventar promessa |
| `aplicar-psicologia-vendas` | Clareza, confiança, fricção, objeção e negociação ética | Sem pressão, escassez ou autoridade falsas |
| `metha-diretor-comercial` (local/global) | Prioridade, fit, forecast, oferta e fontes da Metha | Somente contexto Metha; versões antigas que dizem “Kommo desativado” não anulam autorização humana posterior |
| `cro` | Fricção entre anúncio, página, formulário e entrada no CRM | Hipótese de página não prova defeito do CRM nem autoriza publicação |
| `conversion-tracking` | Contrato de qualificação/venda e retorno de conversões offline | Revalidar APIs, elegibilidade, janelas e deduplicação em docs atuais; não copiar limiares/código ilustrativo como contrato |
| `meta_ads_api` | IDs/campanhas e diagnóstico de aquisição quando solicitado | Marketing API, CAPI e CRM são integrações distintas; verificar versão atual, sem ativar anúncio ou orçamento por uma tarefa de CRM |
| `escolher-momento-pedir-indicacao` | Pós-venda com valor percebido, satisfação, histórico de pedido e pausa | Pontuação/intervalo ilustrativos precisam de calibração; recompensa/contato exigem escopo próprio |
| `find-skills` | Procurar lacuna especializada que as ferramentas/skills atuais não resolvem | Não instalar pacotes por rotina; verificar qualidade e dependências antes de propor |

Prefira a cópia específica do projeto quando aplicável; verifique divergências materiais com a instrução atual. Não importe o funil, ICP, IDs, playbook ou sistemas da Metha para outra conta.
