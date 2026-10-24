# NODE-KOMMO-011 — Validação

Origem: seção 11 do [guia recebido](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/Guia_Salesbot_Kommo.md); referências [PRINT], [OFICIAL], [ESTRATÉGIA] preservadas. Sem teste na conta.

Pré-requisitos: editor autorizado; confirmar conta, canal, campos/IDs e permissões.
Caminho: Salesbot > Adicionar passo > Validação.
Validação: salvar cópia inativa, exercitar cada saída com contato de teste e conferir efeito; não inferir sucesso do preview.
Submenu, seletor ou opção não descritos abaixo: **não observado**, solicitar captura do painel antes de orientar valor exato.

![Entrada Validação: painel aberto não foi capturado](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/imagens/11_validacao_menu.png)

## Opções de configuração disponíveis

**[PRINT]** Apenas a entrada `Validação` foi capturada no menu.

**[OFICIAL]** Operadores documentados:
1. `É igual`.
2. `Não é igual`.
3. `Contém`.
4. `Não contém`.
5. `Tem um comprimento de`.
6. `Expressão regular (Regex)`.

Ao usar `Contém`, a Kommo documenta testes específicos de conteúdo como **números**, **letras**, **telefone**, **email** e **intervalo numérico**. A sintaxe detalhada e a interface de cada operador devem ser confirmadas no painel aberto.

## Possibilidades disruptivas

- **Cadastro limpo antes de vender:** validar telefone ou email antes de gravar no CRM, reduzindo retrabalho e contatos inválidos.
- **Pré-aprovação automatizada:** verificar código, CEP ou protocolo em formato esperado; consultar autenticidade em integração externa quando necessário.
- **Controle de respostas vazias:** impedir avanço para orçamento quando o cliente devolve resposta incompleta ou incompatível.

## Dicas de outros passos que podem ser usados antes ou depois

**Antes:** `Enviar mensagem: Informe seu email` → `Pausar: Até a mensagem recebida`.

**Depois (válido):** `Ação: Definir campo` → `Enviar mensagem` de confirmação.

**Depois (inválido):** `Enviar mensagem: Confira o formato` → `Ir para outra etapa` (retornar à pergunta).

**Métrica sugerida:** percentual de respostas válidas na primeira tentativa.

**Atenção técnica:** Regex verifica **formato**, não comprova que email, telefone ou documento realmente existem; quando necessário valide com serviço apropriado e permissão legal.

---
