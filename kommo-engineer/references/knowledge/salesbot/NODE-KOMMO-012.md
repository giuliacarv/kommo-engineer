# NODE-KOMMO-012 — Ir para outra etapa

Origem: seção 12 do [guia recebido](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/Guia_Salesbot_Kommo.md); referências [PRINT], [OFICIAL], [ESTRATÉGIA] preservadas. Sem teste na conta.

Pré-requisitos: editor autorizado; confirmar conta, canal, campos/IDs e permissões.
Caminho: Salesbot > Adicionar passo > Ir para outra etapa.
Validação: salvar cópia inativa, exercitar cada saída com contato de teste e conferir efeito; não inferir sucesso do preview.
Submenu, seletor ou opção não descritos abaixo: **não observado**, solicitar captura do painel antes de orientar valor exato.

![Entrada Ir para outra etapa: submenu não capturado](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/imagens/12_ir_outra_etapa_menu.png)

## Opções de configuração disponíveis

**[PRINT]** O item e a seta de submenu aparecem no menu.

**[OFICIAL]**
- Selecionar outra etapa **já existente** no Salesbot.
- Criar ligação para a etapa escolhida sem duplicar toda a sequência.
- A opção depende de haver uma etapa disponível como destino; o dropdown exato não aparece nos prints enviados.

## Possibilidades disruptivas

- **Módulo de correção reaproveitável:** qualquer validação inválida pode voltar ao mesmo bloco de coleta sem copiar telas.
- **Caminho único de handoff:** diferentes intenções convergem para a mesma sequência de atribuição e tarefa.
- **Fluxos menores e auditáveis:** caminhos de suporte, cobrança e comercial podem convergir em etapa de encerramento comum.

## Dicas de outros passos que podem ser usados antes ou depois

**Antes:** `Validação` ou `Condição` que exige retorno/reutilização.

**Depois:** bloco destino como `Enviar mensagem`, `Ação` ou `Parar Salesbot`.

**Métrica sugerida:** quantidade de retornos por lead e pontos com maior repetição.

**Atenção técnica:** Proteja loops: defina limite de tentativas, fallback humano e condição clara de saída. Uma volta sem saída pode impedir o encerramento do bot.

---
