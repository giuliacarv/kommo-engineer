# NODE-KOMMO-014 — Etapa adaptada (cód.)

Origem: seção 14 do [guia recebido](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/Guia_Salesbot_Kommo.md); referências [PRINT], [OFICIAL], [ESTRATÉGIA] preservadas. Sem teste na conta.

Pré-requisitos: editor autorizado; confirmar conta, canal, campos/IDs e permissões.
Caminho: Salesbot > Adicionar passo > Etapa adaptada (cód.).
Validação: salvar cópia inativa, exercitar cada saída com contato de teste e conferir efeito; não inferir sucesso do preview.
Submenu, seletor ou opção não descritos abaixo: **não observado**, solicitar captura do painel antes de orientar valor exato.

![Etapa adaptada com estrutura JSON visível](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/imagens/14_codigo.png)

## Opções de configuração disponíveis

**[PRINT]**
- Campo de edição de código.
- Estrutura inicial exibida: `{"handler":"","params":{}}`.
- Menu `...` do bloco.
- O print não mostra ferramentas de teste, autocomplete ou seleção de handlers.

**[OFICIAL | Documentação de desenvolvedores]**
- A etapa aceita comandos na **linguagem JSON do Salesbot** da Kommo.
- Conceitos da linguagem incluem `handler`, `params`, condições e ações.
- A documentação oficial apresenta handlers como `action`, `send_internal`, `goto`, `wait_answer`, `condition` e outros, cada qual com estrutura própria.

**Exemplo ilustrativo documentado — enviar mensagem interna vinculada ao lead:**
```json
{
  "handler": "send_internal",
  "params": {
    "entity_id": "{{lead.id}}",
    "entity_type": 2,
    "message": "Lead precisa de atendimento humano."
  }
}
```
> O exemplo é uma chamada de **linguagem Salesbot**, não de WhatsApp Cloud API. Valide no contexto da etapa e do handler suportado antes de produção.

## Possibilidades disruptivas

- **Automação sob medida:** tratar cenários que não possuem um bloco nativo na interface.
- **Reaproveitamento de dados:** compor mensagens e ações por placeholders, quando suportados pelo handler.
- **Controle fino de fluxo:** criar condições e saltos específicos para operações complexas já previstas na linguagem da Kommo.

## Dicas de outros passos que podem ser usados antes ou depois

**Antes:** `Validação` para evitar dados incompletos; `Condição` para controlar quando o código deve rodar.

**Depois:** `Ação: Adicionar nota` para auditoria ou `Enviar mensagem interna` em caso de tratamento operacional.

**Métrica sugerida:** taxa de sucesso da etapa, tempo para depuração e incidentes por mudança de código.

**Atenção técnica:** Não insira tokens, senhas ou segredos em scripts visíveis aos operadores. Para lógicas complexas ou com credenciais, prefira serviço externo seguro via webhook/API, com registro de execução.

---
