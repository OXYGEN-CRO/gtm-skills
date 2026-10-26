# Workflow budget state

Inspect the trigger metadata and `trigger.automationPaused` with
`oxygen workflows get <slug> --json` before explaining a refusal or resumption.

Null legacy `included_actions` / `remaining_actions` values never mean unlimited
credits. Numeric values describe an action quota; current plans use workspace
credits, run ceilings and applicable budget policies. `overage_enabled: false`
with null action fields does not create a monthly action allowance. A null
allowance object means its lookup is unavailable.

A hard budget refusal skips due cron slots before creating runs, keeps the
trigger armed and records `scheduler_budget_block_reason` and
`scheduler_budget_blocked_at` in trigger metadata. Warning policies allow
admission. After the window resets or the cap is raised, later slots can run;
skipped slots are not replayed.

`trigger.automationPaused` reports quota/credit admission pauses. Monthly quota
pauses have a reset time; credit or unknown refusals have no promised resume date.
Adding credits permits a future retry; manually disabled Workflows stay disabled.
