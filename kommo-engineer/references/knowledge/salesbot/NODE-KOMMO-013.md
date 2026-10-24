# NODE-KOMMO-013 — Iniciar Salesbot

Origem: seção 13 do [guia recebido](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/Guia_Salesbot_Kommo.md); referências [PRINT], [OFICIAL], [ESTRATÉGIA] preservadas. Sem teste na conta.

Pré-requisitos: editor autorizado; confirmar conta, canal, campos/IDs e permissões.
Caminho: Salesbot > Adicionar passo > Iniciar Salesbot.
Validação: salvar cópia inativa, exercitar cada saída com contato de teste e conferir efeito; não inferir sucesso do preview.
Submenu, seletor ou opção não descritos abaixo: **não observado**, solicitar captura do painel antes de orientar valor exato.

![Entrada Iniciar Salesbot: painel não capturado](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/imagens/13_iniciar_salesbot_menu.png)

## Opções de configuração disponíveis

**[PRINT]** O menu mostra o passo, mas o seletor de bots não foi aberto.

**[OFICIAL]**
- Escolher outro Salesbot já criado para ser iniciado no contexto do fluxo.
- Reutilizar um bot especializado dentro de outro.
- A Kommo documenta a continuidade do fluxo chamador após o bot auxiliar concluir, conforme o cenário exemplificado; o comportamento específico deve ser testado na configuração real.

## Possibilidades disruptivas

- **Arquitetura modular:** criar bots especializados (cadastro, pré-vendas, suporte, cobrança) em vez de um único fluxo gigante.
- **Padronização de unidades:** diferentes funis chamam o mesmo bot de validação cadastral.
- **Manutenção mais rápida:** atualizar regras de coleta em um só Salesbot, em vez de replicar em dezenas de automações.

## Dicas de outros passos que podem ser usados antes ou depois

**Antes:** `Condição`/`Mensagem em Lista` define o módulo necessário.

**Depois:** bot auxiliar executa cadastro → fluxo principal segue para `Ação: Mudar status do lead` ou `Enviar mensagem interna`.

**Métrica sugerida:** taxa de conclusão por bot auxiliar e número de pontos de manutenção reduzidos.

**Atenção técnica:** Evite bots que chamam uns aos outros circularmente. Faça testes de contexto, transferência e término.

---
