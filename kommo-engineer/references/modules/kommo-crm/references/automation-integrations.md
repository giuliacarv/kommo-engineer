# Automações, canais e engenharia de integração

## Escolha da arquitetura

| Necessidade | Primeira opção a avaliar |
|---|---|
| Regra determinística em etapa/evento | Digital Pipeline/recurso nativo |
| Conversa com caminhos previsíveis | Salesbot |
| Resposta que depende de conhecimento e linguagem | AI Agent com fontes curadas e handoff |
| Orquestração entre sistemas | n8n/Make ou backend, conforme confiabilidade e manutenção |
| Sincronização crítica | Backend com fila durável, idempotência e reconciliação |
| Canal de mensagens próprio | Chats API e requisitos do provedor |
| Interface dentro do Kommo | Widget/Web SDK suportado |

São critérios de desenho, não promessa de disponibilidade no plano/conta. Confirme ferramenta, API e permissão antes de escolher implementação. Automatização adicional precisa de benefício observável, proprietário e recuperação.

## Contrato de qualquer fluxo

Defina evento/entrada, população elegível, condição, exclusões, entidades/IDs, ação, dono, prazo, saída, erro, pausa e prova do efeito. Mapeie outras regras que tocam os mesmos campos/etapas. Alterar o campo que dispara o próprio fluxo pode causar loop; duas regras que criam tarefas podem duplicar a próxima ação.

## Salesbot e Digital Pipeline

- Partir do ramo comercial vigente e do gatilho real; mapear estado atual, resposta, captura de informação, condições e handoff humano. Separar bot, gatilho do pipeline, canal e tarefa posterior.
- Para cada ramo relevante, definir dados obrigatórios naquele momento, timeout, retomada, resposta inesperada, parada após resposta/opt-out e quem assume atendimento.
- Guardar baseline/exportação quando disponível. Não presumir que lista/detalhe API inclui o modelo visual ou que é possível CRUD completo do editor; verificar endpoint atual e cobertura.
- Testar entrada elegível, inelegível, ramo alternativo, repetição do evento, erro de canal/integração e interrupção humana quando afetados. Exportar, salvar ou simular no editor não comprova entrega nem tarefa persistida.
- Ativar somente quando o escopo humano cobrir ativação e os testes necessários estiverem disponíveis. Testes com clientes reais/mensagens precisam de destinatário e envio autorizados.

## Webhooks, n8n, Make e backend

Padrão útil: receber → validar → registrar de forma durável → deduplicar → resolver vínculos → aplicar regra → persistir → verificar → reconciliar. Escolher armazenamento/fila proporcional ao impacto; não exigir infraestrutura distribuída para um fluxo simples.

- Verificar documentação de evento, payload, content type, confirmação, autenticidade e entrega. Não inventar HMAC em um webhook que não o fornece; assinatura de Chats API não é automaticamente assinatura de todo webhook do CRM.
- Tratar duplicação, ordem invertida e replay como condições de projeto quando não houver garantia oficial. Preferir ID de evento do provedor; sem ele, definir fingerprint e limites de colisão. Não colapsar eventos distintos legítimos só por entidade/data.
- ACK rápido só depois de preservar o evento quando houver fila. Restringir destino e validar URL/payload antes de carregar anexos ou executar ações.
- Persistir chave de idempotência e resultado por etapa; timeout de POST pode ter criado o objeto. Buscar resultado/journal antes de retry. HTTP 200 no orquestrador não prova gravação no Kommo.
- Para fluxo crítico: ramo de erro, reprocessamento limitado, fila de falhas/revisão manual, alerta acionável e reconciliação por chave. Evitar retry infinito e N+1; usar filtro, paginação e cache antes de aumentar concorrência.
- Credenciais ficam no armazenamento do integrador/servidor. Workflow exportado deve omitir token, URLs privadas e dados pessoais. Configuração de conta e IDs fica separada do código reutilizável.

## Formulário e vínculo da oportunidade

Mapear pergunta/subcampo → entidade/campo/enum/nota, origem e tratamento de vazio. Definir chave do envio, identificação de pessoa e regra para oportunidade existente versus nova. Não criar um lead novo em todo retry ou vincular apenas pelo nome. Preservar resposta original recuperável; faixa financeira não vira número exato.

Provar o caminho envio → validação → persistência/fila → CRM → vínculos → leitura de volta. Se houver confirmação/sistema consumidor, validar seu efeito. Integração no Git e deploy do frontend não provam migração, segredo, função, gatilho ou entrega ao CRM.

## Chats API, WhatsApp e Instagram

REST CRM, Chats API, add-on de chats e provedor do canal têm contratos diferentes. Verificar host, autenticação/assinatura, identificadores, suporte do canal e permissão da integração específica. Não assumir que token de longa duração do CRM permite enviar por qualquer WhatsApp existente.

Persistir mapa conta/canal externo ↔ conversa/chat ↔ contato/lead; IDs de mensagem, direção, timestamps e status. Separar aceitação HTTP, envio ao provedor, entrega e leitura. Testar duplicação, mídia, reconexão e falhas relevantes. Validar assinaturas/timestamps pelo contrato exato, sem copiar fórmula de outro produto.

Antes de migração/desconexão: identificar dono do número/página/WABA, provedor atual, histórico e dependências. Para WhatsApp/Meta, conferir regras atuais de janela, template, consentimento, opt-out e qualidade diretamente nas fontes oficiais e no estado do provedor. Não aplicar regras históricas ou resolver erro de entrega só pelo cartão do lead.

## IA e widgets

AI Agent: definir finalidade, canais/escopo, fontes, persona, ações permitidas, dados que pode alterar, handoff, horário e orçamento. Curar conhecimento por tema/uso e atualizar com rastreabilidade; não despejar acervo indiscriminado. A API pública de IA documenta operações específicas, não necessariamente todas as configurações do editor. Verificar operação antes de prometer automatizá-la.

Avaliar conversas normais, lacuna de conhecimento, ambiguidade, preço sem fonte, pedido de humano, dado sensível, prompt injection e ação não autorizada. Medir resposta correta, handoff útil, ação indevida e custo por resultado, além de fluência. Separar sugestões de IA de decisões determinísticas de CRM.

Widget: usar SDK/contexto público e lifecycle suportados. Segredo privilegiado pertence ao backend. Testar localização, permissões, navegação/reabertura, descarte de listeners, idioma/tema quando afetados; não depender de endpoint interno ou seletor sem contrato.

## Atribuição e retorno para mídia

Definir evento de negócio (qualificado, ganho, receita), instante real, valor/moeda, origem e IDs de clique/campanha disponíveis. Contratar normalização/consentimento dos dados, deduplicação por identificador estável e reconciliação CRM ↔ plataforma. Não contar contato duplicado como nova conversão nem marcar toda resposta como lead qualificado.

Kommo, Google Ads, Meta Marketing API e Meta CAPI exigem conexões/autorizações próprias. Revalidar versão, janela, elegibilidade e schema nas docs atuais. Envio de conversão/alteração de mídia só integra o escopo quando solicitado; preparar o contrato pode avançar offline.
