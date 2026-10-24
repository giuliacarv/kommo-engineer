# NODE-KOMMO-006 — Condição de IA

Origem: seção 6 do [guia recebido](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/Guia_Salesbot_Kommo.md); referências [PRINT], [OFICIAL], [ESTRATÉGIA] preservadas. Sem teste na conta.

Pré-requisitos: editor autorizado; confirmar conta, canal, campos/IDs e permissões.
Caminho: Salesbot > Adicionar passo > Condição de IA.
Validação: salvar cópia inativa, exercitar cada saída com contato de teste e conferir efeito; não inferir sucesso do preview.
Submenu, seletor ou opção não descritos abaixo: **não observado**, solicitar captura do painel antes de orientar valor exato.

![Passo Condição de IA com descrição e avisos beta](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/imagens/06_condicao_ia.png)

## Opções de configuração disponíveis

**[PRINT — confirmado diretamente na interface]**
- `Descreva a condição`: entrada em linguagem natural, por exemplo: `O cliente está pronto para comprar ou pergunta sobre o preço`.
- `+ Adicionar próxima condição`: cria outras intenções ou critérios.
- `Nenhuma das condições`: fallback quando nenhum critério for escolhido.
- A descrição da interface informa que a IA usa **mensagem do cliente e campos de lead adicionados à condição**, selecionando a melhor correspondência.
- Pode inserir campos de lead pelo seletor acionado por `[` ou pelo botão de adição indicado.
- Aviso de **versão beta**: o recurso pode mudar ou ficar indisponível.
- Aviso de **créditos de IA**: a análise de mensagem consome créditos; se esgotarem, o bot segue pelo caminho `Nenhuma das condições`.
- A interface recomenda descrever critérios de forma clara e testar antes de usar com clientes.

**[LIMITAÇÃO]** Não há submenu externo aberto mostrando todas as opções de campo, modelo ou plano; não inventamos esses parâmetros.

## Possibilidades disruptivas

- **Roteamento por intenção sem palavra exata:** entender “preciso contratar agora”, “quanto custa?” e “quero um orçamento” como intenção comercial próxima.
- **Alerta de churn ou atrito:** classificar reclamação, urgência e pedido de cancelamento, escalando imediatamente à equipe correta.
- **Triage híbrida:** usar IA para compreender texto livre e, em seguida, regras determinísticas para mover etapa e registrar tags — evitando que a IA execute ações críticas sem confirmação.

## Dicas de outros passos que podem ser usados antes ou depois

**Antes:** `Enviar mensagem` com pergunta aberta → `Pausar: Até a mensagem recebida`.

**Depois:** ramo `Compra` → `Ação: Gerenciar tags` + `Adicionar tarefa`; ramo `Suporte` → `Iniciar Salesbot` especializado; ramo `Nenhuma das condições` → `Mensagem em Lista` ou humano.

**Boa arquitetura:** IA **interpreta**, `Condição/Validação` **conferem**, `Ação` **executa**.

**Métrica sugerida:** acurácia por intenção, percentual de fallback, custo por classificação e conversão após roteamento.

**Atenção técnica:** Crie sempre um caminho de contingência. Como o próprio painel avisa, crédito esgotado e falhas de classificação podem levar ao fallback.

---
