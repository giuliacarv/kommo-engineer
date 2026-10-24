# Receitas e simulação de Salesbot

`salesbot spec --project PATH --recipe triage|qualification|followup|instagram|manual|ai-handoff|seller-macro --channel CANAL --output desenho.json` gera um **desenho não importável**. IDs locais N01 não são handlers Kommo. O arquivo inclui saídas esperadas, falhas e preflight; activation_enabled permanece false. Não há endpoint inventado para publicar definições completas.

Para converter em configuração: resolva IDs e entidade na conta, confirme o contrato específico do editor/versão e canal, preserve export anterior, desenhe cada ramo e valide em contato controlado. Trocar visual/código pode perder editabilidade: backup e cópia inativa antes. Bot manual sem gatilho pode ainda ser iniciado via API/outro bot quando suportado; escolha por / exige teste na interface/canal. Preview isolado não comprova envio.

## Fluxo composto

[Contrato demonstrativo](knowledge/recipes/instagram-to-sales.json): Instagram → elegibilidade/triagem → IA limitada às fontes → vendedor com contexto → follow-up com parada → registro. Cada transição tem dono, chave de idempotência, timeout, exclusões, prova e recuperação. Sem webhook duplicado gerar novo envio; handoff humano suspende o motor automático. Não transformar observações de conversa em fatos confirmados sem a fonte/entidade correta.

Integração n8n: importar somente após verificar node/typeVersion/credenciais/expressões na versão instalada, placeholders para segredos, nenhum envio ativo no exemplo. IA: fonte e validade, escopo, fallback por baixa confiança, disponibilidade humana, opt-out, observabilidade e orçamento. RevOps: lifecycle, responsável, SLA por etapa, origem e critérios de avanço/ganho/perda; métricas dependem do inventário real e período observado.

Testes mínimos: resposta prevista, livre, silêncio, interrupção humana, duplicata, dado ausente, falha integração, falha envio, opt-out e retorno tardio. Classifique como simulado até execução/readback na conta; não marcar receita homologada pelo gerador.
