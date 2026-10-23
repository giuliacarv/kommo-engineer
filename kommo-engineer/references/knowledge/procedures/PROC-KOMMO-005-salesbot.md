# PROC-KOMMO-005 — Salesbot visual e JSON

**Estado:** documentado por fonte pública; não homologado em conta Kommo.
**Revisão:** 2026-10-23.
**Aplicabilidade:** validar plano, idioma, permissões, canal, versão e interface na conta atual.


## Objetivo
Criar um fluxo de atendimento/qualificação seguro, verificável e compatível com o canal.
## Pré-requisitos
Objetivo comercial, canal conectado, permissões, plano, campos necessários, público de teste,
gatilho e autorização para salvar/disparar.
## Escolha técnica
- Visual: preferência quando bloco/conector for suficiente e manutenção pela equipe for essencial.
- JSON: somente se o formato do editor ou importação for identificado e documentado.
- SDK de widgets: contrato **distinto** do JSON de Salesbot.
## Fluxo de construção
1. Liste canais e condições de disparo; identifique o estado inicial.
2. Modele conversa em blocos e transições com fallback para entradas inesperadas.
3. Defina campos no nível certo (lead/contato/empresa) e suas dependências.
4. Inclua lógica de pausa, encerramento e passagem a humano conforme objetivo.
5. Garanta que nenhum contato real receba mensagens durante teste sem autorização.
6. Salve e reabra; valide transições e gatilhos no ambiente/canal de teste.
7. Registre screenshots reais com data e caminhos; classifique visual/JSON/testado independentemente.
## Cuidado com JSON
A documentação apresenta estruturas `question`, `answer`, `finish` e handlers como `show`,
`action`, `condition`, `goto`, `wait_answer`, `stop`; não invente handlers ou esquema de importação.
Código exibido no editor pode ter limitações na volta ao visual; preserve cópia antes da alteração.
## Aceite
Fluxo testado no canal e condições especificadas, sem duplicidades; evidência de execução.
## Fontes
- https://developers.kommo.com/docs/salesbot-dp
- https://developers.kommo.com/docs/salesbot-sdk

