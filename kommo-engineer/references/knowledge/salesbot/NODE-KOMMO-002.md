# NODE-KOMMO-002 — Reação

Origem: seção 2 do [guia recebido](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/Guia_Salesbot_Kommo.md); referências [PRINT], [OFICIAL], [ESTRATÉGIA] preservadas. Sem teste na conta.

Pré-requisitos: editor autorizado; confirmar conta, canal, campos/IDs e permissões.
Caminho: Salesbot > Adicionar passo > Reação.
Validação: salvar cópia inativa, exercitar cada saída com contato de teste e conferir efeito; não inferir sucesso do preview.
Submenu, seletor ou opção não descritos abaixo: **não observado**, solicitar captura do painel antes de orientar valor exato.

![Passo Reação com submenu de tipo de conteúdo](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/imagens/02_reacao.png)

## Opções de configuração disponíveis

**[PRINT]**
- Texto do bloco: `Reaja com um ❤️ à última ...` (emoji de coração mostrado no print).
- Menu de alvo da reação:
  - `mensagem`
  - `comentário`
- Existe um aviso inferior de restrição de disponibilidade, mas o canal completo não aparece na área capturada.

**[OFICIAL / LIMITAÇÃO]**
- O recurso permite criar reações em interações de canais compatíveis; a documentação consultada não fornece um inventário completo de emojis e restrições para cada canal.
- **Não há evidência**, neste print, de que o emoji possa ser trocado nem de que a reação de comentário funcione via WhatsApp API. Verifique no canal real antes de implementar.

## Possibilidades disruptivas

- **Reconhecimento instantâneo:** reagir a uma manifestação positiva enquanto outra etapa identifica se há intenção de compra.
- **Atendimento social sem ruído:** reagir a comentários ou mensagens relevantes sem disparar várias mensagens automáticas consecutivas.
- **Sinalização de recebimento:** criar uma experiência leve para interações rápidas em canais sociais, seguida de resposta quando pertinente.

## Dicas de outros passos que podem ser usados antes ou depois

**Antes:** gatilho por comentário ou `Condição` sobre conteúdo de mensagem.

**Depois:** `Comentário` (resposta pública, quando cabível) ou `Enviar mensagem` (continuidade), e `Parar Salesbot`.

**Métrica sugerida:** proporção de comentários com retorno humano e taxa de resposta após a interação.

**Atenção técnica:** A reação não substitui confirmação de recebimento transacional nem atendimento; confira o suporte do canal.

---
