# NODE-KOMMO-015 — Widget

Origem: seção 15 do [guia recebido](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/Guia_Salesbot_Kommo.md); referências [PRINT], [OFICIAL], [ESTRATÉGIA] preservadas. Sem teste na conta.

Pré-requisitos: editor autorizado; confirmar conta, canal, campos/IDs e permissões.
Caminho: Salesbot > Adicionar passo > Widget.
Validação: salvar cópia inativa, exercitar cada saída com contato de teste e conferir efeito; não inferir sucesso do preview.
Submenu, seletor ou opção não descritos abaixo: **não observado**, solicitar captura do painel antes de orientar valor exato.

![Entrada Widget: painel de escolha não capturado](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/imagens/15_widget_menu.png)

## Opções de configuração disponíveis

**[PRINT]** O passo está no menu; não há print do catálogo de widgets ou da configuração de um widget específico.

**[OFICIAL]**
- Selecionar integração/widget disponível para execução dentro do Salesbot.
- Widgets instalados aparecem primeiro; a interface pode oferecer instalação de outros.
- Cada widget define seus próprios parâmetros (por exemplo, integrações de pagamento, notificação, consulta etc.).

**Não existe uma lista universal de sub-opções:** elas dependem do widget instalado e da versão do fornecedor.

## Possibilidades disruptivas

- **Cobrança dentro da jornada:** gerar link de pagamento por widget compatível, com retorno de status tratado em outros passos.
- **Ponte com software legado:** acionar um widget de agenda, faturas ou catálogo sem reimplementar toda a experiência.
- **Fluxo de atendimento especializado:** usar serviços prontos para enriquecer o lead ou abrir solicitações.

## Dicas de outros passos que podem ser usados antes ou depois

**Antes:** `Condição` (determinar elegibilidade) → `Validação` (coletar dado correto).

**Depois:** `Enviar mensagem` com instrução de próxima ação → `Ação: Definir campo`/`Adicionar tarefa`.

**Métrica sugerida:** sucesso e tempo médio da operação pelo widget.

**Atenção técnica:** Integração de terceiros requer avaliação de privacidade, escopos de acesso, suporte e custos. Consulte os campos reais do widget instalado.

---
