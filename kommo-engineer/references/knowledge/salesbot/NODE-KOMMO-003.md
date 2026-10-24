# NODE-KOMMO-003 — Comentário

Origem: seção 3 do [guia recebido](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/Guia_Salesbot_Kommo.md); referências [PRINT], [OFICIAL], [ESTRATÉGIA] preservadas. Sem teste na conta.

Pré-requisitos: editor autorizado; confirmar conta, canal, campos/IDs e permissões.
Caminho: Salesbot > Adicionar passo > Comentário.
Validação: salvar cópia inativa, exercitar cada saída com contato de teste e conferir efeito; não inferir sucesso do preview.
Submenu, seletor ou opção não descritos abaixo: **não observado**, solicitar captura do painel antes de orientar valor exato.

![Passo Comentário com entrada de texto](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/imagens/03_comentario.png)

## Opções de configuração disponíveis

**[PRINT]**
- Campo principal: `Escreva um comentário...`.
- Conector `+` para continuar o fluxo.
- Menu de mais opções `...` do bloco, sem conteúdo aberto no print.

**[OFICIAL]**
- A Kommo exemplifica esse passo para publicar **respostas públicas a comentários do Instagram**.
- A filtragem por palavra-chave normalmente ocorre antes, por um passo **Condição**; ela não aparece como submenu interno do bloco Comentário.
- Exige canal correspondente conectado e um gatilho apropriado de comentário.

## Possibilidades disruptivas

- **Conteúdo que gera conversa:** ao detectar comentário “CATÁLOGO”, publicar resposta curta e ativar outro fluxo de atendimento quando as regras do canal permitirem.
- **Moderação de intenção:** dar respostas diferentes a perguntas de preço, disponibilidade e dúvidas frequentes.
- **Campanhas mensuráveis:** usar tags diferentes conforme o tema do comentário para medir quais publicações originam oportunidades qualificadas.

## Dicas de outros passos que podem ser usados antes ou depois

**Antes:** gatilho de comentário → `Condição: comentário do cliente é igual/contém palavra-chave`.

**Depois:** `Comentário` → `Ação: Gerenciar tags` ou `Enviar mensagem` se o contexto e as permissões do canal permitirem → `Parar Salesbot`.

**Métrica sugerida:** comentários acionados → conversas iniciadas → leads qualificados.

**Atenção técnica:** Não confunda responder publicamente a um comentário com enviar uma mensagem privada: a segunda ação depende da integração e das políticas de mensagens do canal.

---
