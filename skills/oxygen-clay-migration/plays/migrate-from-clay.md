# Migrate from Clay

## The Play

Ask an Oxygent to move the accessible Clay workspace into Oxygen. It connects through browser sign-in, inspects the source and recreates supported behavior through native Tables, Records, Functions and draft Workflows. Every discovered resource ends with a verified disposition; an unsupported configuration or partial export is never reported as a complete migration.

## Before You Start

- Open **Tables → Import from Clay**, or send this play's prompt to your Oxygent. Load the `oxygen-clay-migration` skill for connector and reconstruction guidance.
- Sign into the Clay workspace through the returned verification link/code. No customer CLI install, copied token or terminal command is needed. Verify the connected identity before selecting the workspace.
- Check Oxygen workspace capacity and the conversation credit balance. Migration authorization does not authorize paid columns, schedules, feeds or external actions.

## Steps

1. Connect and inspect using the hosted `oxygen_clay_migration` tool. CLI agents use the same contract:
   ```bash
   oxygen clay migration --action connect --json
   oxygen clay migration --action status --migration-id <migration-id> --json
   oxygen clay migration --action discover --migration-id <migration-id> --json
   ```
   Follow discovery cursors, inspect configuration and bounded samples, and show the inventory, source limitations and proposed native objects.
2. Create destination skeletons and typed preservation columns through the existing native tools. Transfer bulk values outside chat, retaining original Clay outputs, source IDs and configuration. Check source/export/destination counts before rebuilding downstream behavior.
3. Rebuild supported formulas, prompts, dependencies, relations and orchestration through native validators. Use recovered source definitions where exposed. Missing logic stays labelled as an approximation.
> APPROVAL GATE — replacement-choice: explain material behavior differences and obtain acceptance before applying substitutions. Preserve accessible data while a decision is pending.
4. Checkpoint source-to-destination identities, reconstruction choices and verification results. Resume from the migration ledger rather than creating duplicate objects. Keep new paid columns, schedules, feeds and sends inactive.
5. Reconcile every discovered resource, link created objects and state any unsupported, inaccessible, partial or undecided items:
   ```bash
   oxygen clay migration --action report --migration-id <migration-id> --json
   ```
   Verify original values and deterministic sample outputs through native readback. Disconnect temporary Clay access when finished or cancelled.
> APPROVAL GATE — enrich-pilot: an optional paid comparison needs the native preview, exact row/column scope, current credit estimate and a separately approved ceiling. Imported Clay outputs are historical data, never new Oxygen execution receipts.
6. Only if requested, run the approved pilot and compare results and billing receipts. Compare Clay cost only when source evidence or the user supplies it; never equate one Clay credit with one Oxygen credit.
> APPROVAL GATE — enrich-fanout: show the remaining row/column scope, current estimate and ceiling before any paid batch. Migration completion alone does not authorize it.

## If It Goes Wrong

- Authentication expires or access is refused: reconnect through browser sign-in and verify the source identity; existing imported data remains intact.
- Export or row counts are partial: report the boundary, resume from the returned cursor/checkpoint where possible, and leave coverage incomplete.
- A provider or behavior has no native equivalent: inspect current capabilities, propose the closest supported replacement and wait for acceptance.
- If the user explicitly supplies or chooses a CSV, import its values through Tables and use the migration skill's CSV fallback. A file does not prove workspace inventory or recover formulas, prompts, provider settings or schedules.
