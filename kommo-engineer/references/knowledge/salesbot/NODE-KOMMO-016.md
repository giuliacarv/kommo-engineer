# NODE-KOMMO-016 — Round Robin

Origem: seção 16 do [guia recebido](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/Guia_Salesbot_Kommo.md); referências [PRINT], [OFICIAL], [ESTRATÉGIA] preservadas. Sem teste na conta.

Pré-requisitos: editor autorizado; confirmar conta, canal, campos/IDs e permissões.
Caminho: Salesbot > Adicionar passo > Round Robin.
Validação: salvar cópia inativa, exercitar cada saída com contato de teste e conferir efeito; não inferir sucesso do preview.
Submenu, seletor ou opção não descritos abaixo: **não observado**, solicitar captura do painel antes de orientar valor exato.

![Round Robin com duas opções e adição de ramificação](../../../recursos do kommo/Guia_Salesbot_Kommo_2026/imagens/16_round_robin.png)

## Opções de configuração disponíveis

**[PRINT]**
- Duas ramificações iniciais, ambas denominadas `Opção`.
- Ícone `+` ao lado de cada opção para inserir o próximo passo.
- `+ Adicionar outra opção`.
- Aviso: ao adicionar ou remover uma opção, **a fila é redefinida e começa do início**.

**[OFICIAL]**
- Distribuição **circular e sequencial**, não necessariamente aleatória.
- Mínimo de **2** ramificações, máximo de **100**.
- A distribuição também pode reiniciar por longos períodos de inatividade ou situações operacionais documentadas.
- Pode ser usado para variar mensagens, criar caminhos de atividades, alternar responsáveis ou construir testes A/B.

## Possibilidades disruptivas

- **Teste de scripts comerciais:** metade dos leads recebe um texto de abordagem A; outra metade, texto B, e você mede a taxa de agendamento.
- **Carga operacional equilibrada:** criar ramos para equipes ou responsabilidades diferentes, com cautela para ausências e capacidade individual.
- **Experimentos controlados:** comparar roteiros de qualificação mantendo origem, horário e perfil dos leads equivalentes.

## Dicas de outros passos que podem ser usados antes ou depois

**Antes:** `Condição` filtra leads elegíveis e impede clientes existentes de entrar no experimento.

**Depois (em cada ramo):** `Enviar mensagem` diferente → `Ação: Gerenciar tags` (`teste_A`/`teste_B`) → `Ação: Adicionar tarefa`.

**Métrica sugerida:** conversão por ramo e distribuição efetiva de leads.

**Atenção técnica:** A sequência circular ajuda no balanceamento, mas não considera automaticamente férias, disponibilidade ou carga por vendedor; complemente com regras de elegibilidade e gestão de responsabilidade.

---
