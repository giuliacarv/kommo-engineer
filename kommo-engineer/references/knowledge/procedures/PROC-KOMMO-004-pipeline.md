# PROC-KOMMO-004 — Pipelines e etapas

**Estado:** documentado por fonte pública; não homologado em conta Kommo.
**Revisão:** 2026-10-23.
**Aplicabilidade:** validar plano, idioma, permissões, canal, versão e interface na conta atual.


## Objetivo
Representar um processo comercial aprovado por pipelines e etapas.
## Pré-requisitos
Jornada e regras comerciais definidas, identificação da conta, admin para criar/editar por API,
inventário dos pipelines atuais, autorização de mudança.
## Endpoints documentados (não execute sem contrato dos parâmetros)
- GET `/api/v4/leads/pipelines`
- POST `/api/v4/leads/pipelines`
- GET `/api/v4/leads/pipelines/{pipeline_id}/statuses`
- POST `/api/v4/leads/pipelines/{pipeline_id}/statuses`
## Procedimento
1. Liste pipelines e estágios; registre IDs.
2. Identifique estágios do sistema e restrições documentadas.
3. Desenhe etapas, ordenação, eventos e critérios para avanço; revise com vendas.
4. Planeje criação de pipeline e estágios separadamente; não infira que PATCH pipeline edita estágios.
5. Obtenha autorização, execute por API/interface compatível e releia.
6. Confira nome, ordem, IDs, estágio de chegada/perda e preservação dos leads existentes.
7. Registre configuração e evidência; revise automações dependentes.
## Aceite
Pipeline e etapas corretos, sem alterações colaterais não autorizadas.
## Fontes
- https://developers.kommo.com/reference/pipelines-list
- https://developers.kommo.com/reference/add-pipelines
- https://developers.kommo.com/reference/stages-list
- https://developers.kommo.com/reference/add-stages
- https://developers.kommo.com/reference/leads-pipelines-and-stages

