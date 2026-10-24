# Módulo: IA nativa da Kommo e agentes de IA

Este módulo reúne uma síntese operacional original da documentação oficial da Kommo consultada em 20/10/2026. Ele cobre o Agente de IA nativo, as ferramentas de IA do CRM, fontes, ações, integrações, ativação, teste, limites e supervisão.

O material não reproduz os artigos integralmente. Use os links do índice no final para consultar a versão oficial atualizada quando a pergunta depender de disponibilidade, planos, limites, nomes de controles ou comportamento recente.

## Como usar esta referência

- Na Kommo Engineer, leia este arquivo para dúvidas sobre configuração, comportamento, desenho ou diagnóstico de recursos nativos de IA.
- Para tarefas focadas em IA nativa, carregue o guia interno [operação de IA](operating-guide.md); este arquivo é a referência detalhada única para o produto, acessível diretamente pela Kommo Engineer.
- Para estado de uma conta, configurações, permissões ou execução técnica, use a [engenharia de contas](../crm/account-engineering.md) como autoridade técnica. Uma proposta de configuração não prova o estado atual da conta.

## Mapa dos recursos de IA

| Recurso | Para que serve | Quem controla o efeito |
| --- | --- | --- |
| Agente de IA | Responde automaticamente a mensagens recebidas e executa apenas ações configuradas, dentro dos canais e etapas ativados. | A configuração e ativação definem o comportamento; pode haver resposta ou alteração de CRM sem revisão humana mensagem a mensagem. |
| Salesbot | Executa uma sequência explícita de etapas, mensagens e regras. O agente de IA pode iniciá-lo como uma ação. | Fluxo determinístico configurado no Salesbot; revisar triggers, interrupções e bots concorrentes. |
| Sugestões de resposta | Prepara uma resposta baseada nas fontes para uma pessoa revisar, editar e enviar. | A pessoa revisa e envia. |
| Sugestões de tarefas | Detecta um compromisso mencionado e propõe uma tarefa. | A pessoa revisa e confirma a criação. |
| Reescritor e Sugestões de IA | Aprimoram um rascunho escrito por uma pessoa. | A pessoa escolhe aplicar e envia. |
| Resumo da conversa | Resume uma conversa individual como nota no lead. | A pessoa aciona e pode excluir a nota. |
| Kommo Copilot | Ajuda a trabalhar com a Kommo e consultar dados do CRM; inclui modos Ajuda, Assistente e Analista. | Varia por modo. Sugestões de dados e ações de CRM precisam de validação humana. |

Não trate esses recursos como equivalentes. O agente é a principal ferramenta de resposta automática a clientes; as sugestões são assistência para um atendente; o Salesbot executa etapas definidas; o Copilot auxilia um usuário dentro do CRM.

## Modelo mental do Agente de IA

O comportamento resulta da combinação de:

1. **Fontes e catálogo de produtos:** fatos que o agente pode usar para responder.
2. **Persona:** papel, tom, idioma, extensão, pausa e diretrizes.
3. **Ações:** condições conversacionais e operações que o agente executa.
4. **Integrações:** dados sincronizados de sistemas conectados, quando configuradas.
5. **Canal, etapa e trigger:** onde novas conversas podem começar com o agente.
6. **Limites, créditos, teste e monitoramento:** quanto pode operar e como observar o resultado.

O agente é orientado a mensagens recebidas. Não deve ser planejado como iniciador de conversas de saída. Ele só pode agir sobre os canais, fontes, produtos e ações habilitados para ele. Sem informação confiável, deve pedir esclarecimento, não responder, ou transferir para uma pessoa conforme o desenho.

## Escolha entre configuração automática e manual

- **Automática:** gera uma primeira configuração a partir da URL do site ou das informações da empresa. É um ponto de partida para revisar e testar, não uma aprovação de fatos, persona ou ações.
- **Manual:** permite começar do zero ou conectar uma integração suportada. É mais adequada quando a empresa já conhece o processo, as fontes oficiais, as regras e as rotas de atendimento.
- Usuários sem perfil de administrador podem, conforme a documentação, gerar e pré-visualizar um agente, mas criação e ativação podem exigir administrador.
- A ativação exige canais conectados e seleção de etapas do pipeline. Confira permissões e disponibilidade no workspace antes de planejar etapas.

## Fontes de conhecimento e produtos

### Tipos de fonte

A documentação atual lista URL, DOC, DOCX, PDF, Texto e reutilização de uma fonte existente. A seção de respostas sugeridas pode ter uma interface de cadastro diferente da aba Fontes do Agente; confirme a tela atual.

- URL: pode incluir uma página ou páginas aninhadas. A documentação informa que uma URL pode abranger até 1.500 páginas, sujeito a acessibilidade. Páginas que exigem login, CAPTCHA ou conteúdo dinâmico podem não ser processadas.
- Arquivos: DOC, DOCX ou PDF, com limite documentado de 45 MB por arquivo.
- Texto: conteúdo inserido diretamente, com nome e idioma.
- Fontes existentes podem ser vinculadas novamente; uma integração pode criar ou sincronizar fontes próprias.
- A documentação indica até 10 fontes em contas de teste e até 100 em planos pagos. Reconfirme esse limite na conta antes de planejar importações.
- O recurso processa conteúdo textual. Imagens ou arquivos anexados ao chat não são uma base de conhecimento do agente.
- Os idiomas em que a Kommo informa melhores resultados incluem inglês, indonésio, português, russo, espanhol e turco. Em outros idiomas, faça teste específico.

### Governança das fontes

- Mantenha um proprietário, versão e data de revisão para cada fonte; separe fatos públicos de instruções internas.
- Use apenas fontes aprovadas para clientes. Remova ou desative conteúdo expirado, promocional ou que não deve ser compartilhado.
- A Kommo usa fontes ativas. Uma fonte adicionada não prova que está ativa, conectada ao agente ou correta.
- O agente de IA responde com base nas fontes e integrações habilitadas; não presuma acesso livre à internet.
- Se faltar informação, defina o caminho esperado: pergunta de esclarecimento, abstenção ou transferência.
- Não use a caixa Mais nem uma condição em linguagem natural para conferir estado determinístico do CRM, como “o lead tem a tag X”. A Kommo alerta que a IA pode interpretar esse tipo de lógica de sistema incorretamente.

### Catálogo e lojas

O agente pode acessar Produtos quando esse recurso está habilitado e o catálogo contém dados úteis. Em integrações de e-commerce, os dados sincronizados são descritos como somente leitura na Kommo: corrigir preço, estoque ou política na plataforma de origem e sincronizar novamente.

Integrações citadas pela documentação incluem Shopify, WooCommerce, Nuvemshop e Lazada. Confira se o conector está instalado, autorizado, sincronizado e vinculado ao agente correto. Não inferir disponibilidade ou estoque a partir de uma fonte antiga.

## Persona

Os controles documentados incluem:

- **Função e personalidade:** objetivo e papel do agente. A documentação indica até 1.500 caracteres.
- **Tom:** casual, amigável ou formal, conforme a interface atual.
- **Tamanho:** curto, médio ou longo. Os intervalos de caracteres publicados são aproximados; o agente pode adaptar a resposta ao contexto.
- **Idioma:** detecção automática ou escolha manual. A Kommo destaca seis idiomas como os de melhor desempenho.
- **Atraso:** reduz respostas prematuras quando o cliente envia várias mensagens em sequência. O manual consultado indicava padrão de 600 segundos e faixa de 1 a 86.400 segundos.
- **Diretrizes:** documentação consultada indicava até 50 linhas de 300 caracteres cada.

Redija a persona como uma descrição de papel e estilo. Coloque regras de negócio específicas na ação relevante, fatos nas fontes e estados do CRM em automações determinísticas.

## Ações: QUANDO → FAZER → MAIS

Cada ação deve representar um resultado comercial claro. A documentação consultada indicava até 20 ações por agente, até cinco condições QUANDO por ação e até cinco ações FAZER adicionais. Esses limites podem mudar por plano ou atualização; verificar a UI e a documentação antes de configurar.

### QUANDO: o contexto que inicia a ação

Categorias de condição documentadas:

- O que o cliente deseja: comprar, obter suporte, solicitar reembolso, falar com uma pessoa ou uma opção personalizada.
- Sobre o que pergunta: disponibilidade, entrega, preço, política de reembolso, pedido, solução de problemas ou texto personalizado.
- Sentimento: frustrado, confuso, feliz, neutro, triste ou uma opção personalizada.
- Informação fornecida: e-mail, telefone, nome, endereço ou opção personalizada.
- Conteúdo da mensagem: saudação, palavrão, URL/link ou opção personalizada.
- Primeira vez processando uma mensagem do cliente.
- Horário específico ou horário comercial.
- Ausência de resposta por um período configurado. A documentação consultada descrevia um limite de até 24 horas em chats ativos e uma faixa de 1 minuto a 23h59; disponibilidade depende do plano e da janela do canal.

É possível escolher se **qualquer** condição basta (OR) ou se **todas** devem ocorrer (AND). Registre exemplos positivos e negativos para validar a combinação. Condições em linguagem natural são interpretadas pela IA e podem falhar; não equivalem a filtros exatos de campo, tag, proprietário ou etapa.

### FAZER: resposta e operações

A configuração combina uma resposta ao cliente com ações adicionais. Entre as opções documentadas há respostas em texto e uma opção explícita para não responder; confirme como a escolha aparece na interface atual. Outras opções incluem:

- Transferir para usuário.
- Usar uma mensagem fixa, responder com uma informação específica, falar sempre sobre um assunto ou tentar abordá-lo.
- Responder usando uma fonte de conhecimento.
- Solicitar informação ao cliente ou não mencionar um assunto.
- Adicionar tarefa, definir campo ou gerenciar tags.
- Criar compromisso no Calendário.
- Iniciar um Salesbot.
- Mudar etapa do lead ou alterar o usuário responsável.
- Enviar arquivo ou não responder.

Nem todas as ações aparecem em todos os planos, canais ou contas. Ações como definir campo e gerenciar tags foram listadas como dependentes de plano Avançado ou superior; confirme cada capacidade no plano e workspace ativos.

A Kommo descreve a sequência FAZER como ordenada logicamente: se a ação solicita uma informação e depois agradece por ela, o agente pode aguardar a resposta antes de agradecer. Isso não substitui teste de casos incompletos, mensagens ambíguas e clientes que mudam de assunto.

### MAIS: instrução contextual

Use MAIS para orientar uma ação em linguagem natural: quais detalhes perguntar, quando pedir esclarecimento e em quais circunstâncias prosseguir. Mantenha a instrução curta e específica. Não use MAIS para lógica de acesso, condições de campo, idempotência, exclusões exatas ou regras de precedência entre automações.

## Padrões de processo

### Qualificação de lead

1. Dê boas-vindas somente quando uma mensagem recebida iniciar o atendimento.
2. Pergunte a necessidade e colete um conjunto mínimo de dados realmente útil.
3. Use fonte aprovada para explicar produto, preço, disponibilidade e política.
4. Salve dados somente em campos verificados e defina o que fazer se estiverem ausentes ou divergentes.
5. Transfira para a equipe quando o lead pedir uma pessoa, a intenção for sensível, as fontes forem insuficientes ou a ação não puder ser executada.

Peça apenas dados que sejam necessários à próxima etapa; evite repetição quando a conversa ou o CRM já contiverem a resposta.

### Suporte ao cliente

- Mantenha artigos de FAQ, entrega, garantia, devolução, pagamentos e solução de problemas atualizados.
- Separe perguntas respondíveis por fonte de casos que exigem consulta de pedido ou intervenção humana.
- Defina transferência explícita para reclamações, exceções, reembolsos não padronizados e falhas de fonte.
- Não prometa status de pedido em tempo real sem integração conectada e sincronizada.

### Fora do horário

- Configure horários e fuso usados pela empresa; valide a virada de dia e finais de semana.
- Dentro do horário, responda com fontes aprovadas; fora do horário, informe a expectativa e colete somente dados necessários para acompanhamento.
- Defina tarefa, prazo, responsável e tag apenas se o modelo de dados e a fila de atendimento estiverem verificados.
- Planeje como o agente para de responder quando a equipe assume. Uma tag sozinha não prova que outra automação será interrompida.

### Agendamento

Para compromissos no Calendário da Kommo, configure primeiro tipos de serviço, duração, disponibilidade e responsáveis. Depois, crie uma ação QUANDO apropriada e FAZER “Criar agendamento no Calendário”, limitando quais serviços podem ser marcados. Informações comerciais como preço, descrição, preparação e cancelamento podem estar em uma fonte; essa fonte não habilita por si só um serviço a ser agendado.

A documentação de agendamentos também descreve consulta, reagendamento e cancelamento pela conversa, limites de persistência de contexto e encerramento após tentativas fora do assunto. Valide esses limites ao vivo antes de prometer um fluxo. Google Calendar Appointment Schedules é outro caminho de integração, descrito em uma página própria; não misture esse link com o Calendário nativo sem confirmar a arquitetura pretendida.

## Pipeline, ativação e transferência

- Um trigger “Iniciar agente de IA” em uma etapa e canais escolhidos inicia o atendimento de novas conversas. Uma etapa só inicia um agente para novas conversas naquele estágio.
- Agentes diferentes podem atender novas conversas em etapas diferentes.
- Mover o lead pode afetar conversas novas e existentes de forma distinta: as existentes podem continuar com o agente anterior; confira a regra atual antes de desenhar a troca de owner ou agente.
- A Kommo documenta o trigger “Parar agente de IA” para interromper um agente específico quando o lead entra numa etapa. Confirme quais conversas e agentes são afetados antes de usar.
- Transferência ao atendente, encerramento do chat e desativação do agente têm semânticas diferentes. Defina o ponto de transferência, responsável, alerta, contexto compartilhado e condição de parada.
- O material de uso consultado indicava uma espera de cinco minutos depois que um chat era encerrado antes de iniciar nova conversa. Trate isso como comportamento versionado, não como contrato permanente.
- Se o agente iniciar Salesbot, audite o grafo completo do bot, os demais triggers e a tomada de controle. Use [../automation/native-automation.md](../automation/native-automation.md) para projetar a fronteira Agente de IA/Salesbot.

## Voz, teste e lançamento

### Mensagens de voz

A documentação consultada listava mensagens de voz do agente como recurso do plano Pro. O agente transcreve o áudio, aplica fontes, ações e persona e responde em texto. A mensagem original, transcrição e resposta ficam disponíveis na Kommo. Se a transcrição falhar, o fluxo pode pedir ao cliente que envie texto e sinalizar erro para revisão. Confirme plano, canal, idioma, tratamento de erro e controles atuais.

### Modo de teste

O modo de teste ajuda a revisar as respostas com as fontes e instruções configuradas, mas não executa as automações nem prova transferências no canal real. A prévia consome créditos de IA.

Use exemplos para:

- Casos esperados e mensagens que quase correspondem à condição.
- Falta, conflito ou desatualização de uma fonte.
- Pedido para falar com uma pessoa.
- Nome, telefone e e-mail ausentes, já existentes ou corrigidos.
- Mudança de assunto, mensagens repetidas, clientes que enviam várias mensagens e horário fora de expediente.
- Ações que escrevem campo, tag ou tarefa e ações que iniciam Salesbot.

Revise a intenção reconhecida, ações concluídas ou agendadas, fontes utilizadas, lacunas de conhecimento e custo por resposta. Salve mudanças antes de testar novamente. Faça homologação controlada de integrações e efeitos reais antes de ativar amplo.

### Critério de ativação

Antes de lançamento, confirme por evidência: fonte ativa e atualizada; produtos e integrações sincronizados; canais e etapa corretos; permissões; triggers que se sobrepõem; disponibilidade de responsável humano; comportamento ao exceder limite; saldo de créditos; exemplos negativos; plano de interrupção e reversão.

## Limites, créditos e observabilidade

- Créditos de IA são compartilhados entre ferramentas como agente, Copilot, resumo, reescrita e sugestões. O uso é repartido pela conta/workspace.
- Os créditos são renovados no ciclo de faturamento e os não usados podem expirar. A documentação distingue limite de crédito, créditos extras e limites mensais separados para perguntas do Copilot sobre a própria Kommo.
- Créditos extras elevam o saldo de uso, mas não necessariamente habilitam recursos que o plano não inclui.
- Os limites de mensagens e créditos por conversa são configurados por agente. Ao atingir o limite, o agente deixa de responder e pode transferir conforme as opções configuradas. Como o consumo é contabilizado após a resposta, pode ultrapassar ligeiramente o limite configurado.
- Número total e simultâneo de agentes, créditos por plano, disponibilidade por canal e recursos dependem da assinatura e mudam com o produto. Artigos oficiais consultados apresentavam datas e condições de planos diferentes; não embutir números de plano como regra permanente. Consultar cobrança, limites e permissões do workspace na data de implementação.
- Admins podem revisar créditos em Configurações/Faturamento; o Registro de atividades permite investigar consumo e ações. A linha do tempo do lead ajuda a inspecionar qual agente respondeu e o custo registrado.
- O Painel por agente apresenta atividade por período, canal, transferências, perguntas sem resposta, tempo de resposta e consumo por tipo de mensagem. Compare as métricas com uma baseline local e trate lacunas ou resultados sem fonte como filas de trabalho.

## Outras ferramentas de IA

### Sugestões de resposta

Usa mensagem recebida e fontes ativas para propor uma resposta. Pode sugerir automaticamente ou ser acionada numa mensagem específica. Se não encontrar informação relevante, pode não gerar resposta. A pessoa inclui o texto como rascunho, revisa, edita e envia. A documentação limita o processamento de uma mensagem a 25.000 caracteres.

### Reescritor de texto e sugestões enquanto digita

- O Reescritor aplica uma transformação escolhida, como corrigir, profissionalizar, tornar amigável, criativo, mais longo, curto ou simples. A alteração ocorre no rascunho e pode ser desfeita.
- Sugestões de IA aparecem durante a digitação para gramática, ortografia, tom, linguagem inadequada ou encurtamento. A documentação consultada citava limite de 1.800 caracteres para várias sugestões e botão de encurtamento em torno de 3.000; confirme os limites atuais. Nada deve ser enviado sem ação humana.

### Resumo da conversa

A pessoa aciona o resumo no menu de ferramentas de chat; a Kommo adiciona uma nota à conversa individual. Não interpretar como resumo automático de todos os chats do lead. A documentação consultada mencionava busca de resumos no plano Empresarial.

### Sugestões de tarefas

A ferramenta detecta ações mencionadas em mensagens de texto e sugere rascunhos com assunto, prazo, tipo e responsável (normalmente quem selecionou a sugestão). Uma pessoa confirma a tarefa. Pode não sugerir se já existem tarefas ativas ou se a mensagem contém uma pergunta que prioriza uma resposta sugerida. Não considera informações gerais do lead para inferir fatos que não estão na mensagem.

### Kommo Copilot

- **Ajuda:** responde dúvidas sobre a Kommo usando a documentação do produto.
- **Assistente:** trabalha com conversas, resumos e dados do lead segundo o contexto e as permissões do usuário.
- **Analista:** consulta dados da workspace para perguntas de negócio e pode produzir tabelas ou gráficos.
- Sugestões de valores de campos não devem ser tratadas como fatos confirmados; revisar e confirmar antes de gravar.
- **Proteção de dados:** a documentação consultada afirma que o modo Analista usa dados da workspace independentemente das permissões individuais; outros modos seguem permissões do usuário. Isso exige validação de autorização, finalidade e audiência antes de uso analítico. A disponibilidade do modo e de recursos varia por plano.

## Power-up de IA legado

O Power-up/Ativação de IA associado a Salesbot é descrito pela Kommo como recurso legado, acessível apenas em contas que o ativaram anteriormente. Ele não é a mesma coisa que o Agente de IA atual. Se aparecer na conta, identifique-o pelo recurso e histórico; não proponha configurar um Power-up em uma conta nova sem confirmar que ele existe.

## Critérios de arquitetura e segurança

1. Use agente de IA para interpretação de linguagem e conversação baseada em fontes; use Salesbot ou automação da pipeline para condições exatas de CRM e sequência repetível.
2. Separe respostas automáticas de sugestões sujeitas a confirmação humana.
3. Defina explicitamente os fatos permitidos, o que fazer quando faltar conhecimento e o caminho de transferência.
4. Antes de escrever dados, confira o campo, a semântica, permissões, duplicidade, retries e preservação de valores existentes.
5. Evite dois agentes, Salesbots e regras de pipeline respondendo ao mesmo evento. Prove exclusão mútua e regra de parada.
6. Meça resolução, transferência, lacunas, demora, qualidade, erros de gravação, gasto de créditos e reabertura de conversa. Não use volume de respostas como medida suficiente de sucesso.
7. Para decisões que mudam estado ou contactam clientes, siga a proposta e o regra de autorização da Kommo Engineer e confirme a autorização específica do usuário.

## Índice de documentação oficial consultada

Os links são fontes da Kommo, não conteúdo embarcado. As páginas abaixo foram localizadas em português brasileiro em 20/10/2026. Alguns endereços de categoria ou integração usam a rota atual em resources/docs; links e slugs podem mudar.

### Kommo AI e ferramentas

- [Kommo AI — categoria enviada pelo usuário](https://support.kommo.com/docs/pt-br/kommo-ai)
- [Visão geral da Kommo IA](https://support.kommo.com/docs/pt-br/kommo-ai-overview)
- [Limites de IA da Kommo e créditos compartilhados](https://support.kommo.com/docs/pt-br/ai-agent-packages)
- [Comprar créditos de IA](https://support.kommo.com/docs/pt-br/ai-agent-packages-purchase)
- [Reescritor de texto IA](https://support.kommo.com/docs/pt-br/ai-rewriter)
- [Sugestões de IA enquanto digita](https://support.kommo.com/docs/pt-br/ai-suggestions)
- [Respostas sugeridas por IA](https://support.kommo.com/docs/pt-br/work-with-ai-suggestions)
- [Adicionar e gerenciar fontes de conhecimento](https://support.kommo.com/docs/pt-br/add-and-manage-ai-knowledge-sources)
- [Resumo da conversa](https://support.kommo.com/docs/pt-br/conversation-summary)
- [Sugestões de tarefas](https://support.kommo.com/docs/pt-br/task-suggestions)
- [Visão geral do Kommo Copilot](https://support.kommo.com/docs/pt-br/set-up-and-use-kommo-copilot)
- [Usar o Copilot para gerenciar informações de leads](https://support.kommo.com/docs/pt-br/copilot-ai-use)
- [Visão geral do modo Analista do Copilot](https://support.kommo.com/docs/pt-br/analyst-mode-overview)
- [Usar o modo Analista](https://support.kommo.com/docs/pt-br/analyst-mode-usage)

### Agente de IA — categoria com 11 artigos

- [Categoria Agente de IA enviada pelo usuário](https://support.kommo.com/resources/docs/pt-br/ai-agent-1)
- [Visão geral do Agente de IA da Kommo](https://support.kommo.com/docs/pt-br/kommo-agente-ia)
- [Criar um agente automaticamente](https://support.kommo.com/docs/pt-br/ai-agent-automatic-setup)
- [Configurar agentes de IA manualmente](https://support.kommo.com/docs/pt-br/ai-agent-manual-setup)
- [Testar agentes de IA](https://support.kommo.com/docs/pt-br/ai-agent-testing)
- [Gerenciar agentes de IA](https://support.kommo.com/docs/pt-br/ai-agent-usage)
- [Qualificar leads com o agente de IA](https://support.kommo.com/docs/pt-br/ai-agent-lead-qualification)
- [Atender clientes com o agente de IA](https://support.kommo.com/docs/pt-br/ai-agent-assist)
- [Gerenciar conversas fora do horário](https://support.kommo.com/docs/pt-br/after-hours-conversations-ai)
- [Automatizar agendamentos com o agente de IA](https://support.kommo.com/docs/pt-br/ai-agent-bookings)
- [Usar agentes de IA no pipeline, voz e painel](https://support.kommo.com/docs/pt-br/work-with-ai-agents)
- [Limites do agente de IA](https://support.kommo.com/resources/docs/pt-br/understand-limits-ai-agents)

### Limites, planos e integrações relacionadas

- [Limites dos planos](https://support.kommo.com/docs/pt-br/plans-limits)
- [Conectar Shopify à Kommo](https://support.kommo.com/resources/docs/pt-br/connect-shopify-to-kommo)
- [Conectar WooCommerce à Kommo](https://support.kommo.com/resources/docs/pt-br/connect-woocommerce-to-kommo)
- [Conectar Lazada à Kommo](https://support.kommo.com/resources/docs/pt-br/connect-lazada-with-kommo)
- [Conectar Nuvemshop à Kommo](https://support.kommo.com/resources/docs/pt-br/connect-nuvemshoptiendanube-to-kommo)
- [Integrar Google Calendar com o agente de IA](https://support.kommo.com/docs/pt-br/google-calendar-ai-agent)
- [Power-up/Ativação de IA legado](https://support.kommo.com/docs/pt-br/ai-power-up)
- [Índice oficial geral de documentação para LLMs](https://support.kommo.com/llms.txt)

## Referências internas

- [Guia de arquitetura entre Agente de IA e Salesbot](../automation/native-automation.md)
- [Controle, aprovação, piloto e reversão](../automation/governance.md)
- [Handoff técnico para Kommo](../strategy/execution-contract.md)


## Fronteira com agentes externos

Quando o usuário pedir backend próprio, modelo local/nuvem, memória persistente ou recuperação vetorial, consulte [agentes externos e RAG](external-rag-agents.md). Os componentes desse desenho não pertencem automaticamente ao Agente de IA nativo Kommo. Compare custo, manutenção, privacidade, ferramentas e controle de envio antes de escolher; não exija instalar uma stack externa para usar as funções nativas.
