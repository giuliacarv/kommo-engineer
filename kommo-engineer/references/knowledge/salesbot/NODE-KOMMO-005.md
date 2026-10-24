# NODE-KOMMO-005 — Mensagem em Lista (WhatsApp)

Origem: seção 5 do [guia recebido](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/Guia_Salesbot_Kommo.md); referências [PRINT], [OFICIAL], [ESTRATÉGIA] preservadas. Sem teste na conta.

Pré-requisitos: editor autorizado; confirmar conta, canal, campos/IDs e permissões.
Caminho: Salesbot > Adicionar passo > Mensagem em Lista (WhatsApp).
Validação: salvar cópia inativa, exercitar cada saída com contato de teste e conferir efeito; não inferir sucesso do preview.
Submenu, seletor ou opção não descritos abaixo: **não observado**, solicitar captura do painel antes de orientar valor exato.

![Mensagem em Lista: campos de cabeçalho, botão e opções](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/imagens/05_mensagem_lista.png)

## Opções de configuração disponíveis

**[PRINT]**
- `Título da mensagem...` (opcional).
- `Mensagem...` (obrigatória).
- `Rodapé...` (opcional).
- `Nome do botão...` (obrigatório).
- `Título da seção...` (obrigatório).
- `Título da opção...` (obrigatório).
- `Descrição...` (opcional).
- `Adicionar opção` e `+ Adicionar seção`.
- Ramificações: `Outra resposta` e `Sem resposta`.

**[OFICIAL | atualizado em 16/10/2026]**
- Máximo **10 opções no total**, somadas todas as seções.
- Cada seção contém ao menos uma opção; seleção do cliente é única por lista.
- Título de seção: até **24 caracteres**; título de opção: até **24**; descrição: até **72**.
- Lista é **mensagem interativa**, não é template aprovado pela Meta.
- Disponível somente no **Salesbot**, com integração WhatsApp Business, **janela de 24 horas aberta** e requisitos de plano/permissão documentados (Avançado ou superior ou teste ativo; administrador).

## Possibilidades disruptivas

- **Central inteligente:** uma única lista de `Vendas`, `Suporte`, `Financeiro` e `Parcerias`, seguida de atribuição automática de setor e responsável.
- **Pré-qualificação de proposta:** perguntar faixa de investimento, categoria ou unidade de interesse sem exigir digitação.
- **Pós-venda escalável:** oferecer escolhas de status do pedido, devolução e ajuda técnica; registrar a categoria de atendimento.

## Dicas de outros passos que podem ser usados antes ou depois

**Antes:** `Enviar mensagem` (contextualizar e pedir permissão de seguir) ou receber mensagem do cliente para abrir a janela.

**Depois:** `Condição: mensagem do cliente é igual ao título exato da opção` → `Ação: Definir campo` → `Ação: Mudar status do lead` → `Round Robin`/`Mudar usuário responsável`.

**Fallback:** `Outra resposta` → `Enviar mensagem` de esclarecimento; `Sem resposta` → `Pausar`/`Adicionar tarefa`.

**Métrica sugerida:** escolhas por departamento e porcentagem resolvida sem humano.

**Atenção técnica:** **Regra crítica:** fora da janela de 24 horas a lista não é entregue. O fluxo correto é usar um template WhatsApp aprovado (quando autorizado), aguardar resposta do cliente e só então abrir a lista.

---
