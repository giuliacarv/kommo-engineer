Origem: `runitsolutions/kommo-mcp`, versão documental 1.1.0, licença declarada MIT. Guia incorporado como referência interna; não instala servidor, ferramentas ou credenciais. Os nomes, a quantidade de ferramentas e os limites abaixo descrevem essa versão documental; confira a instalação e as ferramentas atuais antes de usá-los.

Para criar integração, guardar o token e configurar Codex, Agy ou Claude Code sem segredo no arquivo do cliente, siga [Acessar Kommo por MCP](mcp-access-setup.md). Os scripts Windows dessa referência fazem parte da skill; este arquivo descreve capacidades documentadas de um servidor específico.


# Kommo MCP

Guide for using **runitsolutions/kommo-mcp** — a TypeScript MCP server that wraps Kommo CRM API v4 (plus Files, Conversations, analytics).

Official API docs: https://developers.kommo.com/  
Server repo: https://github.com/runitsolutions/kommo-mcp

## Quando consultar este conector

- User wants to control Kommo/amoCRM from Cursor (or another MCP client)
- Need to install/configure the MCP server
- Need the right tool for leads, contacts, pipelines, tasks, notes, files, talks, Salesbots, webhooks, catalogs, custom fields, or reports

Prefer MCP tools over inventing raw `curl` calls once the server is configured.

## Instalação e configuração

O guia [Acessar Kommo por MCP](mcp-access-setup.md) fornece comandos e configurações para Windows, Codex, Agy e Claude Code. Nunca coloque o token em `mcpServers.env`, TOML, JSON, argumentos ou prompts; use o cofre local e o launcher. Um exemplo antigo do conector usava token literal no JSON do cliente e foi retirado por expor o segredo.

### Auth options

| Mode | Env vars |
|------|----------|
| Long-lived token | `KOMMO_SUBDOMAIN` + `KOMMO_ACCESS_TOKEN` |
| OAuth refresh | `KOMMO_SUBDOMAIN` + `KOMMO_CLIENT_ID` + `KOMMO_CLIENT_SECRET` + `KOMMO_REFRESH_TOKEN` |

OAuth tokens persist to `.kommo_tokens.json` (or `KOMMO_TOKEN_FILE`) and refresh automatically on HTTP 401.

### HTTP transport (optional)

```bash
MCP_TRANSPORT=http MCP_HOST=127.0.0.1 MCP_PORT=3000 npm start
# endpoint: http://127.0.0.1:3000/mcp
# health:   http://127.0.0.1:3000/health
```

Optional gate: `MCP_AUTH_TOKEN` (Bearer or `x-api-key`).

## Tool conventions

- Names: `kommo_<entity>_<action>` (e.g. `kommo_leads_list`, `kommo_contacts_create`)
- Responses are JSON envelopes: `{ "data": ... }` and often `pagination: { page, has_next }`
- Errors: `{ "error", "status_code", "detail" }` with MCP `isError: true`
- HAL `_links` stripped and `_embedded` flattened by default (`KOMMO_NORMALIZE_HAL=true`)
- Rate limit: **7 req/s** (client throttles + 429 backoff)
- Destructive tools (`*_delete`, uninstall, etc.) require authorization covering the exact action; reuse an explicit authorization already granted for that scope.

## Resources (read context first)

| URI | Use for |
|-----|---------|
| `kommo://account` | Account metadata, drive URL |
| `kommo://pipelines` | Pipelines + stages (IDs for moves) |
| `kommo://dashboard` | Dashboard snapshot |
| `kommo://custom-fields/{entity}` | Field defs for `leads`, `contacts`, `companies` |

## Prompts

- `kommo_create_lead_with_contact` — complex create + duplicate control
- `kommo_move_lead_stage` — move deal with status/pipeline IDs
- `kommo_find_contact` — search by phone/email/name

## Common workflows

### Find a contact

1. `kommo_contacts_list` with `query` = phone, email, or name
2. If multiple hits, summarize `id` + name + custom fields
3. Optional: `kommo_contacts_get` with `with=leads`

### Create lead + contact

1. Read `kommo://pipelines` and `kommo://custom-fields/contacts`
2. `kommo_leads_complex_create` with lead + `_embedded.contacts`
3. Phone/email via `custom_fields_values` with `field_code` `PHONE` / `EMAIL`

### Move a lead

1. Resolve stage IDs from `kommo://pipelines` or `kommo_pipelines_list`
2. Prefer `kommo_leads_move` (`id`, `status_id`, optional `pipeline_id`, `loss_reason_id`)
3. Or `kommo_leads_update_one`

### Search / filter leads

- Quick text: `kommo_leads_search`
- Filters: `kommo_leads_list` with `filter_pipeline_id`, `filter_status_id`, `filter_created_at_from`/`_to` (unix), etc.

### Analytics

- `kommo_dashboard_get`
- `kommo_sales_report` (`date_from` / `date_to` as `YYYY-MM-DD`)
- `kommo_pipeline_analytics` (native endpoint or client aggregation fallback)
- `kommo_leads_summary`

### Notes / tasks

- Notes: `kommo_notes_create` on `leads|contacts|companies` with `note_type` (e.g. `common`) and `params.text`
- Tasks: `kommo_tasks_create` with `text`, `complete_till` (unix), `entity_id`, `entity_type`

## Domain map (tool families)

| Domain | Prefix examples |
|--------|-----------------|
| Account | `kommo_account_get` |
| Leads | `kommo_leads_*`, `kommo_incoming_leads_*` |
| Contacts / companies | `kommo_contacts_*`, `kommo_companies_*` |
| Pipelines / stages | `kommo_pipelines_*`, `kommo_stages_*` |
| Tasks / notes / tags | `kommo_tasks_*`, `kommo_notes_*`, `kommo_tags_*` |
| Custom fields / catalogs | `kommo_custom_fields_*`, `kommo_catalogs_*`, `kommo_catalog_elements_*` |
| Users / roles | `kommo_users_*`, `kommo_roles_*` |
| Links / events | `kommo_links_*`, `kommo_events_*` |
| Webhooks / Salesbots | `kommo_webhooks_*`, `kommo_salesbots_*` |
| Conversations / calls | `kommo_conversations_*`, `kommo_calls_*` |
| Sources / templates / widgets | `kommo_sources_*`, `kommo_templates_*`, `kommo_widgets_*`, `kommo_crm_plugins_*` |
| Files | `kommo_files_*` |
| Analytics | `kommo_dashboard_get`, `kommo_sales_report`, `kommo_pipeline_analytics`, `kommo_leads_summary` |

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Missing env at startup | Set `KOMMO_SUBDOMAIN` + token or OAuth trio |
| 401 | Check/re-provision an expired or revoked long-lived token; use refresh only for OAuth credentials |
| 403 after many 429s | IP temporarily blocked; slow down / wait |
| Files API fails | Set `KOMMO_DRIVE_URL` or call account with `with=drive_url` |
| Empty lists | Check pipeline/status filters; confirm pagination `has_next` |


## Integração com a engenharia da conta

Este guia documenta um servidor específico; as ferramentas e os schemas disponíveis nesta sessão definem o contrato executável. O número histórico de 152 ferramentas, o envelope normalizado e a taxa documentada não comprovam a instalação, versão ou quota atuais. Use [conexão da conta](../crm/connection.md) e [execução e recuperação](../crm/safe-execution.md) para identidade, direitos, falhas e readback.

- O diagnóstico `scripts/connection-doctor.mjs` recebe `KOMMO_TOKEN`; este servidor documenta `KOMMO_ACCESS_TOKEN`. São contratos de clientes diferentes. Configure a referência segura no processo correto; não renomeie nem duplique segredos por rotina.
- Token de longa duração não tem refresh token. O refresh automático descrito acima pertence ao modo OAuth. Em 401, interrompa chamadas e identifique o modo antes de escolher substituição ou refresh.
- Para Codex, Agy e Claude Code, use os formatos específicos do [guia de acesso](mcp-access-setup.md); não sobrescreva configuração de outro cliente nem instale o servidor por apenas consultar esta referência.
- Recursos `kommo://`, prompts e famílias de ferramentas só são utilizáveis quando o servidor os expõe. Não derive uma operação inexistente pelo padrão do nome.
- Uma resposta pode ser normalizada pelo MCP; não misture seu envelope com o HAL bruto da REST API. Identifique paginação, valores vazios e erros pelo schema observado.
- A instalação da antiga skill via `npx skills add` é uma instrução de distribuição da fonte, preservada no registro de integração; não é necessária para a Kommo Engineer.


## Comparar com outro servidor MCP

Use [transportes e capacidades MCP](mcp-transport-and-capabilities.md) para identificar implementação, versão, stdio/HTTP, health/readiness e schemas reais. O snapshot `Miguelgbastos/Kommo-MCP` tem nomes, configuração e relatórios próprios; não transfira para ele o catálogo desta implementação por semelhança do nome Kommo.
