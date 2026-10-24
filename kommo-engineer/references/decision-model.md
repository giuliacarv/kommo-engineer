# Modelo de decisão comercial e técnica

Use para diagnóstico com causas concorrentes, escolha de arquitetura ou trabalho que atravessa estratégia, dados, automação e canal. Perguntas pontuais podem seguir diretamente a referência técnica.

## Do resultado à operação

Forme uma cadeia verificável: resultado desejado → sintoma observado → hipóteses concorrentes → evidência que as distingue → decisão → mudança autorizada → efeito observado. Mantenha fonte, data, população e cobertura nas afirmações materiais. Não substitua lacunas por score, benchmark ou regra herdada de outro cliente.

| Sinal inicial | Hipóteses a separar | Evidência que decide a próxima ação |
|---|---|---|
| Poucos leads qualificados | Aquisição inadequada, critério divergente, dado ausente ou automação que move etapa cedo | Origem/coorte, definição de qualificado, amostra de conversas e histórico de etapas/campos |
| Resposta comercial lenta | Distribuição, capacidade humana, fila, bot concorrente ou canal indisponível | Horários/fuso, recebimento, responsável, próxima tarefa, execução do bot e status do provedor |
| Conversão menor | Mudança de população, denominador, atraso, significado da etapa ou piora real | Coortes comparáveis, eventos de entrada/saída, perdas, campos ausentes e tamanho da amostra |
| IA erra preço ou política | Fonte desatualizada/inativa, integração atrasada, lacuna de contexto ou instrução conflitante | Fonte utilizada e versão, ação reconhecida, catálogo/sync e resposta com contexto controlado |
| Bot não executa | Bot salvo sem entrada, gatilho não ocorrido, condição inelegível, outro bot ou canal | Referências que iniciam o bot, configuração publicada, ocorrência do evento e evidência de execução |
| Campo retorna ao valor antigo | Entidade/enum incorretos, automações concorrentes ou sincronização que sobrescreve | Leitura antes/depois, dono do campo, ordem dos eventos e consumidores que escrevem |
| Registros ou tarefas duplicados | Retry de escrita ambígua, evento repetido, mapeamento de identidade ou regras sobrepostas | Chave/journal, IDs retornados, payload por evento, concorrência e vínculos |
| Ferramenta responde vazio | Filtro, paginação incompleta, conta incorreta, permissão ou normalização | Identidade, schema do MCP/API, páginas e amostra de leitura independente no mesmo escopo |

Antes de concluir, procure uma observação que contradiga a hipótese principal. Diga se o achado é causa demonstrada, explicação provável ou hipótese pendente. Não faça uma alteração grande para investigar um sintoma quando uma leitura delimitada pode distinguir as causas.

## Contrato dos dados

| Informação ou ação | Decisão de modelagem |
|---|---|
| Avanço comercial | Etapa com evidência de entrada/saída; não usar etapa como depósito de dados |
| Fato estruturado | Campo na entidade correta, tipo/enum e fonte definidos; preservar desconhecido e correção do usuário |
| Segmento/seleção | Tag com significado e consumidores identificados; aplicar tag não prova disparo de gatilho |
| Próximo passo | Tarefa com responsável, prazo/fuso, critério de conclusão e proteção contra duplicação |
| Pessoa, escritório e oportunidade | Resolver contato, empresa, lead e seus vínculos; identidade ambígua exige revisão |
| Sincronização | Fonte de verdade por campo, precedência, direção, atraso tolerado e reconciliação |
| Métrica | Numerador, denominador, coorte, período, timestamp, exclusões, cobertura e owner |

Confira os detalhes em [modelo de CRM](crm/crm-design.md), [RevOps](strategy/revops-and-pipeline.md) e [workflow](strategy/workflow-architecture.md). Não crie campos, oportunidades ou conversões para preencher uma hipótese ainda não confirmada.

## Escolha do mecanismo e do grau de autonomia

| O que precisa acontecer | Mecanismo a avaliar | Condição para escolhê-lo |
|---|---|---|
| A pessoa deve revisar a redação ou ação | Sugestão, rascunho ou modelo de chat | Revisão e envio permanecem explícitos; não transformar sugestão em automação |
| Estado de CRM exato ou sequência previsível | Pipeline/Salesbot | Evento e filtros verificáveis, transições, fallback e encerramento claros |
| Interpretar intenção e responder com conhecimento | Agente de IA | Fontes aprovadas, abstenção, ações delimitadas e transferência útil |
| Atendente escolhe iniciar uma sequência | Playbook manual | Inventário confirma entradas; ausência de gatilho local não exclui execução por outro bot/API |
| Trocar dados com outro sistema | Conector, n8n/Make ou backend | Contrato documentado, dono, segurança, deduplicação e recuperação compatíveis com o impacto |
| Sincronização crítica | Persistência/fila proporcional e reconciliação | Eventos e resultados recuperáveis, falhas visíveis e replay sem duplicar |
| Recurso só disponível na interface | UI suportada | Conta/controle corretos, evidência posterior e manutenção viável; endpoint privado não vira contrato |

Use [automação nativa](automation/native-automation.md), [Salesbot](automation/salesbot-playbooks-and-api.md), [IA](ai/native-agents.md) e [integrações](crm/automation-integrations.md) para as diferenças de produto. Compare disponibilidade observada, custo, manutenção, latência necessária, explicabilidade e reversão. Não escolha IA para uma condição exata de tag/campo nem introduza backend só porque ele é possível.

## Combinar IA, Salesbot e atendimento

Defina quem controla a conversa em cada estado e o evento que muda esse controle. Separe interpretar a mensagem, decidir elegibilidade por dados exatos, executar uma sequência e atender uma exceção. Confirme como agente, bot e outras regras param ou retomam; transferência, chat encerrado, lead movido e agente desativado têm efeitos diferentes.

No desenho, explicite fonte e dados já conhecidos, pergunta necessária, destino verificado, condição de avanço, resposta inesperada, pedido de humano, responsável e contexto transferido. Não solicite novamente dados já disponíveis sem motivo. Em falta de fonte ou ambiguidade, defina esclarecimento, abstenção ou atendimento humano.

Avalie cenários normais, quase correspondentes, fonte ausente/conflitante, correção de dado, mensagem repetida, horário/fuso, interrupção humana, ação indevida e falha de integração. Preview avalia parte da conversa; escrita, handoff e entrega requerem observação controlada do efeito e autorização correspondente.

## Da hipótese à implantação

Leve o mesmo contrato comercial até a execução: conta, alvo, campos/IDs, antes/depois, gatilho, exclusões, dono, teste discriminante, limite, aceite e recuperação. Use [proposta](strategy/proposal-and-approval.md), [governança](automation/governance.md) e [execução](crm/safe-execution.md) conforme o impacto.

- Uma atualização simples pode precisar apenas de inspeção e readback. Lote, comunicação ou migração precisam de conjunto explícito, precondições, piloto proporcional, journal e reconciliação.
- Autorização já dada permanece válida para seu escopo; divergência material em conta, audiência, campos ou efeito exige decisão antes da operação afetada.
- Timeout de escrita é resultado desconhecido. Reconciliar antes de repetir; uma nova tentativa não deve criar outra entidade ou mensagem.
- Distinguir documentação, ferramenta disponível, permissão observada, autorização e comportamento homologado. Nenhum desses estados implica automaticamente os seguintes.
- Evidência de configuração, resposta HTTP, execução, persistência e entrega são provas diferentes. Informe a última etapa realmente observada.

## Exemplos de combinação

**Qualificação por IA:** derive dados mínimos do processo comercial; mapeie campo/entidade; mantenha regras exatas no mecanismo determinístico; use fontes curadas para linguagem; defina quando a pessoa assume; confira escrita e parada em cenário autorizado. O agente nativo é orientado a mensagens recebidas, conforme a referência versionada; não desenhe prospecção de saída presumindo essa capacidade.

**Biblioteca de Salesbots manuais:** escolha a sequência pelo trabalho do atendente; inventarie chamadas por gatilho, outro bot e API; mantenha mídia e canal compatíveis; salvar o bot e executá-lo são ações diferentes. Não prometa CRUD público do editor porque a API consegue listar/iniciar/parar bots.

**Formulário com duplicações:** descubra a chave de envio e os vínculos; confira onde o retry ocorre; reconcilie contato/empresa/oportunidade; preserve a resposta recuperável; faça replay limitado com chave e leitura posterior. Frontend publicado não prova que a resposta chegou à oportunidade correta.

**Queda de conversão:** fixe a definição da etapa e a coorte; compare período e completude; cruze origem, qualificação, espera e capacidade; proponha uma intervenção com medida discriminante. Não altere ao mesmo tempo estágio, público e cadência e atribua o resultado a uma única causa.

**Renovação ou expansão:** use sinais de adoção, valor e risco realmente observados; identifique responsável e próxima conversa; valide o interesse antes de criar oportunidade; pause contato quando resposta, opt-out, suporte ou mudança de owner invalidar a cadência.

**MCP autenticado sem escrita:** confira identidade e ferramentas reais; distinga envelopes/paginação do conector e REST; mantenha o plano offline quando faltar operação. Token administrativo e leitura de identidade não comprovam envio de mensagem nem cobertura do editor visual.


## Refinar a hipótese pelo componente

| Evidência nova | Próximo aprofundamento útil |
|---|---|
| Nó n8n recebeu zero/array diferente ou sugeriu enum de outra conta | [Tipos, item linking e cache](integrations/n8n-community-nodes.md) |
| Planilha e CRM mudaram o mesmo campo desde o último ciclo | [Baseline e conflitos por campo](integrations/google-sheets-sync.md) |
| DataFrame parece completo, mas algumas páginas falharam | [Cobertura de extração e schema drift](data/extraction-and-modeling.md) |
| Relatório chama taxa de ganhos sobre fechados de conversão de novos leads | [População e período do relatório MCP](integrations/mcp-transport-and-capabilities.md) |
| Bot volta a passo menor ou inicia outro bot | [Grafo e dependências](automation/salesbot-graph-audit.md) antes de concluir ciclo/duplicação |
| Painel de etapa inicia o relógio em created_at ou depende de browser | [Cobertura temporal e visitas](analytics/stage-time-and-sla.md) |
| Modelo local continua enviando documentos para parser/embedding remoto | [Fluxo de dados do agente externo](ai/external-rag-agents.md) |
| Gerador diz sucesso, mas IDs foram produzidos por mock | [Desenho versus execução do onboarding](strategy/conversation-led-onboarding.md) |
| Widget importa, mas ação falha ao reabrir o cartão | [Callback, lifecycle e pacote](engineering/widgets-and-react.md) |
