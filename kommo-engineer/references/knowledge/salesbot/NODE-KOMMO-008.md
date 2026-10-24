# NODE-KOMMO-008 — Inscrever-se (Meta)

Origem: seção 8 do [guia recebido](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/Guia_Salesbot_Kommo.md); referências [PRINT], [OFICIAL], [ESTRATÉGIA] preservadas. Sem teste na conta.

Pré-requisitos: editor autorizado; confirmar conta, canal, campos/IDs e permissões.
Caminho: Salesbot > Adicionar passo > Inscrever-se (Meta).
Validação: salvar cópia inativa, exercitar cada saída com contato de teste e conferir efeito; não inferir sucesso do preview.
Submenu, seletor ou opção não descritos abaixo: **não observado**, solicitar captura do painel antes de orientar valor exato.

![Inscrever-se Meta — visão do bloco](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/imagens/08_inscrever_meta_resumo.png)

![Inscrever-se Meta — instruções de opt-in no próprio editor](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/imagens/08_inscrever_meta_expandido.png)

## Opções de configuração disponíveis

**[PRINT]**
- Escolha de destinatário e canais no cabeçalho (ex.: `Todos os contatos — canais selecionados`).
- Campos de `Título da mensagem...` e `#adicionar tags`.
- Texto de consentimento exibido na mensagem, como `Você deseja continuar recebendo nossas mensagens? Você pode cancelar a qualquer momento.`
- Controle `Permitir mensagens`.
- Caminhos `Outra resposta` e `Sem resposta`.
- Nota explicativa de que a funcionalidade serve a assinaturas para comunicações posteriores.

**[OFICIAL]**
- Exige integração **Facebook** conectada à página comercial.
- Dois campos principais exigidos: **tag** do lead e **título/tópico de inscrição**.
- O recurso é de **opt-in para canais Meta/Facebook compatíveis**, não um atalho geral para disparar mensagens WhatsApp fora das regras da API.

## Possibilidades disruptivas

- **Conteúdo recorrente consentido:** construir inscrição por tópico para novidades ou eventos em canais suportados.
- **Segmentação de interesse:** vincular inscrições a tags de interesse; equipes podem usar esses sinais para campanhas futuras conforme políticas aplicáveis.
- **Gestão de relevância:** reduzir mensagens não desejadas, enviando somente a temas selecionados.

## Dicas de outros passos que podem ser usados antes ou depois

**Antes:** `Condição` por canal (Facebook) → `Enviar mensagem` explicando o tema e a frequência.

**Depois:** `Ação: Gerenciar tags` de acordo com o retorno → `Pausar`/`Parar Salesbot`.

**Métrica sugerida:** taxa de adesão por tópico, cancelamentos e engajamento das comunicações.

**Atenção técnica:** **Não confundir com opt-in do WhatsApp Business API.** Consentimento e janela WhatsApp seguem regras próprias; a inscrição exibida não garante permissão de envio por WhatsApp.

---
