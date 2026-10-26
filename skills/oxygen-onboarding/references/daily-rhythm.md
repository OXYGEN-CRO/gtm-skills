# Daily Oxygent routines

Reach this guide when the person requests recurring lead discovery or a morning briefing. Finishing onboarding arms no schedules. Guided routines require enabled onboarding and current non-client workspace membership; production uses the normal subscription entitlement. A missing routine/chat prerequisite or reviewed sourcing capability leaves setup unavailable; use its native readiness result.

## Establish the scope

Read `oxygen onboarding activation status --json` (MCP `oxygen_onboarding_activation_status`) first. Its `resources.oxygent`, `resources.direct_chat`, `resources.scan_routine` and `resources.briefing_routine` identify the existing destinations and sessions without loading chat snippets. Reuse those pointers, the First leads Table and Sequence on resume. Read only the native resource needed for the next action.

If the Oxygent handle is already known, `oxygen oxygents routines --slug <oxygent> --json` lists the creator's existing routines and `oxygen agent session templates --slug <oxygent> --json` reads the reviewed config/template catalog. MCP: `oxygen_oxygents_routines`, `oxygen_agent_session_templates`. Hydrate schemas through capability discovery when outside the connected toolset. `oxygents list` includes chat snippets; use it only when reading that chat content is within scope, not solely to discover a report destination.

For the chosen Oxygent path, `oxygen onboarding activation start --operating-path oxygent` prepares native Agent/canonical-chat bindings without an attended message or inference. Reuse an existing valid published workspace Agent version. For the untouched factory draft, the explicit reviewed `oxygen onboarding activation routines-preview` action below prepares its scoped immutable version and both routine drafts together. Page visits and GETs leave the draft untouched. Paused, customized, historical or mismatched versions require native review; preserve that refusal and existing policies. Retain chat approval settings and exact tool/spend bounds; setup needs no attended onboarding turn or invented model credentials.

Use the Oxygent’s canonical direct chat. Workspace Oxygents share this history; Personal Oxygents are creator-only. A separate group chat is not the destination. If a required native pointer or handle is missing, explain that configuration gap; never guess an ID or read private conversation history to manufacture the binding.

Collect the confirmed IANA timezone, the approved source scope and company/ICP revisions, the exact First leads Table and Sequence, and the budget for each routine. Suggest **02:00** for the scan and **08:30** for the briefing in that timezone; these are editable suggestions. CLI/MCP clients must ask for the timezone when it is unknown. UTC is not a fallback for a local time the person named.

The two purposes are independently configured and pausable:

- **Nightly lead scan:** bounded approved discovery into the First leads Table. Set a positive new-lead ceiling and quote inference, provider and asynchronous child costs. Persist source evidence and scan status. Every new candidate is review only; adding someone to a running Sequence is a separate outreach decision.
- **Morning briefing:** read the bound Table, Sequence and scan results and post once per local day to the Oxygent’s canonical chat. Include the covered period, freshness, new qualified people, confirmed/accepted outreach and replies, waiting reasons, charges and holds, source links and one next action. A missing, failed, partial or still-running scan differs from a completed scan with zero new leads. The briefing does no new search or outreach.

## Review and activate

Use the native setup producer to build both drafts and their complete previews. It derives the configuration, resources, creator-chat binding and source policy from native owners. Source IDs are the original reviewed native ingestion IDs or `table:<native-source-Table-uuid>` for a watermark source; the source Table differs from the destination First leads Table. Copied preview rows do not authorize provider continuation. Every flag below is required; substitute the person's confirmed scope and caps:

```bash
oxygen onboarding activation routines-preview --activation-id <activation> --revision <activation-revision> \
  --timezone <IANA-zone> --timezone-confirmed --scan-time <HH:mm> --briefing-time <HH:mm> \
  --source-ids <native-source-ids> --max-examined <n> --max-new-leads <n> \
  --max-provider-pages <n> --max-provider-credits <cap> \
  --scan-per-run-credits <cap> --scan-daily-credits <cap> \
  --briefing-per-run-credits <cap> --briefing-daily-credits <cap> --json
```

MCP `oxygen_onboarding_activation_routines_preview` takes `activationId` and the same fields in snake_case. It returns `scan` and `briefing`, each with native `session`, `preview`, `quote`, permitted `native_effects` and links; `delivery` is `oxygent_chat_only`. Creating these drafts starts no inference and arms no schedule. Changed configuration pauses the session and invalidates previous authority. Daily caps must cover a run, and the scan per-run cap must cover its provider ceiling. A positive parent cap remains required even when the native Table-source provider/inference quote is zero.

Show the complete native source policy, configuration, resource IDs, schedule and provider/inference/parent cap quote. The guided scan marker carries `activation_id`, `purpose: lead_scan` and native `scan_policy`; the briefing uses `purpose: morning_briefing` and `teammate_routine.report_policy: periodic` so zero-new-lead or missed-scan periods still report. The scan uses `changes_only`. Never construct policy digests or authority in the client. Re-proposing setup reuses one routine per activation, creator and purpose. Existing `oxygen agent session preview --slug <oxygent> --session <session> --json` / `oxygen_agent_session_preview` can inspect either session again.

Show the exact costs and permitted actions. Activation runs on the server while the browser is closed; each wake stays inside its approved caps. Ask mode collects the person's decision. Valid existing auto-approve authority can answer the operation approval for requested, fully configured work; missing resources, timezone or caps are configuration questions. Material changes require a fresh preview.

```bash
oxygen onboarding activation routine-activate --activation-id <activation> --purpose <lead_scan|morning_briefing> --revision <purpose-preview-revision> --preview-token <purpose-preview-token> --approved --json
```

MCP `oxygen_onboarding_activation_routine_activate` takes `activationId`, `purpose`, `revision`, `preview_token` and the approval decision. A trusted current canonical Oxygent chat with valid paid auto-approve authority may omit `approved`; the server validates that identity and existing policy. Other clients supply the explicit decision. Never send caller-defined chat identity or auto-approve fields. Add `approve_above_default` only when that separate higher-cap decision is authorized. Activate the scan and briefing separately; one successful activation does not prove the other is ready.

## Inspect and pause

```bash
oxygen agent session get --slug <oxygent> --session <session> --json
oxygen agent session pause --slug <oxygent> --session <session> --json
oxygen agent session resume --slug <oxygent> --session <session> --json
```

MCP uses `oxygen_agent_session_get`, `oxygen_agent_session_pause` and `oxygen_agent_session_resume`. Only the creator may configure, activate, resume or run their routine; workspace members retain the native pause brake. Pausing one purpose leaves the other independently inspectable. Resume requires unchanged approved configuration. For a timezone change, review the new schedule and explicit next occurrence before activation.

Inspect a returned run ID with `oxygen agent run-get <oxygent> <run-id> --json`; MCP `oxygen_agent_run_get` takes `slug` and `run_id`. For the admitted current creator, session history exposes `runs[].output.guided_activation` and the run read exposes `run.output.guided_activation`. These persisted receipts identify the exact occurrence and its `manual` or `scheduled` origin. Scan receipts retain the saved snapshot, source progress, checkpoint and credit facts; briefing receipts retain the saved snapshot and shared-chat post reference, without post text. An omitted receipt or `snapshot: null` is not a completed zero-result scan. Preserve unresolved holds and unverified coverage; a manual receipt never proves the scheduled occurrence.

An explicit **Run now** uses the existing session operation with its own bounded preview:

```bash
oxygen agent session run --slug <oxygent> --session <session> --no-approved --json
oxygen agent session run --slug <oxygent> --session <session> --revision <preview-session-revision> --preview-token <preview-token> --approved --json
```

MCP `oxygen_agent_session_run` uses `approved: false` for preview, then `approved: true`, `revision` and `preview_token` for the exact decision. Show its current source/configuration and cap before executing. The server creates a distinct approved manual receipt; a retry with that receipt reuses its logical work and leaves the scheduled local-date occurrence separate. Changed or expired review needs a fresh preview. Do not clone the routine to force a second scheduled occurrence. After a missed local time, show the missed scan and offer the bounded manual operation rather than replaying a backlog. Confirm the saved report/post and unread state before calling a briefing delivered; a queued run is not delivery.
