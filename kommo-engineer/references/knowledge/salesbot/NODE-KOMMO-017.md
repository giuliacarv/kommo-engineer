# NODE-KOMMO-017 — Parar Salesbot

Origem: seção 17 do [guia recebido](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/Guia_Salesbot_Kommo.md); referências [PRINT], [OFICIAL], [ESTRATÉGIA] preservadas. Sem teste na conta.

Pré-requisitos: editor autorizado; confirmar conta, canal, campos/IDs e permissões.
Caminho: Salesbot > Adicionar passo > Parar Salesbot.
Validação: salvar cópia inativa, exercitar cada saída com contato de teste e conferir efeito; não inferir sucesso do preview.
Submenu, seletor ou opção não descritos abaixo: **não observado**, solicitar captura do painel antes de orientar valor exato.

![Entrada Parar Salesbot no menu](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/imagens/17_parar_salesbot_menu.png)

## Opções de configuração disponíveis

**[PRINT]** A opção `Parar Salesbot` aparece na lista; não há parâmetros internos exibidos.

**[OFICIAL]**
- Termina a execução daquele Salesbot.
- É apropriado ao final dos ramos que concluíram seu objetivo, realizaram handoff ou passaram por tratamento de falha.
- Não encerra necessariamente o lead, a conversa ou o negócio; esses estados exigem **Ações** específicas.

## Possibilidades disruptivas

- **Encerramento limpo:** separar concluir a conversa automatizada de fechar a oportunidade de vendas.
- **Proteção contra mensagens indevidas:** impedir que sequências adicionais continuem após o cliente pedir atendimento humano.
- **Retorno mensurável:** registrar tag/nota/status antes de encerrar, permitindo auditoria de como cada ramo terminou.

## Dicas de outros passos que podem ser usados antes ou depois

**Antes:** `Ação: Gerenciar tags`, `Mudar status do lead`, `Adicionar tarefa` ou `Enviar mensagem interna`.

**Depois:** não existe continuação naquele caminho do bot. A próxima interação depende de outro gatilho, bot ou ação humana.

**Métrica sugerida:** proporção dos leads que atingem encerramento esperado versus encerramento por fallback.

**Atenção técnica:** `Parar Salesbot` não é o mesmo que `Alterar status da conversa` nem `Mudar status do lead`.

---
