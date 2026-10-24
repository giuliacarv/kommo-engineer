# Kommo native AI agents and Salesbots

Use this guide when a request involves the native Kommo AI agent, Salesbots, AI reply suggestions, AI task suggestions, or coordination between them. It helps select and design the right Kommo capability. For live account state, API/UI mechanics, and technical execution, follow the internal `../crm/account-engineering.md` module and current official Kommo documentation.

For a detailed feature reference covering Kommo AI tools and the native AI agent, load [../ai/native-agents.md](../ai/native-agents.md). This guide remains the short architecture overview for selecting and combining AI agents, Salesbots, and deterministic pipeline automation.

For the operating pattern of saving reusable Salesbots without an automatic trigger, manually launching one from a chat, working with JSON, or deciding what belongs in the public API, load [salesbot-playbooks-and-api.md](salesbot-playbooks-and-api.md).

## Select the right capability

| Need | Kommo capability | Operating distinction |
| --- | --- | --- |
| Ask about Kommo, summarize a lead, find unanswered questions, or suggest field values | Kommo Copilot | A user-invoked workspace assistant. Field suggestions are proposals that require review and confirmation. It is not the customer-facing AI agent. |
| Draft a response for a person to review | AI reply suggestions | Produces a suggested reply based on message context and available knowledge sources. The user reviews, edits, and sends it. |
| Detect an action in a chat and propose a follow-up task | AI task suggestions | Proposes a task from conversation text. The user reviews and confirms task creation. |
| Interpret natural-language messages and respond or route using business rules | Native AI agent | Uses Persona, connected knowledge, selected channels/stages, and configured Actions. Some actions can update Kommo or start a Salesbot. |
| Run a fixed, repeatable conversation or internal sequence | Salesbot | A visual flow of explicit steps that runs from configured triggers. Use it when the sequence and transitions should be deterministic. |
| Change records when a known pipeline event or stage occurs | Salesbot or Digital Pipeline automation | Prefer explicit event and field conditions over asking an AI agent to infer system state from chat language. Verify the exact capability in the current account. |

Do not treat these features as interchangeable. Copilot supports a user working in the CRM; an AI reply suggestion is a human-reviewed draft; an AI agent may reply automatically according to its activation settings; a Salesbot follows a configured step flow.

### Copilot and access scope

Kommo Copilot provides Help, Assistant, and Analyst modes. It can answer product questions, summarize lead history, identify unanswered customer questions, and suggest field values from conversation history. Treat a suggested field value as unverified until a person checks and confirms it. Kommo's current Copilot documentation states that Analyst mode can use all workspace data regardless of the individual user's permissions, while other modes follow user access permissions. Verify that the user is authorized to run Analyst mode for the intended data and use case.

## Native AI agent model

- **Persona** describes the agent's role and communication style: tone, reply length, language, delay, and guidelines. Write operational rules that are concrete, bounded, and consistent with the business's approved facts.
- **Sources** provide approved product, service, policy, and FAQ content. Keep ownership and update cadence clear; review active status, last update, use, and which AI features use each source. A use count does not establish factual accuracy. If no active source or connected integration establishes a fact, the agent should ask, abstain, or hand off rather than invent it.
- **Integrations** can expose platform data, such as connected store information, when supported and configured. Do not assume an integration exists or that its data is current; check connection and sync state. The Kommo overview describes synced store data as read-only within Kommo.
- **Actions** use the visible structure **When → Do → More**. When conditions describe conversational intent or message context; Do lists configured operations; More adds action-specific guidance. Keep each action focused on one outcome.
- **Channels, pipeline stages, usage limits, and credits** bound where the agent can operate and how much it can run. Confirm the current selection and remaining limits before launch; a list entry or enabled indicator in an old screenshot is not current-state proof.
- **Preview and dashboard** support testing and monitoring. Preview output is not live-channel proof; inspect the saved configuration and controlled results separately.

### Conditions and branching

The current setup guide lists conditions such as what the client wants, what they ask about, sentiment, information provided, message content, first handling, business hours, and no reply within a configured time. Custom conversational conditions may also be available.

When one action has multiple conditions, decide whether **any** or **all** must match. Treat this as OR or AND logic respectively, and describe boundary examples that should and should not trigger it. The Kommo setup guide reviewed on 20/10/2026 states up to 20 Actions per agent and up to 5 When conditions per Action; these limits are time-sensitive and must be rechecked before implementation.

Do not encode deterministic CRM-state logic as a natural-language condition. Kommo warns that AI conditions may not reliably interpret system logic such as checking a lead tag. Use a Salesbot or pipeline automation for exact tag, stage, owner, or field checks when that functionality is available, then revalidate the handoff to the agent.

### Actions and data writes

The available Do menu can include responding from a knowledge source, asking for information, setting a lead field, managing tags, adding a task, transferring to a user, changing stage or owner, starting a Salesbot, creating a calendar appointment, or sending a file. Availability varies by account, channel, plan, and product changes. Treat screenshots as evidence of a past interface, not a guarantee of present availability.

For every write or handoff, define:

1. The exact condition and which information is known versus missing.
2. The destination field, tag, stage, user, task, calendar, or Salesbot and its verified meaning.
3. Whether to preserve an existing value, how to avoid duplicate tasks, and what happens on retries.
4. The assigned human owner and the point at which the agent or other automation must stop or defer. Verify the actual stop/pause mechanism rather than assuming transfer stops all other flows.
5. The message, summary, or record evidence that will be read back after execution.

Use fields for structured facts, not unverified conclusions. Define exact handling for corrections, ambiguous values, a person speaking on behalf of someone else, and messages with attachments. Do not ask twice for information already present in the conversation or record unless revalidation is part of the intended process.

## Salesbot model

Salesbot uses a visual builder with explicit steps and triggers. Kommo documents trigger families covering pipeline, scheduled, behavior-based, and conversational events. Inspect the trigger location and condition, the complete step graph, its wait/timeout behavior, the terminal step, and any loop or recurring behavior before recommending a change.

A Salesbot may send messages, route conversations, or perform CRM actions according to its steps. Closing a conversation ends its Salesbot flow, and Kommo documents that only one Salesbot can run in a conversation at a time. Check for existing bots and triggers that can run on the same conversation before adding one. When an AI agent starts a Salesbot, define a clear transfer of control, a stop condition, and what happens if the customer replies or a human takes over.

## Design and verification sequence

1. Restate the business outcome, channel, pipeline stage, intended population, owner, and allowed side effects.
2. Read current account configuration: existing agents, channels/stages, sources, integrations, Salesbot triggers and steps, overlapping pipeline rules, human handoff, and plan/credit constraints. Do not infer these from filenames or old screenshots.
3. Choose the capability from the table above. Prefer a deterministic Salesbot or pipeline rule for exact CRM state; use an AI agent for conversation meaning and language-based decisions; use suggestions when a human should decide before sending or creating a task.
4. Specify positive and negative examples, missing-source behavior, duplicate/retry behavior, handoff and stop behavior, and the exact expected CRM readback.
5. Preview or homologate with controlled examples that cover intended triggers, near misses, missing or conflicting facts, repeated events, attachments if relevant, and human takeover. Keep tests away from live external messaging unless the user has authorized it.
6. Make only the change the user authorized. After saving, reopen the exact agent or bot and inspect its trigger/action graph. For a controlled live pilot, inspect run evidence and affected records before expanding scope.
7. Report observed state, verified behavior, untested cases, and the exact disable or rollback path separately.

## Official Kommo references

- [Kommo AI agent overview](https://support.kommo.com/docs/kommo-ai-agent)
- [Set up AI agents](https://support.kommo.com/docs/ai-agent-manual-setup)
- [Add and manage AI knowledge sources](https://support.kommo.com/docs/add-and-manage-ai-knowledge-sources)
- [Create a Salesbot](https://support.kommo.com/docs/create-a-salesbot-in-kommo)
- [Configure Salesbot triggers](https://support.kommo.com/docs/configure-your-salesbot-triggers)
- [Use AI reply suggestions](https://support.kommo.com/docs/work-with-ai-suggestions)
- [Use Task Suggestions](https://support.kommo.com/docs/task-suggestions)
- [Kommo AI overview](https://support.kommo.com/docs/kommo-ai-overview)
- [Use Kommo Copilot to manage lead information](https://support.kommo.com/docs/copilot-ai-use)
