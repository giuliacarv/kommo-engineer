---
name: kommo-mcp
description: >-
  Operate Kommo CRM via the runitsolutions/kommo-mcp MCP server (152 tools).
  Use when configuring, debugging, or using Kommo/amoCRM through MCP tools;
  managing leads, contacts, companies, pipelines, tasks, notes, files,
  conversations, Salesbots, webhooks, or analytics; or setting up Cursor MCP
  with KOMMO_SUBDOMAIN / KOMMO_ACCESS_TOKEN / OAuth refresh.
license: MIT
metadata:
  author: runitsolutions
  version: "1.1.0"
  repository: https://github.com/runitsolutions/kommo-mcp
---

> **Codex portability note:** This package contains skill instructions only. It does not install, build, or configure the runitsolutions MCP server or credentials. In Codex, use only Kommo tools actually present in the current session. Treat setup commands as documentation and never expose tokens.


# Kommo MCP

Guide for using **runitsolutions/kommo-mcp** — a TypeScript MCP server that wraps Kommo CRM API v4 (plus Files, Conversations, analytics).

Official API docs: https://developers.kommo.com/  
Server repo: https://github.com/runitsolutions/kommo-mcp

## When this skill applies

- User wants to control Kommo/amoCRM from Cursor (or another MCP client)
- Need to install/configure the MCP server
- Need the right tool for leads, contacts, pipelines, tasks, notes, files, talks, Salesbots, webhooks, catalogs, custom fields, or reports

Prefer MCP tools over inventing raw `curl` calls once the server is configured.

## Install the MCP in Cursor

1. Clone and build:

```bash
git clone git@github.com:runitsolutions/kommo-mcp.git
cd kommo-mcp
npm install
npm run build
```

2. Create a private integration in Kommo (**Settings → Integrations**) and generate a **long-lived token** (leave Redirect URL empty), or use OAuth refresh credentials.

3. Add to Cursor MCP settings:

```json
{
  "mcpServers": {
    "kommo": {
      "command": "node",
      "args": ["/absolute/path/to/kommo-mcp/dist/index.js"],
      "env": {
        "KOMMO_SUBDOMAIN": "your-subdomain",
        "KOMMO_ACCESS_TOKEN": "your-long-lived-token"
      }
    }
  }
}
```

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
- Confirm with the user before destructive tools (`*_delete`, uninstall, etc.)

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
| 401 | Refresh long-lived token or configure OAuth refresh |
| 403 after many 429s | IP temporarily blocked; slow down / wait |
| Files API fails | Set `KOMMO_DRIVE_URL` or call account with `with=drive_url` |
| Empty lists | Check pipeline/status filters; confirm pagination `has_next` |

## Install this skill (skills.sh)

```bash
npx skills add runitsolutions/kommo-mcp --skill kommo-mcp -a cursor -y --copy
```

Project-level install from the repo root; use `-g` for user-global.
