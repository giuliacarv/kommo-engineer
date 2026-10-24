# NODE-KOMMO-001 — Enviar mensagem

Origem: seção 1 do [guia recebido](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/Guia_Salesbot_Kommo.md); referências [PRINT], [OFICIAL], [ESTRATÉGIA] preservadas. Sem teste na conta.

Pré-requisitos: editor autorizado; confirmar conta, canal, campos/IDs e permissões.
Caminho: Salesbot > Adicionar passo > Enviar mensagem.
Validação: salvar cópia inativa, exercitar cada saída com contato de teste e conferir efeito; não inferir sucesso do preview.
Submenu, seletor ou opção não descritos abaixo: **não observado**, solicitar captura do painel antes de orientar valor exato.

![Passo Enviar mensagem — respostas e ramificações](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/imagens/01_enviar_mensagem_botoes.png)

![Passo Enviar mensagem — botão de URL e anexo](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/imagens/01_enviar_mensagem_url.png)

![Simulação e seleção dos canais](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/imagens/extra_canais.png)

## Opções de configuração disponíveis

**[PRINT]**
- `Escreva algo ou escolha um modelo`: insere texto livre ou seleciona um modelo pronto.
- Ícones visíveis: **microfone**, **anexo** e **adicionar**; aparecem conforme o tipo de composição do bloco.
- `+ Botão de ação`: inclui respostas guiadas; cada botão pode conduzir a uma ramificação.
- `+ Botão de URL`: cria um botão que abre um endereço.
- `Outra resposta`: caminho para texto diferente dos botões/sinônimos previstos.
- `Sem resposta`: caminho de ausência de retorno, geralmente associado a uma espera.
- `Falha ao enviar a mensagem`: tratamento separado de erro de envio.
- A captura de pré-visualização traz os canais **WhatsApp Business, WhatsApp Lite, Facebook, Instagram, Telegram, TikTok e Outros canais**. São destinos exibidos no simulador, não garantia de suporte idêntico a todos os formatos.

**[OFICIAL]**
- É possível inserir botões de resposta rápida, sinônimos de resposta e anexos (documento, imagem, vídeo e áudio, com regras por canal).
- É possível escolher destinatários: **todos os contatos** ou **contato principal**, usando **canais selecionados** ou **canal principal**.
- A Kommo documenta até **13 botões no editor**, mas recomenda em geral **até 3** para não comprometer a exibição em determinados canais.
- A continuidade principal e a ramificação de falha de envio devem ser tratadas separadamente.

## Possibilidades disruptivas

- **Qualificação progressiva:** perguntar objetivo, segmento e prazo em pequenas mensagens; gravar as respostas com **Ação → Definir campo** em vez de deixar dados soltos no chat.
- **Triagem com recuperação automática:** se a mensagem falhar, registrar uma tarefa para o time verificar número, canal, template e histórico do atendimento.
- **Venda consultiva multicanal:** apresentar escolhas que abrem páginas específicas; usar tags para medir quantos clientes escolheram cada opção.

## Dicas de outros passos que podem ser usados antes ou depois

**Antes:** `Condição` (segmento/canal) → `Enviar mensagem`.

**Depois:** `Pausar` (aguardar retorno) → `Validação` (qualidade do dado) → `Ação: Definir campo`.

**Tratamento de erro:** `Falha ao enviar a mensagem` → `Ação: Adicionar tarefa` → `Enviar mensagem interna` → `Parar Salesbot`.

**Métrica sugerida:** taxa de entrega e taxa de resposta por opção.

**Atenção técnica:** **WhatsApp API:** mensagens livres e interativas normalmente dependem da janela de atendimento aberta; fora dela, planeje a retomada com um template aprovado e com permissão adequada. Não assuma que um botão renderizado em outro canal terá o mesmo comportamento no WhatsApp.

---
