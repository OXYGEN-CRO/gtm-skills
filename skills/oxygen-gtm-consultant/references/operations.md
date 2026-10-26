# Operational improvements

Use when the constraint is converting or operating existing demand, rather than finding more people. These are optional diagnostic examples; combine them to fit the user's process.

**Lead qualification and routing.** Inspect a bounded sample of available intake and assignment evidence. Locate where an eligible lead waits, who owns the next action, and what qualifies it. Start with one intake path and a clear owner or fallback. Records hold durable identity and activities; Tables can evaluate working qualification; Workflows own deterministic routing. Ask about responsibility when the data does not establish it. Measure time to assignment and the share of eligible leads with an owner, not just records processed.

**Follow-up and handoffs.** Distinguish unanswered existing conversations from net-new outreach. Use `oxygen-unibox` for existing-thread work and `oxygen-sequencer` for an approved outreach cadence. A hosted Workflow can connect intake, qualification and a next-action handoff when those capabilities exist. Check suppression, replies, active sequences and ownership before proposing automation that might duplicate contact. Start with one queue or segment; measure time to first response, overdue follow-ups or qualified conversations recovered. Do not promise a response SLA before learning the team's coverage.

**Data quality and recurring work.** Trace an operational symptom to its owner: duplicate canonical contacts belong to Records, working column cleanup to Tables, recurring deterministic steps to Workflows, and bounded adaptive judgment to Agents. Read `oxygen-table-tidy` or `oxygen-workflow-authoring` only when those needs arise. Prefer a small correction at the source over adding another sync. Measure manual minutes, failure rate or records needing repair against an observed baseline.

A composite improvement need not match a named play. Explain which native capabilities can implement it, what remains unknown, and the smallest validation. Do not create an unnecessary Table, sequence or scheduled agent simply to demonstrate product features.
