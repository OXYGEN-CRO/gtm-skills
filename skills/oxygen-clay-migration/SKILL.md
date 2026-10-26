---
name: oxygen-clay-migration
description: "Move a Clay workspace into OXYGEN through browser sign-in: discover accessible resources, transfer data, rebuild native Tables, Records and Workflows, and verify coverage. Also handles a user-supplied Clay export."
allowed-tools: Bash(oxygen *)
---

# OXYGEN Clay migration

Use `oxygen_clay_migration` (CLI: `oxygen clay migration`) for the hosted Clay connection, source inspection, bulk transfer and durable migration ledger. Rebuild behavior with existing native Oxygen tools; the connector does not translate workflows. Column mechanics come from the `oxygen-tables` dependency; [the walkthrough](references/clay-migration.md) covers reconstruction and recovery.

## Start and continue

- For a workspace migration, use `connect` and present its browser verification link/code. Customers need no installed Clay CLI, copied credentials or terminal commands. Check `status` after they sign in; connect never proves authorization by itself.
- Use `discover` to inventory the selected source workspace, following returned cursors. Inspect configuration with `read`. Account for every accessible resource, including folders, tables, Audiences, functions, Claygents, schedules and workflows; exposed types and fields determine actual coverage.
- Keep bulk rows outside model context: use `transfer` for table and Audience rows into newly created native Tables, retaining original outputs and source configuration. Verify source/export/destination counts and extraction completeness before rebuilding downstream behavior.
- Check the migration ledger before resuming. Save source-to-destination identities, reconstruction choices, verification and unresolved items with `checkpoint`; its report is the handoff across conversations. A transfer checkpoint does not prove that formulas or workflows were rebuilt.

## Rebuild and reconcile

Port recovered formulas, prompts, dependencies and conditions into native columns, Functions or draft hosted Workflows using their existing validators. Create destination skeletons before cross-table references. Discover current tools and providers instead of assuming the Clay provider exists. Explain meaningful substitutions and obtain acceptance before applying them; mark missing source logic as an approximation, never a recovered original.

Request the `oxygen-crm`, `oxygen-enrichment`, `oxygen-workflow-authoring` or `oxygen-knowledge` skill by name when its primitive is needed. Accessible records and configuration can be preserved even when executable behavior cannot be reconstructed. Finish with `report` plus native readback: link created objects, state counts and explain every remaining unsupported, inaccessible, partial or undecided item. Claim completion only for verified coverage.

## Gates

- Import authorization covers the requested internal reconstruction, not paid execution or external writes. Keep auto-run, feeds, schedules and sends inactive; creation must not enroll rows or contact anyone.
- Every paid pilot needs the current native preview, exact rows/columns, a credit ceiling and approval. Compare Clay cost only when source evidence exposes it. A non-GET HTTP action needs separate external-write approval.
- Keep imported Clay outputs and provenance separate from new Oxygen run results. Do not clear source originals to make a rebuilt column writable.
- Never overwrite existing destination objects by default. Ask about material data loss, missing connections or substitutions; continue independent safe migration work while a choice is pending.
- A CSV-only import is an explicit fallback for a user-supplied export, not proof of workspace migration or configuration recovery. Report connection/export limitations instead of silently switching paths. Disconnect temporary Clay access when finished or cancelled.

Plays: [migrate-from-clay](plays/migrate-from-clay.md).
