# NODE-KOMMO-010 — Condição

Origem: seção 10 do [guia recebido](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/Guia_Salesbot_Kommo.md); referências [PRINT], [OFICIAL], [ESTRATÉGIA] preservadas. Sem teste na conta.

Pré-requisitos: editor autorizado; confirmar conta, canal, campos/IDs e permissões.
Caminho: Salesbot > Adicionar passo > Condição.
Validação: salvar cópia inativa, exercitar cada saída com contato de teste e conferir efeito; não inferir sucesso do preview.
Submenu, seletor ou opção não descritos abaixo: **não observado**, solicitar captura do painel antes de orientar valor exato.

![Passo Condição com comparação e caminho padrão](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/imagens/10_condicao.png)

## Opções de configuração disponíveis

**[PRINT]**
- Exemplo exibido: `Se Cliente enviar Iguais: Entrada manual`.
- `Adicionar condição (+)` dentro de um ramo.
- `+ Adicionar próxima condição` para outro ramo.
- `Nenhuma das condições` para fallback.
- A captura confirma comparação de entrada e operação `Iguais`, mas **não mostra o dropdown completo** de operadores/fontes.

**[OFICIAL]**
- Pode avaliar mensagem/chat, fonte do lead, código do chat ativo e campos personalizados disponíveis.
- Permite múltiplos ramos para resultados diferentes.
- As opções exatas de cada seletor dependem dos dados, campos e condições habilitados no ambiente.

## Possibilidades disruptivas

- **Roteamento por origem:** campanhas pagas seguem para equipe A; indicações seguem para atendimento de parceria.
- **Tratamento por dados existentes:** leads com campo `Plano` preenchido não repetem perguntas; os demais entram em enriquecimento de dados.
- **Antiduplos de comunicação:** verificar tag de campanha antes de reenviar materiais ou criar tarefas repetidas.

## Dicas de outros passos que podem ser usados antes ou depois

**Antes:** `Mensagem em Lista` para obter escolha, ou `Ação: Definir campo` para registrar contexto.

**Depois:** ramo aprovado → `Ação: Mudar etapa`; ramo não aprovado → `Enviar mensagem` explicativa; `Nenhuma das condições` → `Enviar mensagem interna`.

**Métrica sugerida:** distribuição entre ramos e queda de conversão por condição.

**Atenção técnica:** **Condição** compara dados/regras; **Validação** testa formato da resposta; **Condição de IA** interpreta intenção e pode consumir créditos. Escolha o bloco conforme o problema.

---
