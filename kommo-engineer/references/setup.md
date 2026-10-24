# Setup guiado — Kommo Engineer (Etapa 3)

## Propósito

No primeiro uso em um projeto, ajudar a descobrir o objetivo comercial sem começar por perguntas técnicas irrelevantes. A skill conduz a conversa; o utilitário local registra os dados. Não execute operações remotas durante o setup.

**Primeira pergunta conversacional:**

> Qual é seu papel na empresa, como vocês vendem hoje e qual problema querem resolver primeiro com o Kommo?

A pergunta identifica autoridade, processo e prioridade. Registre as respostas nos campos correspondentes, sem forçar uma resposta única para preencher dados independentes.

## Fonte de verdade e estados

O contrato verificável está em [`schemas/setup-fields.json`](../schemas/setup-fields.json). Evite repetir listas estáticas de campos aqui.

Estados de cada resposta:
- `pending`: não respondida.
- `proposed`: hipótese ou sugestão; requer confirmação do usuário.
- `confirmed`: resposta afirmada pelo usuário.
- `deferred`: decisão adiada com justificativa; obrigatórios continuam pendentes.
- `not_applicable`: campo opcional inaplicável, com justificativa. Nunca em obrigatório.

Estados gerais:
- `in_progress`: ainda faltam campos necessários para planejar.
- `ready_for_planning`: os campos centrais de planejamento estão confirmados, mas o setup completo possui pendências.
- `complete`: todos os obrigatórios estão confirmados. **Não equivale** a autorização de mutações remotas ou confirmação de recursos/plano/canais da conta.

A progressão geral é computada pelas respostas, não decidida livremente pelo agente.

## Fluxo de trabalho

1. Verifique se `.kommo-engineer/project.json` já existe. Se existir, execute `project resume` e `setup status`; não reinicialize.
2. Para novo diretório: use `project init --project ... --name ... --business ... --goal ...`.
3. Para diretório de cliente já existente: **somente com autorização explícita para anexar o contexto** use `--use-existing-dir`. O inicializador preserva arquivos preexistentes e acrescenta uma seção delimitada a `AGENTS.md` quando existente.
4. Consulte `setup status`, apresente somente a próxima pergunta relevante e registre respostas com `setup update`.
5. Uma hipótese deve usar `--proposed`; nunca promova automaticamente para `confirmed`.
6. Campos não críticos podem ficar pendentes ou adiados. Requisitos técnicos condicionais (plano Kommo, canais, permissão etc.) tornam-se bloqueadores antes da operação que deles depender.
7. Quando pronto, use `project resume` para recuperar o resumo e criar a primeira meta, se fizer sentido. Consultas pontuais não exigem projeto.

### Exemplos sintáticos (não execute automaticamente)

```powershell
py -3 "<SKILL>\\scripts\\ke.py" project init --project "C:\\Projetos\\Cliente" --name "Cliente" --business "Serviços" --goal "Organizar leads" --use-existing-dir
py -3 "<SKILL>\\scripts\\ke.py" setup status --project "C:\\Projetos\\Cliente"
py -3 "<SKILL>\\scripts\\ke.py" setup update --project "C:\\Projetos\\Cliente" --field role --value "Gestor comercial"
py -3 "<SKILL>\\scripts\\ke.py" setup update --project "C:\\Projetos\\Cliente" --field channels --defer --reason "Confirmar canais depois"
py -3 "<SKILL>\\scripts\\ke.py" project resume --project "C:\\Projetos\\Cliente"
```

Não informe credenciais em CLI, respostas ou documentos. Argumentos de processos podem ficar visíveis em ferramentas do sistema; trate `--value` como entrada para texto comercial não sensível.

## Continuidade entre chats

`AGENTS.md` é um roteador conciso. Leia `.kommo-engineer/state.json`, `.kommo-engineer/project.json` e somente a meta ativa (ou última relevante) quando existir. `project resume` retorna nome, estado do setup, pendências, meta relevante, plano, próxima ação e referências de arquivo, sem reler logs ou capturas.

## Validação e limites

- `project validate` confere contratos mínimos e identifica estado de setup inconsistente ou campos obrigatórios marcados inaplicáveis.
- A própria presença de um ID de conta em texto livre não comprova o ID remoto; validar em preflight.
- A segurança do estado local não impede um editor externo de adulterar arquivos. Evite edições manuais não verificadas.
- Esta etapa não implementa o entrevistador autônomo no CLI nem acesso Kommo; a conversa é responsabilidade da skill no Codex.


## Entrada opcional por conversas ou materiais existentes

Se o usuário fornecer conversas para orientar o projeto, complemente o setup com [onboarding baseado em evidência](strategy/conversation-led-onboarding.md). Preserve o contrato atual de respostas propostas/confirmadas: extração por LLM, planilha gerada e IDs simulados não confirmam decisão humana nem recurso criado na conta.


## Atualização 0.5 RC

Consulte [workflow operacional](operational-workflow.md). O aceite por arquivo foi substituído por anexo + teste/observação explícitos. Schemas são validados em runtime no subconjunto documentado; relatórios têm releases imutáveis.
