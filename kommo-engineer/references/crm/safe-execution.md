# Implementação, validação e recuperação

## Converter intenção em execução

Antes de mudar a conta, ter resultado, conta alvo, objetos/IDs, operação, dependências, limite e aceite claros. Aproveite a autorização já dada; só peça esclarecimento se uma lacuna material impedir escolher/agir. Não transforme pedido de recomendação em implantação.

Mudança simples/reversível pode ser executada com inspeção e leitura posterior proporcionais. Para mudança estrutural, lote, migração ou comunicação, tornar o impacto concreto e revisável antes da execução; apresentar o diff quando aplicável. Exclusão, envio, ativação e outras consequências precisam estar cobertos pela instrução humana. Não usar escopo/allowlist genérica para contornar restrição específica do projeto.

Plano de lote útil:

`account_id + subdomain | objetivo | operações e IDs | antes/depois | precondições/hash | consumidores | autorização | limites | recuperação | aceite`

Configuração proposta não é payload executável. Verifique método, endpoint, schema, entidade, tipo/enums, paginação, permissões e efeitos pela fonte atual. Reutilize cliente/executor existente e seu tratamento de erro. Não improvise rota interna por engenharia reversa quando falta operação suportada.

## Sequência para lote de impacto

1. Capturar baseline com dados necessários à recuperação e declarar a cobertura. Snapshot de metadados não recupera valores, histórico ou mensagens.
2. Gerar plano/diff por conta, IDs e operação; preservar versão/hash revisados. Guardar dados pessoais em área privada, evidência saneada no projeto.
3. Conferir autorização vigente, conta e precondições imediatamente antes de aplicar. Divergência pausa a operação afetada; não ajustar plano aprovado silenciosamente.
4. Executar pequeno lote/piloto por executor adequado, com exclusão mútua quando houver risco de corrida e journal por operação/chave.
5. Ler o objeto de volta, reconciliar antes/depois e testar o consumidor/efeito relevante. Expandir apenas o escopo autorizado depois que o piloto passar.
6. Registrar aplicado, comprovado, falha parcial e pendência, com próxima ação. Não reaplicar automaticamente operações já confirmadas.

Rollback só pode ser prometido quando o caminho foi definido e é viável. Escrita compensatória não apaga mensagem enviada, restaura ID removido ou desfaz automaticamente efeitos em integrações.

## Cliente e falhas de API

- HTTPS no host exato da conta, token no header, sem seguir redirect com credencial. Hosts de outras APIs só quando o contrato documentado exigir.
- Cliente com allowlist de método/rota e configuração separada por conta. Validar status/content type/schema antes de interpretar corpo. Registrar cobertura de paginação; não declarar leitura completa com página faltante.
- 400/422: corrigir payload/contrato; não repetir inalterado. 401: parar acesso e resolver credencial. 403: verificar recurso/permissão/bloqueio. 429: reduzir taxa e backoff limitado com jitter, conforme resposta/documentação.
- 5xx/timeout: leitura idempotente admite retry limitado; escrita exige reconciliação por chave/journal antes da repetição. Não assumir suporte a header de idempotência inexistente.
- Resposta de erro pode conter PII/segredo: sanear antes de log/exibição. Journal privado guarda evidência necessária; saída pública traz contagem, código, objeto e referência segura.
- Revalidar limites oficiais e coordenar carga de outros consumidores. Os limites publicados não são meta de throughput nem quota reservada ao agente.

## Testes que provam o pedido

Escolher casos pelo que mudou: tipos/enums/vínculos, condição de entrada/saída, evento duplicado, falha parcial, permissão ausente, timeout e interrupção humana. Use fixtures locais com dados sintéticos para lógica; prova live controlada para persistência e entrega. Não crie registros reais de teste ou envie mensagens sem escopo apropriado.

Exemplos de aceite:

- Campo/grupo: leitura posterior e reabertura quando a alteração afeta UI, IDs/valores preservados e consumidor testado.
- Importação: contagem reconciliada, vínculos, retorno de IDs, exceções separadas e retry sem duplicação.
- Bot: gatilho real, ramo correto, parada/handoff e tarefa/entrega observados; preview apenas valida uma parte.
- Formulário: envio chega à oportunidade correta e mantém respostas completas; frontend salvo não basta.
- Recomendação: evidência/cobertura, decisão e forma de medir; não exige criar dados ou implantar para ser concluída.

## Troubleshooting por evidência

Rastrear em ordem do sintoma: conta/acesso → dado/vínculo → evento/gatilho → regra/bot → integração/fila → canal/provedor. Investigar apenas camadas pertinentes. Registrar fatos e hipóteses separadamente e escolher o próximo teste que as distingue.

| Sintoma | Evidência que costuma distinguir a causa |
|---|---|
| Lead ausente | Recebimento do evento, rejeição de schema, dedupe, fila e resposta API |
| Lead/tarefa duplicado | Chave/evento, retries, concorrência e automações sobrepostas |
| Campo não alterou | Entidade/ID/tipo/enum, resposta API e sobrescrita por outro consumidor |
| Bot não iniciou | Gatilho ocorrido, condições/estado, canal, publicação e execução |
| Mensagem não chegou | Destino, resposta/provedor, regra/template e status de entrega |
| 429 recorrente | Requisições por consumidor, N+1, paginação/cache e retries |

Em incidente, conter somente o componente afetado no escopo autorizado, preservar evidência, estimar alcance, corrigir e reconciliar/reprocessar sem duplicar. Não desligar todas as automações por conveniência. Após duas tentativas significativas sem progresso, parar essa operação e informar causa, evidência e próximo passo necessário.
