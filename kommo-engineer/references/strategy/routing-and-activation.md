# Specialist routing and activation

Use this map on every invocation of the master skill. It converts the user's requested outcome, provided context, named Kommo capability, intended deliverable, and implementation scope into a small set of internal modules and conditional specialist handoffs.

## Route from intent, inputs, and needs

First determine what result the user wants, not just which terms they used. For each request, identify:

1. **Outcome:** understand/discover, diagnose, design, implement, audit/review, analyze/report, or document/train.
2. **Business need:** the process constraint or user/job-to-be-done that makes the outcome useful; use only context the user supplied or evidence you can verify.
3. **Kommo object or capability:** for example, AI agent, Salesbot, trigger, pipeline stage, lead, contact, field, chat, integration, or metric. If the term can mean different features, inspect context and ask a concise question only when the ambiguity changes the design or side effects.
4. **Inputs and boundaries:** provided files/screenshots, available account or data access, channels, audience, time period, permissions, and what the user has authorized.
5. **Work phase and effects:** read-only analysis vs a draft/proposal vs actual CRM writes, activation, bulk changes, or outbound messages.

Then select **one primary module** for the main problem and add only the companion modules required by the user's needs. Read the selected reference(s) before reasoning from their specialty. A module is activated by opening and applying its internal reference; mentioning a module name is not evidence that it was read, and linking an upstream skill is not invoking it. If a follow-up changes the outcome or scope, route again using the new request plus the still-relevant conversation context.

### User-need to module map

| User intent, input, or need | Load this internal module | Add this companion when needed |
| --- | --- | --- |
| Understand the company, offer, ICP, buyer, current process, or missing business context | [discovery-and-context.md](discovery-and-context.md) | [workflow-architecture.md](workflow-architecture.md) when turning findings into a system/workflow design |
| Decide whether to use a Kommo native AI agent, Salesbot, AI suggestion, or a handoff between them | [../automation/native-automation.md](../automation/native-automation.md) | [../ai/native-agents.md](../ai/native-agents.md) for native AI agent setup, sources, persona, tools, testing, limits, or behavior |
| Learn Kommo AI product behavior or work specifically on native AI agent sources, persona, tools, tests, limits, or monitoring | Load the native AI operating guide at `../ai/operating-guide.md` and read [../ai/native-agents.md](../ai/native-agents.md) | [../automation/native-automation.md](../automation/native-automation.md) if comparing AI with Salesbots/workflows; the internal technical module for account-specific configuration or readback |
| Build a reusable Salesbot playbook; choose manual vs trigger-based execution; design message steps or branches; work with JSON, templates, imports/exports, or Salesbot API limits | [../automation/salesbot-playbooks-and-api.md](../automation/salesbot-playbooks-and-api.md) | [../automation/native-automation.md](../automation/native-automation.md) when the design compares Salesbots with native AI or pipeline automation |
| Design a workflow, trigger, integration, data handoff, system boundary, or failure/retry path | [workflow-architecture.md](workflow-architecture.md) | [../automation/native-automation.md](../automation/native-automation.md) for Kommo-native automation choices; [../automation/governance.md](../automation/governance.md) for live effects, outbound, AI behavior, bulk changes, or rollback |
| Review pipeline stages, stage definitions, funnel health, GTM architecture, or metric formulas | [revops-and-pipeline.md](revops-and-pipeline.md) | [discovery-and-context.md](discovery-and-context.md) if business definitions or ownership are missing |
| Review deals, forecast, lead triage, account context/tiering, CRM hygiene, win/loss, or opportunity updates | [sales-operations.md](sales-operations.md) | [revops-and-pipeline.md](revops-and-pipeline.md) when the request depends on stages, conversion, or forecast definitions |
| Design post-sale onboarding, customer health, retention, churn prevention, support handoff, or expansion | [customer-lifecycle.md](customer-lifecycle.md) | [sales-operations.md](sales-operations.md) when expansion changes an active opportunity or CRM record |
| Plan AI SDR, outbound, bulk edits, activation safeguards, experiment controls, or reversibility | [../automation/governance.md](../automation/governance.md) | [discovery-and-context.md](discovery-and-context.md) for audience, offer, qualification, and business constraints |
| Produce a written operating guide, Mermaid flow, diagram, or visual decision aid | [documentation-and-visuals.md](documentation-and-visuals.md) | Load the underlying business/technical module first when the deliverable must reflect a specific analysis |
| Execute or audit an account-specific Kommo API/UI change, field mapping, data operation, permission check, or readback | No duplicate internal procedure; use the integrated technical module | Also load the relevant design module if the requested operation implements a strategy, Salesbot, AI agent, pipeline, or integration change |

### Selection rules

- Do not activate a module because a single word happens to match. For example, “bot” may mean a native AI agent, a Salesbot, or any automated workflow; use the requested behavior, inputs, and trigger needs to distinguish them.
- Keep the route minimal: one primary module is the default; add a second only when a distinct need requires its method. Multiple modules are appropriate for cross-functional work, not as a checklist to complete on every request.
- Load [discovery-and-context.md](discovery-and-context.md) when the business context is necessary and absent or when discovery itself is requested. Do not force a discovery interview before a narrow technical read or a sufficiently specified task.
- Load [../automation/governance.md](../automation/governance.md) whenever the design or authorized action can send messages, alter records, change routing, affect many records, or activate autonomous behavior. This module adds controls; it does not itself grant authorization.
- Consult the internal technical module for account-specific Kommo mechanics. A plan or mention of an API is not proof of connected tools, token scope, account identity, or write permission.
- If inputs are incomplete, continue with the evidence available and mark assumptions. Ask only for missing information that materially changes the recommendation, recipient/audience, API/UI operation, or side effect; do independent read-only work while awaiting that answer.
- If the request is narrow and technical, route directly to the internal technical module rather than making the strategic layer perform a full diagnosis.

### Route examples

| Example request | Route |
| --- | --- |
| “Quero que a IA qualifique leads e passe os casos prontos para um vendedor.” | `../automation/native-automation.md` + `../ai/native-agents.md` + `workflow-architecture.md`; add discovery only if the qualification process is unknown, governance if messages or autonomous actions are in scope, and the internal technical module for live account changes. |
| “Monte um Salesbot manual com áudio e catálogo para a equipe enviar no chat.” | `../automation/salesbot-playbooks-and-api.md`; add discovery if audience/offer/message strategy is missing, governance if outbound message behavior is being designed, and the internal technical module if creating or verifying it in an account. |
| “Por que caiu a conversão entre as etapas do funil?” | `revops-and-pipeline.md` + `sales-operations.md`; add discovery if stage definitions or commercial context are unclear. |
| “Atualize o campo X pela API nesta conta.” | Route directly to the internal technical module; do not load strategic modules unless the requested field change implements a broader workflow decision. |

### Lightweight routing output

For complex or cross-functional requests, state the route briefly before the analysis (for example, “Vou usar descoberta + arquitetura de workflow + governança, porque você quer desenhar uma automação com saída para clientes”). For a simple request, apply the route silently and answer directly. Do not expose internal file loading as a substitute for evidence or results.

## Know which layer you are invoking

| Layer | How it is made available | What this skill should do |
| --- | --- | --- |
| Internal specialist playbook | A Markdown file under this skill's `references/`; it is not a separate Codex skill. | Read the relevant module and apply its adapted method. |
| Independent Codex skill | A skill listed in the current Codex skill picker or otherwise confirmed installed in the current environment. | Invoke or consult it only when the task materially needs its specialty. Availability in another chat, profile, or repository does not prove availability here. |
| Connector, MCP, API, or UI tool | A tool actually enabled in the current chat with the needed scope. | Inspect its current capabilities and permissions before relying on it. A skill or source link does not grant tool access. |
| Upstream repository link | An upstream source cited in the relevant internal reference or in `docs/content-integration.json`; an external source register is not required. | Use as research/attribution; do not treat the page as an installed skill or executable agent. |

Reading an internal playbook is how this orchestrator activates that specialty. Do not claim to have invoked a separate upstream skill unless Codex actually exposes that skill in this conversation. Never assume that an external GitHub URL can be loaded as a local skill or that a connector from another task is available.

## Route the supplied sources

The item numbers below preserve the historical source mapping from the original strategy material. They are provenance labels, not a new task, a current source inventory, or additional work authorization. Read only the mapped module(s) relevant to the request.

| Source items | Internal module | Use for |
| --- | --- | --- |
| 0 | [discovery-and-context.md](discovery-and-context.md) | Company, offer, ICP, process context, evidence, and assumptions |
| 1, 2, 21, 22 | [workflow-architecture.md](workflow-architecture.md); [../automation/governance.md](../automation/governance.md) when writes, AI, or bulk changes are involved | Workflow and CRM integration design; reliability, dry-run, approval, batch, and recovery concepts |
| 3, 4, 6, 9 | [revops-and-pipeline.md](revops-and-pipeline.md) | RevOps, stage management, system architecture, and metric definitions |
| 5, 7 | [customer-lifecycle.md](customer-lifecycle.md) | Post-sale lifecycle and customer-success patterns; item 7 is a duplicate of item 5 |
| 8 | [../automation/governance.md](../automation/governance.md) | AI SDR pilot and outbound automation controls |
| 10a, 10c | [documentation-and-visuals.md](documentation-and-visuals.md) | Written and visual deliverables; use available Codex documentation skills when useful |
| 10b | No bundled module | Link only; license was not confirmed and no source text is redistributed |
| 11–18, 20 | [sales-operations.md](sales-operations.md) | Pipeline, hygiene, win/loss, deal review, forecast, triage, tiering, context, and explicit opportunity updates |
| 19 | [customer-lifecycle.md](customer-lifecycle.md); [sales-operations.md](sales-operations.md) when an existing opportunity or CRM update is in scope | Expansion evidence and handoff to sales operations |

## Use other available Codex specialists only when they help

- For Kommo API, UI, account data, mappings, or technical write/readback, use the integrated technical module at `../crm/account-engineering.md` as the authority. Those internal references contain the account procedures; no separate Kommo skill needs to be invoked.
- For an ordinary reference or guide, consult `markdown-docs` only if it is available in this Codex environment and the output warrants that specialty.
- For a Markdown visual, consult `documd-visuals` only if it is currently available and a visual artifact improves the requested result.
- For skill authoring or package validation, consult `skill-creator` when available.
- For any other specialty, check current skill availability and task fit first. If none is installed, use the relevant internal playbook, narrow the deliverable, or explain the missing capability; never invent an activation.

These are conditional handoffs, not mandatory dependencies. Do not load every skill or tool for a request that one playbook and one verified data source can answer.

## When a source should become its own Codex skill

Keep a method as an internal reference when it is mainly a reusable analytical lens, overlaps other sources, assumes another CRM, or lacks a distinct reusable interface. Create a separately invokable skill only when there is a recurring user task with a clear trigger, distinct deliverable, and self-contained instructions that justify another picker entry. Write original, license-aware guidance; a source link does not grant permission to copy a skill package.
