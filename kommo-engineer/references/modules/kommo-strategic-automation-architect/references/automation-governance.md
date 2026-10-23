# Automation governance, AI SDR, and bulk changes

Use for outreach automation, agent-assisted sales, high-volume workflow updates, migrations, or changes with meaningful customer or operational impact.

## Pilot before scaling

Define the eligible segment, volume limit, owner, observation window, control group or baseline when feasible, human review, pause conditions, and stop criteria. Verify identity, personalization evidence, contact permission, opt-out/suppression, channel ownership, and human handoff before any outbound action. The presence of an AI SDR playbook is not permission to send messages.

## Bulk operations

Before a bulk write, inventory the exact target set, current values, proposed values, matching rule, exclusions, and expected count. Produce a dry-run summary and digest of intended changes. Preserve an export or reversible checkpoint where allowed. Apply in bounded batches with checkpoints and a stop-on-mismatch rule. Read back the exact targets and reconcile count, changed values, skipped rows, and failures.

Never infer a target set from a broad label or stale count. Do not convert incomplete identity into new CRM entities. If the preview cannot prove target membership and intended field/entity mapping, stop and present the unresolved rows.

## AI and assisted decisions

Name which decisions are deterministic and which are model-assisted. For model-assisted decisions, record inputs, evidence requirements, confidence/abstention behavior, human review point, and prohibited actions. Do not let generated text create unsupported claims about a lead or customer. A human handoff must have an owner, visible reason, and a way to suspend automation.

## Activation and rollback

For go-live, specify exact workflow/version, account, segment, activation time, monitors, owner, and disable procedure. Verify the saved configuration after activation and inspect early executions before increasing scope. When rollback is requested or a stop threshold is met, disable the exact workflow and verify its paused state; then reconcile pending or partially completed actions with the owner. Do not assert a message was delivered because a workflow ran or a tool call succeeded.
