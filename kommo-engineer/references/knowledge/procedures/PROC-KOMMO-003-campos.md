# PROC-KOMMO-003 — Campos personalizados

**Estado:** documentado por fonte pública; não homologado em conta Kommo.
**Revisão:** 2026-10-23.
**Aplicabilidade:** validar plano, idioma, permissões, canal, versão e interface na conta atual.


## Objetivo
Projetar e criar campos na entidade correta, evitando duplicação.
## Pré-requisitos
Finalidade comercial, entidade (`leads`, `contacts`, `companies`), nome, tipo, visibilidade,
permissões de administrador para adicionar por API; autorização explícita de mutação.
## Opções
- API oficial: `GET /api/v4/{entity_type}/custom_fields` para inventário;
  `POST /api/v4/{entity_type}/custom_fields` para criação com payload do **tipo documentado**.
- Interface: Admin pode configurar pela interface; confirme a tela viva.
## Procedimento
1. Liste campos existentes e seus IDs/códigos/tipos.
2. Compare nome, entidade e definição; mesmo nome não prova equivalência.
3. Valide contrato oficial do tipo desejado e dependências de enums/grupos.
4. Mostre proposta e obtenha aprovação.
5. Crie somente depois da autorização.
6. Leia novamente e compare ID, nome, entidade, tipo e propriedades aprovadas.
7. Registre IDs reais e evidência sanitizada.
## Em timeout
Não repita POST sem primeiro pesquisar se o campo foi criado.
## Aceite
Campo persistido com as propriedades autorizadas; nova execução não duplica.
## Fontes
- https://developers.kommo.com/reference/custom-field-by-entity
- https://developers.kommo.com/reference/add-custom-fields
- https://support.kommo.com/docs/customize-fields-in-lead-profiles

