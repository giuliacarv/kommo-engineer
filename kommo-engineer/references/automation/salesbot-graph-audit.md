# Auditoria de Salesbots por grafo e dependências

Use para revisar automações existentes, conflito entre bots, importação de um fluxo ou falha que depende de vários caminhos. Aprofunda [playbooks de Salesbot](salesbot-playbooks-and-api.md), [automação nativa](native-automation.md) e [execução](../crm/safe-execution.md).

## Identificar o material antes de validar

Registre conta, versão/data, bot e formato observado: exportação do editor, JSON codificado, metadados de API ou diagrama. Identifique como passos, conexões, condições, erro e fim são representados nessa versão. O formato `model.text`, `_start`, `_stop` de um projeto não é schema universal de Salesbot.

Colete por meios autorizados: inventário de bots, gatilhos/canais/horários, conteúdo disponível, pipelines, etapas, campos/enums, responsáveis e chamadas entre bots. Marque cobertura parcial quando o mecanismo só fornece metadados. Requisição interna capturada no navegador pode ajudar a entender a UI, sem estabelecer um endpoint suportado de integração.

## Dois grafos que respondem a perguntas diferentes

1. **Dentro do bot:** nós são passos/estados; arestas são transições normais, alternativas, erro, timeout e retomada. Marque entrada, espera, saída, transferência e ação de escrita/envio.
2. **Entre componentes:** bots, triggers, regras de pipeline, agente de IA, canal e serviços externos; arestas representam quem inicia, para, escreve um campo ou provoca evento usado por outro componente.

Conecte grafo e dicionário de dados. Campo aparentemente não usado por um bot pode ser consumido por formulário, integração, relatório ou equipe. Etapa sem bot não é automaticamente erro: pode representar trabalho humano.

## O que procurar

| Verificação | Evidência necessária | Cuidado de interpretação |
|---|---|---|
| Referência inexistente | Destino de passo, campo/enum, etapa, bot e owner resolvidos no snapshot da conta | Nome igual não prova ID ou entidade iguais |
| Caminho inalcançável | Percurso a partir de todas as entradas reais conhecidas | Um playbook pode ter entrada manual/API sem gatilho local |
| Espera sem saída | Evento esperado, timeout, alternativa e interrupção observados | Duração e fallback dependem do processo e canal |
| Ciclo | Caminho que retorna ao mesmo estado e condição de saída/limite | Voltar a um número de passo menor é pista; não prova loop infinito |
| Efeito duplicado | Entradas concorrentes, retries e mesmo registro/ação | Bots diferentes podem atingir o mesmo consumidor por eventos distintos |
| Handoff incompleto | Quem assume, contexto, tarefa/alerta e mecanismo real de parada | Iniciar outro bot ou transferir não prova parada de todos os fluxos |
| Campo alterado incorretamente | Entidade, tipo, enum, valor anterior e próxima regra | Escrita pode disparar outra automação ou ser sobrescrita |
| Envio incompatível | Canal, destinatário, template/regra atual e execução | Handler de mensagem ou espera anterior não demonstra elegibilidade de envio |

Para ciclos relevantes, siga arestas reais e componentes de retorno, incluindo chamadas entre bots e mudanças de etapa que reiniciam gatilhos. Diferencie repetição controlada, espera, reentrada legítima e ciclo sem progresso. Teste o limite no escopo autorizado; não faça uma execução destrutiva para confirmar uma suspeita.

## Evidência e registro do achado

Cada achado precisa de identificador, local no grafo, versão, condição de reprodução, fato observado, interpretação, alcance provável, severidade justificada, correção proposta e aceite. Separe falha certa de recomendação e de informação ausente. Não adote nota global de maturidade ou severidade fixa da fonte sem critério apropriado à conta.

Para acervo grande, pode ser útil manter metadados e raw JSON em armazenamento relacional. Inclua conta, snapshot/versão, IDs nativos, IDs internos de auditoria, origem e extração; preserve enum multivalorado, conexões e gatilhos separadamente. Não confunda chave serial local com ID de bot no CRM. Use armazenamento proporcional; PostgreSQL não é requisito para auditar um bot.

## Validação estática e prova funcional

Um validador estático só prova as regras que implementa para o formato que conhece. O exemplo da fonte trata `goto` para índice anterior como possível loop e usa heurísticas para mensagens; isso não cobre todo o grafo nem valida janela de canal. `PASS` não autoriza ativação.

Prove os caminhos relevantes: elegível, inelegível, alternativa, erro, timeout, repetição e humano assumindo. Leitura posterior comprova configuração; execução controlada comprova transição; status do canal comprova a etapa de envio realmente observada. Documente regras sem cobertura e proponha a menor correção necessária.

Origem metodológica: [EXT-004](../external-sources.md#ext-004). Síntese própria de método e limitações; nenhum validador ou esquema SQL externo foi instalado nem copiado para execução.
