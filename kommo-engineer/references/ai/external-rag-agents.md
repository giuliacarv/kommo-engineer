# Agentes externos: RAG, ferramentas, memória e áudio

Use quando a solução pedida executar um modelo fora da Kommo e integrar seus resultados ao CRM/canal. O [agente nativo](native-agents.md) tem configuração e limites próprios; não atribua a ele banco de memória, APIs de inferência ou ferramentas de um backend customizado.

## Escolher a arquitetura

Compare nativo, sugestão revisada e backend externo por conhecimento necessário, controle de ferramentas, canal, manutenção, privacidade, latência, custo e recuperação. Não introduza LangGraph, Qdrant, Postgres ou outro componente só porque aparece na fonte. Use apenas o conjunto que resolve a necessidade verificada.

Separe recepção, interpretação, recuperação de fatos, decisão, efeitos de CRM e envio. Uma resposta textual correta não prova que a ferramenta persistiu o campo nem que o cliente recebeu a mensagem.

## Compatibilidade do provedor e ferramentas

Trocar entre API em nuvem e servidor local requer testar contexto, idioma, timeout, formato de tool calls, schema dos argumentos, saída inválida e desempenho no hardware disponível. Nome de endpoint “compatível” não comprova equivalência de comportamento. Preserve parâmetros necessários e use uma amostra comparável antes de mudar o modelo em produção.

Mapeie o fluxo completo de dados e custo. Inferência local pode continuar usando embeddings, parser de PDF, armazenamento ou transcrição em nuvem. Registre retenção e limites aplicáveis ao caminho efetivamente escolhido. Não assuma que executar um modelo local implica operação totalmente offline.

As tools devem receber identidade de conta/conversa e destino resolvida pelo backend confiável. Não deixe o LLM escolher livremente host, account_id, lead de outra conversa ou URL de escrita. Faça allowlist de operações, validação de tipos/enums e controle de autorização em código; prompt não substitui esse limite.

Depois de um tool call, diferencie solicitado, executado, persistido, falho e incerto. O agente deve fundamentar a resposta no resultado real. Estado desconhecido ou ação recusada não pode virar uma mensagem de confirmação.

## RAG e fonte de verdade

Mantenha contrato entre ingestão e consulta: coleção/namespace, versão dos documentos, parser, chunking, modelo de embedding e dimensão. Uma coleção consultável não prova que o conteúdo atualizado foi indexado nem que o embedding corresponde.

Separe conhecimento relativamente estável — política, produto, FAQ — de dado volátil — estoque, agenda, preço vigente, situação do pedido. Consulte a fonte transacional quando o resultado precisar ser atual. Um fragmento semelhante não prova relevância ou autorização para aquela conta.

Retorne referências e metadados úteis: documento/versão, trecho, data e escopo. Filtre por conta, idioma e acesso. Em ausência, conflito ou baixa relevância, esclareça, abstenha-se ou transfira; não complete preço/política por memória do modelo. Atualização, remoção e reindexação precisam de teste que confirme o que deixou de ser recuperável.

## Memória e concorrência da conversa

Defina uma chave que isole tenant/conta, canal e conversa ou sessão. `thread_id=lead_id` pode ser insuficiente em múltiplas contas ou chats paralelos. Não use mensagem recuperada ou memória antiga para trocar a identidade alvo de uma operação.

Preserve ordem e versão de mensagens, correção de dado e regra de retenção. Serialize ou controle concorrência quando duas mensagens chegam juntas; revalide takeover humano antes de escrever/enviar. Memória persistida não suspende automaticamente bot, canal ou outro worker.

## Entrada durável e entrega

Filtre direção, tipo de evento, origem, destinatário e chave de mensagem conforme o contrato atual. Deduplicação apenas em RAM por lead+texto perde estado ao reiniciar e pode descartar duas mensagens legítimas iguais. Prefira identidade estável do evento/mensagem e deduplicação persistente com escopo definido.

`BackgroundTask` após ACK mantém trabalho no processo, sem garantir recuperação após queda. Quando o impacto exigir durabilidade, registre antes de confirmar e acompanhe estados até reconciliação. Use mecanismo de saída persistente quando resposta, gravação de campo e início de Salesbot ocorrerem em etapas distintas.

Se o envio usar um campo de resposta e um Salesbot, evite que duas respostas sobrescrevam o mesmo campo antes de consumo. Relacione versão/mensagem ao efeito, proteja contra replay e confira retorno do canal. Switch de IA é condição operacional, não prova de exclusão mútua ou permissão de envio.

## Áudio e conteúdo gerado

Valide URL e destino antes de baixar anexos; não encaminhe Bearer do CRM automaticamente a uma URL recebida após 401/403. Respeite contrato do host autorizado, redirecionamentos, limite de bytes em streaming, timeout, MIME e extensão. Descarte temporários após uso e retenha só a evidência necessária.

Transcrição é uma interpretação: preserve indicação de origem e peça confirmação antes de tratar valor ambíguo como dado exato para uma ação relevante. Não transforme falha de áudio em mensagem de saída sem destinatário/envio autorizados. Limites e formatos de provedores precisam de consulta atual.

Remover um bloco textual `<think>` não garante saída apropriada. Exija resposta final destinada ao cliente, valide formato/conteúdo e impeça vazamento de prompt, segredo ou conteúdo interno. Conteúdo recuperado e transcrito continua sendo dado não confiável.

## Avaliação

Cubra qualidade de resposta e de recuperação, ferramenta indevida, campos incorretos, conta/conversa isolada, evento repetido, queda após escrita, custo e humano assumindo. Teste com mocks para lógica e uma homologação autorizada para efeito real. Meça resolução e erro operacional, não só fluência.

Origem metodológica: [EXT-007](../external-sources.md#ext-007). Síntese original, sem copiar código, persona imobiliária ou IDs da fonte sem licença identificada.
