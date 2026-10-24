# NODE-KOMMO-004 — Enviar mensagem interna

Origem: seção 4 do [guia recebido](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/Guia_Salesbot_Kommo.md); referências [PRINT], [OFICIAL], [ESTRATÉGIA] preservadas. Sem teste na conta.

Pré-requisitos: editor autorizado; confirmar conta, canal, campos/IDs e permissões.
Caminho: Salesbot > Adicionar passo > Enviar mensagem interna.
Validação: salvar cópia inativa, exercitar cada saída com contato de teste e conferir efeito; não inferir sucesso do preview.
Submenu, seletor ou opção não descritos abaixo: **não observado**, solicitar captura do painel antes de orientar valor exato.

![Entrada do passo Enviar mensagem interna — não há print do painel aberto](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/imagens/04_mensagem_interna_menu.png)

## Opções de configuração disponíveis

**[PRINT]** A imagem disponível mostra **apenas a opção no menu**; não mostra os campos internos.

**[OFICIAL]**
- Conteúdo da mensagem destinada à equipe.
- Seleção de um ou vários usuários responsáveis/destinatários.
- Mensagem privada ao contexto de trabalho da Kommo, não enviada ao contato externo.
- Na linguagem de desenvolvedor, o handler `send_internal` admite mensagem, entidade/lead e identificação de usuário ou grupo; isto é uma **capacidade da API/linguagem**, não prova de todos esses campos no formulário visual.

## Possibilidades disruptivas

- **Escalonamento de alta intenção:** alertar pré-vendas quando um cliente informar “quero fechar hoje”.
- **Alertas operacionais contextuais:** avisar financeiro quando o cliente escolher segunda via ou confirmar comprovante.
- **Handoff sem perda de contexto:** combinar resposta do bot, tags e mensagem para orientar o consultor na próxima ação.

## Dicas de outros passos que podem ser usados antes ou depois

**Antes:** `Condição de IA` (classificação) ou `Mensagem em Lista` (setor escolhido) → `Ação: Definir campo`.

**Depois:** `Ação: Mudar usuário responsável` → `Ação: Adicionar tarefa` → `Parar Salesbot`.

**Métrica sugerida:** tempo entre alerta interno e primeira ação do responsável.

**Atenção técnica:** Para o passo visual, é necessário um print expandido para catalogar todos os seletores com precisão.

---
