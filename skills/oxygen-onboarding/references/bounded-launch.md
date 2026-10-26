# Bounded first LinkedIn launch

Use for the admitted dev guided-activation pilot. Preserve the activation's First leads Table, Sequence, creator and selected sender. Resuming reads the existing native resources; it does not create another draft or shortlist. Company/ICP corrections belong to Knowledge/profile owners. Website drafts are hypotheses until confirmed and do not silently authorize claims in outreach copy.

Read `oxygen onboarding activation status --json` (MCP `oxygen_onboarding_activation_status`). If the person chose their own agent and no record exists, `oxygen onboarding activation start --operating-path own_agent --json` creates or resumes it without a chat send, provider call or outreach. The Oxygent path uses `--operating-path oxygent` and also prepares the native workspace Agent and canonical Oxygent chat in the same transaction. This free preparation preserves chat approval settings and sends no Start onboarding message; the deliberate attended entry remains separate. If the native activation already reports `onboarding_start.state: posted`, resume the same chat using its original `turn_id` and optional `event_seq`. A claimed or uncertain receipt needs native chat inspection before retrying Start. These are server-returned provenance fields; activation start still accepts only `operating_path`. Read an exact record with `oxygen onboarding activation get --activation-id <id> --json` (MCP `oxygen_onboarding_activation_get`, `activationId`). An unavailable pilot stays unavailable; never change environment, creator or workspace to bypass admission.

Create or resume the one native First leads Table with `oxygen onboarding activation first-leads --activation-id <id> --json` (MCP `oxygen_onboarding_activation_first_leads`, `activationId`). This free factory discovers no people, enriches nothing and leaves automatic column execution off. Read the actual Table before claiming it is populated. To bind an existing resource, use `oxygen onboarding activation link --activation-id <id> --revision <current-revision> --resource <slot> --resource-id <native-id> --json` (MCP `oxygen_onboarding_activation_link`, fields `activationId`, `revision`, `resource`, `resource_id`). Slots are `knowledge`, `first_leads_table`, `sequence` and `sender`; native ownership and Sequence/source binding are checked. Refresh after a stale revision. Linking grants no outreach authority and accepts no caller-declared completion outcome.

## Draft and review

Keep roughly ten qualified leads, with first messages for three to five. Use stable lead keys and source evidence; apply do-not-contact and contacted exclusions. The selected recipient subset is the audience, not every future row in the Table.

Native authored creation saves supplied LinkedIn steps without inference. Read the current activation revision before reviewing a new draft:

```bash
oxygen sequences create --activation-id <activation> --activation-revision <current-revision> --name '<name>' --slug <slug> --channels linkedin --steps-file <authored-steps.json> --table <bound-first-leads-table> --json
```

The steps file is the existing `{ "steps": [...] }` definition, for example a manually written `message` with `id`, `channel: "linkedin"` and `template`. MCP `oxygen_sequences_create` takes `activation_id`, `activation_revision` (the same current revision), `source_table_id`, `name`, `slug`, `channels: ["linkedin"]` and that `definition`. Native creator/source binding and authored provenance are server-owned; send no metadata or AI receipt. This path has no AI goal or `create` flag. A stale first-create revision refuses; read current onboarding and review again. Initial creation saves an inert draft. Retries recover the same Sequence with its current native status and preserve corrections. Omit sender to keep it senderless; do not enroll the entire Table as a setup shortcut.

For paid AI drafting, `oxygen sequences draft --channel linkedin --goal '<goal>' --table <table> --max-credits <approved-cap> --json` (MCP `oxygen_sequences_draft`, `channel: "linkedin"`) uses confirmed Knowledge and returns grounding provenance. For guided creation, pass `--activation-id <activation>` with `--create --name '<name>' --slug <slug>` and the activation's exact bound Table. MCP uses `activation_id`. The native transaction derives the creator, reuses the existing bound Sequence on retries, and preserves corrections without generating again. Initial creation saves an inert draft; recovery preserves its current status. Generation does not authorize enrollment or outreach. Email remains the default when the channel is omitted. Use authored creation for supplied copy or no-inference fixture setup; invoke AI only when requested and budgeted.

Check plan/seat readiness before connecting. The owner connects their own account through the existing hosted connection; show its actual commitment preview first. Never buy a seat, connect an account or substitute a sender to make validation pass.

Prepare only the reviewed recipients. Enrolling into a draft holds them; enrolling into an active Sequence can send on its next tick and needs its own bounded outreach authority. The pilot uses one exact LinkedIn sender, native invite/message/wait steps, contacted exclusion, reply stop and waiting rather than fallback when the sender is unavailable.

```bash
oxygen sequences start <sequence> --max-live-sends <approved-actions> --max-credits <approved-credits> --json
```

MCP: `oxygen_sequences_start` with `sequence`, `approved: false`, positive `max_live_sends` and nonnegative `max_credits`, through `oxygen_capabilities_read`. This launch check sends nothing. The uncapped `sequences preview` can inspect readiness but cannot create a new bounded review. Read readiness, every selected recipient's personalized steps and variables, exact sender, Knowledge/copy revisions, schedule and caps. Resolve blockers and refresh after any material correction. A connection or an active empty Sequence is not onboarding success.

## Launch the exact review

For a guided Sequence the native response includes `preview.launch_review`: `digest`, `expires_at`, positive `max_live_sends` and nonnegative `max_credits`. Preserve that exact object. The digest binds server-owned actor/activation and material audience, sender, copy, Knowledge and schedule inputs. A zero credit cap still requires the positive action ceiling: LinkedIn sends can cost zero marginal credits and create real external effects.

Show this scope and use the person's explicit launch decision or valid pre-existing auto-approve authority within those same bounds. Where Network Mining runs, only the person can approve it ([day-1 loop](day-one-loop.md)). Save only the returned `launch_review` object to a local JSON file, then:

```bash
oxygen sequences start <sequence> --launch-review-file <review.json> --approved --json
```

`--launch-review-json '<exact object>'` is the inline alternative. MCP `oxygen_sequences_start` takes `sequence`, `approved: true` and the same `launch_review`. Outer credit/action caps may also be echoed but must exactly equal the frozen review; zero credits still requires the positive action bound. No client-calculated digest or broader recipient scope is valid. Expired or changed review inputs require a fresh preview.

Inspect `oxygen sequences stats <sequence> --json` (MCP `oxygen_sequences_stats`) and the native action/run receipts. Report launched, waiting for hours/cap, accepted action, confirmed action, replied and paused separately. A queued job or simulated action does not prove a confirmed live send. Live test outreach requires the exact sender, recipient and action authorization.

After launch, requested recurring work follows the [daily rhythm](daily-rhythm.md). New scan candidates remain review only; no routine expands the approved launch audience.
