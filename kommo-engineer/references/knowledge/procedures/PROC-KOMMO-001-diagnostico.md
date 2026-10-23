# PROC-KOMMO-001 — Diagnóstico inicial da conta

**Estado:** documentado por fonte pública; não homologado em conta Kommo.
**Revisão:** 2026-10-23.
**Aplicabilidade:** validar plano, idioma, permissões, canal, versão e interface na conta atual.


## Objetivo
Identificar a conta correta e recursos pertinentes à demanda, sem executar alterações.
## Pré-requisitos
Confirmação do subdomínio e usuário autorizado; saber se o acesso é via interface ou API.
Não peça tokens em chat. `GET /api/v4/account` é uma forma de leitura se credencial segura existir.
## Procedimento
1. Confirme o resultado comercial e quais entidades importam (leads, contatos, empresas).
2. Com API habilitada, envie **somente GET** ao subdomínio exato da conta.
3. Compare ID/nome da resposta com a conta que o usuário indicou.
4. Se necessário, use GET de pipelines e campos das entidades pertinentes.
5. Registre os IDs, origem, data, limitações e itens não verificados em `inventory.json` do projeto.
6. Pela interface, registre tela observada; não infira plano ou permissões não visíveis.
## Aceite
Alvo confirmado, IDs relevantes identificados e lacunas explicitadas. Nenhuma alteração remota.
## Falhas
401/403: interromper; subdomínio divergente: bloquear; sem ferramenta: orientação apenas.
## Fontes
- https://developers.kommo.com/reference/account-parameters
- https://developers.kommo.com/reference/pipelines-list
- https://developers.kommo.com/reference/custom-field-by-entity

