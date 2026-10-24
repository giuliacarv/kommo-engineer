# Workflow and CRM integration architecture

Use for new or revised routing, integrations, automations, lifecycle logic, field changes, or handoffs between systems. This is a design checklist; Kommo-specific mechanics are defined in [account engineering](../crm/account-engineering.md).

## Specify the workflow

Document these dimensions before recommending implementation:

| Dimension | Decision to make |
| --- | --- |
| Outcome | What user or customer outcome changes? |
| Trigger | Which event starts the workflow, and how is it observed? |
| Eligibility | Which records qualify at trigger time? |
| Exclusions | Which opt-outs, duplicates, closed records, existing owners, or other states must stop it? Base conditions on verified fields and policy. |
| Data | What is read/written, what is the source of truth, and who owns each field? |
| Logic | What deterministic rules or model decisions apply? How are unknown/conflicting values handled? |
| Action | What exactly happens, in which system/channel, and under whose identity? |
| Handoff | When does a human take ownership, and how does automation pause or stop? |
| Reliability | How are duplicates, retries, timeouts, partial failures, and repeated events handled? |
| Observability | Which run state, errors, outcomes, and audit evidence are retained? |
| Recovery | How is the workflow disabled, the prior state restored, or affected records reconciled? |

## Data and integration rules

- Name the authoritative source for each business fact; do not assume the CRM is the source for every field.
- Resolve identity and deduplication before creating or updating entities. Preserve ambiguous records for review rather than inventing mappings.
- Define field ownership and write precedence. Before changing an existing field, inspect its current semantics, dependencies, and consumers.
- Treat enrichment as a proposed observation with provenance and timestamp, not as verified identity by default.
- Describe synchronization direction, conflict behavior, lag tolerance, and backfill separately. A one-way event hook is not a complete sync design.
- Estimate expected volume and failure cost from actual evidence. Do not invent API limits, latency guarantees, or costs.

## Idempotency and recovery

For any retryable action, specify a stable idempotency key or an equivalent duplicate guard. Distinguish retryable from permanent errors, cap retries, and define a visible failure queue or owner. For multi-step changes, record checkpoints and the exact compensating action for each completed step. If no safe rollback exists, call that out before approval.

## Platform translation

General workflow concepts transfer across CRMs; commands, object models, APIs, and permission models do not. Translate an approved design through the internal account-engineering references and current official documentation for each affected platform. Never copy HubSpot CLI instructions, Salesforce object assumptions, or another vendor's tool schemas into a Kommo runbook.
