# NODE-KOMMO-007 — Pausar

Origem: seção 7 do [guia recebido](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/Guia_Salesbot_Kommo.md); referências [PRINT], [OFICIAL], [ESTRATÉGIA] preservadas. Sem teste na conta.

Pré-requisitos: editor autorizado; confirmar conta, canal, campos/IDs e permissões.
Caminho: Salesbot > Adicionar passo > Pausar.
Validação: salvar cópia inativa, exercitar cada saída com contato de teste e conferir efeito; não inferir sucesso do preview.
Submenu, seletor ou opção não descritos abaixo: **não observado**, solicitar captura do painel antes de orientar valor exato.

![Menu suspenso do passo Pausar com cinco eventos](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/imagens/07_pausar.png)

## Opções de configuração disponíveis

**[PRINT]** O dropdown revela **cinco opções**:
1. `Até a mensagem recebida`.
2. `Cronômetro`.
3. `Exceto durante o expediente`.
4. `Até o vídeo ser aberto`.
5. `Até o vídeo ser fechado`.

**[OFICIAL]**
- O `Cronômetro` aguarda intervalo definido (a documentação apresenta limite de até 8760 horas, 60 minutos e 60 segundos).
- O modo de expediente consulta o horário de trabalho configurado.
- Os eventos de vídeo **aberto/fechado** são restritos ao **Live Chat**, não ao WhatsApp.
- Pode-se configurar múltiplas condições de espera; o Salesbot segue o caminho do evento que ocorrer primeiro.

## Possibilidades disruptivas

- **SLA de atendimento:** se chegar resposta em 5 minutos, qualificar automaticamente; caso contrário, avisar o responsável.
- **Jornada respeitosa:** segurar comunicação fora do horário comercial e iniciar a próxima etapa no período operacional.
- **Follow-up controlado:** programar uma verificação ou tarefa após intervalo; evitando bombardear o cliente com mensagens.

## Dicas de outros passos que podem ser usados antes ou depois

**Antes:** `Enviar mensagem`/`Mensagem em Lista`.

**Depois (respondeu):** `Validação` → `Ação: Definir campo`.

**Depois (timer disparou):** `Ação: Adicionar tarefa` ou mensagem **somente se o canal ainda permitir** → `Parar Salesbot`.

**Métrica sugerida:** taxa de resposta em 5/15/60 minutos e tempo até handoff.

**Atenção técnica:** O cronômetro do Salesbot **não estende** a janela do WhatsApp API; qualquer mensagem programada precisa respeitar a elegibilidade no momento de envio.

---
