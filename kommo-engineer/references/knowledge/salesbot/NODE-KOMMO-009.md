# NODE-KOMMO-009 — Ação

Origem: seção 9 do [guia recebido](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/Guia_Salesbot_Kommo.md); referências [PRINT], [OFICIAL], [ESTRATÉGIA] preservadas. Sem teste na conta.

Pré-requisitos: editor autorizado; confirmar conta, canal, campos/IDs e permissões.
Caminho: Salesbot > Adicionar passo > Ação.
Validação: salvar cópia inativa, exercitar cada saída com contato de teste e conferir efeito; não inferir sucesso do preview.
Submenu, seletor ou opção não descritos abaixo: **não observado**, solicitar captura do painel antes de orientar valor exato.

![Entrada Ação: submenu não foi aberto nos prints recebidos](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/imagens/09_acao_menu.png)

## Opções de configuração disponíveis

**[PRINT]** A imagem recortada confirma a existência do passo `Ação` e da seta de submenu, mas não mostra a lista interna.

**[OFICIAL]** O guia do Salesbot descreve estas ações:

| Ação interna | Principais parâmetros/efeito |
|---|---|
| **Adicionar nota** | Entidade alvo e texto da anotação. |
| **Adicionar tarefa** | Responsável, tipo, vencimento e comentário. |
| **Alterar status da conversa** | Marcar conversa como respondida ou fechada. |
| **Mudar status do lead** | Selecionar funil e etapa de destino. |
| **Mudar usuário responsável** | Escolher usuário e entidade (lead, contato principal, todos os contatos, contato do chat ou empresa). |
| **Concluir tarefa** | Selecionar tarefas a concluir e critérios aplicáveis. |
| **Gerar formulário** | Criar formulário e definir campos; pode alimentar lead atual ou criar novo, conforme configuração. |
| **Criar lead** | Definir dados copiados/incluídos, responsável, funil e etapa. |
| **Gerenciar assinantes** | Adicionar/remover membros da equipe que acompanham o lead. |
| **Gerenciar tags** | Adicionar ou remover tags em entidades selecionadas. |
| **Meta Conversions API** | Acionar evento de conversão integrado à Meta, mediante integração/configuração. |
| **Enviar email** | Usar endereço de email conectado e modelo pré-criado. |
| **Enviar webhook** | Inserir URL de integração externa; tratar a resposta no sistema receptor. |
| **Definir campo** | Selecionar entidade, campo e origem do dado (p.ex., última mensagem ou entrada manual, conforme o campo). |

**Importante:** os rótulos exatos e subcampos do seu dropdown **ainda não foram fotografados**. A tabela acima é um inventário **documental**, não transcrição visual da sua conta.

## Possibilidades disruptivas

- **Lead autônomo:** ao identificar orçamento e prazo, preencher campos, atribuir uma pontuação externa e mover o lead para uma fila prioritária.
- **Integração orquestrada:** usar `Enviar webhook` para avisar n8n/ERP, calcular proposta ou consultar estoque; o sistema externo deve validar autenticação, duplicidades e consistência.
- **Rastreio de qualidade comercial:** gravar tags de intenção e eventos de conversão para comparar origem, qualificação e fechamento.
- **Operação sem esquecimentos:** gerar tarefa ao responsável sempre que o cliente pedir contato humano.

## Dicas de outros passos que podem ser usados antes ou depois

**Antes:** `Validação` (dado correto), `Condição` (regra determinística) ou `Condição de IA` (intenção).

**Depois:** `Enviar mensagem interna` para handoff, `Enviar mensagem` para confirmação, ou `Iniciar Salesbot` especializado.

**Mini-fluxo:** `Condição de IA: orçamento` → `Ação: Definir campo` → `Ação: Mudar status do lead` → `Ação: Adicionar tarefa` → `Parar Salesbot`.

**Métrica sugerida:** tarefas no prazo, precisão de dados gravados, tempo de ciclo entre etapas e taxa de conversão.

**Atenção técnica:** **Webhook ≠ resposta garantida.** Configure idempotência, autenticação, logs, alerta de falha e mecanismos de reprocessamento do lado do n8n/ERP. O bloco do Salesbot só expõe a chamada que a integração oferece.

---
