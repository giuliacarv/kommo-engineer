# Bots da Kommo: playbooks, gatilhos, JSON e API

Este guia organiza padrões de uso para transformar Salesbots em fluxos reutilizáveis, sem confundir o bot salvo com o gatilho que o executa. A documentação oficial foi consultada em 21/10/2026. Os detalhes de UI, JSON, canais, plano e endpoints podem mudar; valide no workspace e na documentação atual antes de configurar.

## Modelo mental

- **Bot**: sequência reutilizável de mensagens, condições e ações. Pode ser criado no editor visual ou como fluxo codificado.
- **Gatilho**: regra de entrada automática, como evento/etapa do pipeline, horário, comportamento ou conversa. O mesmo bot pode ser ligado a gatilhos diferentes.
- **Execução manual**: um usuário escolhe um bot salvo dentro de uma conversa e inicia o fluxo.
- **Execução por API ou por outro bot**: pode iniciar um Salesbot mesmo sem um gatilho de pipeline configurado.

Portanto, salvar um bot sem gatilho de automação deixa o bot fora dos eventos automáticos associados àquele Salesbot; isso não significa que ele esteja impossível de executar. Ele ainda pode ser iniciado manualmente, por outro bot ou por uma chamada de API autorizada. Separe também o estado `active` do bot da existência de gatilhos: a API pode indicar `active=true` mesmo quando não há gatilho de pipeline associado. Não descreva um bot como “inativo” apenas porque ele não tem gatilho; verifique cada sinal separadamente.

## Escolha do padrão

| Objetivo | Padrão útil | Consequência |
| --- | --- | --- |
| Guardar um fluxo para atendentes usarem quando fizer sentido | Salvar como playbook, sem gatilho automático | O atendente decide quando iniciar; ainda pode haver execução manual/API ou chamada por outro bot. |
| Repetir um processo previsível após um evento do pipeline | Ligar a um gatilho e definir condições, horário, público e etapa | A execução pode enviar mensagens ou alterar registros sem escolha do atendente a cada lead. |
| Dar respostas sobre assuntos descritos em fontes usando linguagem natural | Agente de IA com ação de iniciar Salesbot quando uma regra conversacional válida for atendida | O agente interpreta a conversa; o Salesbot conduz a sequência definida. Auditar os dois lados do handoff. |
| Enviar uma única resposta padrão que o atendente escolhe | Modelo de chat | Modelo de chat não é um fluxo com ramificações e ações de Salesbot. |

Escolha pela necessidade e pelo objetivo comercial. Prefira o playbook manual quando a decisão depende do contexto do atendente; escolha um gatilho quando a regra de ativação for estável, observável e tiver escopo claro.

## Onde criar e como manter a biblioteca

A Kommo documenta caminhos de criação em Configurações → Ferramentas de comunicação → Salesbots e, em algumas áreas, IA e Automação → Bots. O usuário também relata o atalho de interface `/bots`; rótulos e rotas podem variar por versão e conta. A lista permite criar do zero, usar modelos e importar Salesbots. Depois de salvar, a janela de configuração do gatilho pode aparecer; a documentação diz que o gatilho pode ser adicionado depois.

Para montar uma biblioteca reutilizável:

1. Crie o bot visual ou a partir de um modelo aprovado.
2. Se a intenção for uso manual, não associe um gatilho de pipeline ao bot. Confira também se o bot não está referenciado por outro Salesbot, automação, campanha ou chamada de API programada.
3. Use um nome que revele intenção e uso. Convenção opcional: `LIB | atendimento | enviar catálogo | v1` ou `AUTO | qualificação | novo lead | v1`.
4. Registre propósito, responsável, canais compatíveis, dados usados, último teste e se o bot é manual, automático ou auxiliar de outro fluxo.
5. Faça inventário dos gatilhos e das chamadas que iniciam o bot antes de mudar, importar, renomear ou remover uma versão.

Não use apenas um nome como prova de que o bot é manual ou inofensivo. Um bot sem gatilho local ainda pode ser iniciado por outro fluxo ou API. Bots importados podem ter gatilhos, IDs de campos/etapas e integrações ligados à conta de origem; inspecione essas dependências antes de usá-los na conta de destino.

## Iniciar um playbook no chat

A documentação da Kommo para Messenger descreve o fluxo manual: abrir a conversa, digitar `/`, selecionar um bot salvo e clicar em Executar. A sintaxe exata ` /+nome-do-bot ` foi relatada pelo usuário como dica de uso na interface dele; a página oficial consultada documenta o seletor aberto por `/`, sem confirmar o `+` como sintaxe universal. Teste o seletor no canal e na versão de UI que serão usados.

O Salesbot pode compor várias etapas. O passo de mensagem aceita texto/modelos e, conforme canal e configuração, mídia como áudio/voz e arquivos. Não presuma que todos os canais entregam texto, áudio, imagem, vídeo, botões ou modelos da mesma maneira. Verifique as regras vigentes do canal, o formato e tamanho do arquivo e as exigências de template; teste em conversa de homologação antes de acionar um cliente.

Antes de iniciar manualmente, confira o lead/conversa selecionado, o conteúdo final, as ações de CRM, o canal e se o fluxo espera uma resposta do cliente. Iniciar manualmente é uma ação externa real, não apenas abrir uma prévia.

## Editor visual, JSON, importação e exportação

- O editor visual é a opção padrão para sequências que a equipe precisa inspecionar e manter.
- A documentação permite abrir ou editar o código do Salesbot e documenta a estrutura JSON com objetos como `question`, `answer` e `finish`. Ela recomenda validar o JSON e informa limite de 64 KB.
- A documentação de criação confirma importar Salesbots e consultar o código. Ela alerta que, após editar o código, aquele Salesbot pode deixar de abrir no editor visual. Faça uma cópia/versionamento antes de passar para o modo codificado.
- O usuário relata exportação e importação pela interface da conta. A ajuda oficial consultada confirma importação, mas não estabelece todas as regras de exportação, portabilidade entre contas ou round-trip. Confirme os comandos e teste a restauração num ambiente de homologação.
- JSON exportado ou construído pode conter IDs internos, tags, etapas, campos, contas ou configurações de canal. Não assuma que é portátil só porque o arquivo importa; reconcilie dependências e comportamento após importar.
- Não use código de endpoints internos observados na UI como contrato público. O modelo JSON do bot e os endpoints REST da API são superfícies distintas.

## Integrações e API: o que afirmar

Codex, Claude Code, Antigravity, VS Code ou um script podem consumir a API quando o cliente estiver configurado com transporte, rede, autenticação e credencial seguros. Isso não significa que esses produtos tenham uma integração Kommo nativa pronta. Para conectar ou operar a conta, consulte o módulo interno `../crm/account-engineering.md`, que contém o procedimento de identidade, conexão e armazenamento seguro de credenciais.

Na documentação pública da Kommo consultada, os endpoints específicos de Salesbot listados permitem:

- listar Salesbots em `GET /api/v4/bots`;
- obter um Salesbot por ID;
- iniciar um bot para lead/contato autorizado, individualmente ou em lote;
- parar um bot em uma entidade.

O índice oficial consultado não lista endpoints CRUD para criar, editar ou apagar a definição completa do bot/gatilhos. Não prometa que a API REST pública gerencia o editor visual ou aceita JSON arbitrário do Salesbot só porque existem endpoints para listar, iniciar e parar bots. Use a UI/importação/código documentados ou confirme uma superfície oficialmente suportada antes de projetar a gravação. A documentação também afirma que métodos não descritos na referência pública não têm suporte garantido.

A API CRM tem operações próprias para entidades e campos, incluindo métodos documentados para adicionar, atualizar e apagar campos personalizados. Isso não implica que qualquer usuário do Codex tenha permissão para executá-los ou que um token de CRM acesse API de chat, canais ou configurações de automação. Confirme endpoint, escopo, conta e autorização por operação; o módulo `../crm/account-engineering.md` é a autoridade para implementação.

### Tratamento do token

Uma integração privada e um token de longa duração podem viabilizar chamadas ao workspace; a documentação da Kommo alerta que tokens de longa duração são para integrações privadas e operam com direitos administrativos. OAuth 2.0 oferece escopos de acesso autorizados. A credencial deve ser provisionada em cofre/ambiente local do processo cliente, fora de prompt, chat, JSON versionado, código, log e pasta sincronizada. Não solicite nem reproduza o valor do token. Para setup, identidade, privilégio e armazenamento, siga a referência interna de [conexão](../crm/connection.md).

## Fluxo de trabalho para desenhar um bot

1. Defina resultado, público, canal, contexto de início, dono e desfecho esperado.
2. Escolha se será playbook manual, automação por gatilho ou subfluxo chamado por agente/outro Salesbot.
3. Leia o bot e os gatilhos existentes. Mapeie colisões, loops, dupla resposta, campos alterados, tarefa duplicada e interrupção humana.
4. Escreva os ramos: entrada, mensagem, condição, coleta de dados, validação, erro/timeout, handoff e parada.
5. Para a biblioteca manual, salve sem gatilho automático e verifique referências externas. Para automação, conecte somente os gatilhos, canais, etapas e condições aprovados.
6. Se usar JSON, compare com a estrutura e os limites oficiais, valide IDs de conta/campo/etapa e mantenha uma versão recuperável.
7. Homologue em lead/conversa de teste; leia de volta o bot, gatilhos, dados alterados, mensagens e logs. A resposta HTTP de iniciar uma tarefa não prova que todas as mensagens foram entregues.
8. Ative no público pretendido só depois de testar elegíveis, não elegíveis, mensagens repetidas, respostas inesperadas, falha de canal e parada/transferência.

Qualquer alteração real continua sujeita à autorização para a conta e para o efeito específico. Um pedido para criar a biblioteca não autoriza anexar gatilhos, disparar mensagens ou modificar registros de clientes.

## Fontes oficiais consultadas

### Ajuda da Kommo

- [Criar um Salesbot](https://support.kommo.com/docs/pt-br/create-a-salesbot-in-kommo)
- [Configurar gatilhos do Salesbot](https://support.kommo.com/docs/pt-br/configure-your-salesbot-triggers)
- [Gatilhos do Funil de Vendas Digital](https://support.kommo.com/docs/pt-br/set-up-digital-pipeline-triggers)
- [Iniciar manualmente um bot em um chat — guia de Messenger](https://support.kommo.com/resources/docs/pt-br/personalizar-mensagens-facebook)
- [Modelos de Salesbot](https://support.kommo.com/docs/pt-br/use-salesbot-templates)
- [Visão geral e etapas do Salesbot](https://support.kommo.com/docs/pt-br/salesbot-overview)
- [Enviar mensagens de voz via Salesbot](https://support.kommo.com/docs/pt-br/send-voice-messages-via-salesbot)
- [Arquivos disponíveis para canais e bots](https://developers.kommo.com/reference/files-api)

### Documentação de desenvolvedor da Kommo

- [Salesbot e formato do JSON](https://developers.kommo.com/docs/salesbot-dp)
- [Índice da API REST — endpoints de Salesbot](https://developers.kommo.com/reference/salesbots-list)
- [Iniciar um Salesbot](https://developers.kommo.com/reference/launch-a-salesbot)
- [Parar um Salesbot](https://developers.kommo.com/reference/stop-salesbot)
- [API de campos personalizados](https://developers.kommo.com/reference/custom-fields)
- [Sobre a API Kommo e métodos oficialmente suportados](https://developers.kommo.com/reference/kommo-api-reference)
- [Integração privada](https://developers.kommo.com/docs/private-integration)
- [Token de longa duração](https://developers.kommo.com/docs/long-lived-token)
- [OAuth 2.0](https://developers.kommo.com/docs/oauth-20)

## Referências internas

- [Arquitetura entre Agente de IA e Salesbot](native-automation.md)
- [Detalhes do agente de IA e ferramentas Kommo](../ai/native-agents.md)
- Para execução da conta e autenticação, use o módulo técnico integrado `../crm/account-engineering.md`.


## Auditoria de fluxo existente

Quando o problema depender de ramificações ou várias automações, use a [auditoria por grafo](salesbot-graph-audit.md). Analise entradas reais, passos, alternativas, timeout, chamadas entre bots e consumidores dos campos. Um `goto` para passo anterior é uma pista de ciclo; a comprovação exige caminho e condição de saída. Um validador que passa não autoriza ativação nem comprova política do canal.
