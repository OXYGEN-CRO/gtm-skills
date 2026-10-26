# Workspace context: resolve, fill, pin

Use this when a task depends on company, ICP, positioning or offer context and the workspace profile is empty or too thin. A first session with a new user is the `oxygen-onboarding` skill; this page is the mechanics underneath.

## Is there enough context?

```bash
oxygen knowledge resolve --purpose general --require-ready --json
oxygen knowledge bootstrap status --json
```

Pick the closest purpose: `lead_sourcing`, `qualification`, `outbound_copy`, `workflow_design` (`onboarding` reads without a readiness gate). MCP: `oxygen_context_resolve`. Context is insufficient when the resolver returns `context_missing`, `missing_required_context` or a non-empty `missing_fields` for the decision at hand; ask only for what would change it. An eligible workspace is researched once automatically at signup, so a `[[company-research]]` page and a partly filled profile may already exist to correct rather than recreate: `bootstrap status` answers that in one free call. The older `oxygen context ...` commands are aliases of `oxygen knowledge ...`.

## Fill it from public sources (free, the default)

1. Identify the company from its website, or its LinkedIn company page when it has none. A creator's personal LinkedIn profile describes the person, not the company: keep it out of the company research.
2. Draft from the website, public pages and what the user provides. Reading public pages yourself costs the user nothing; a provider call costs credits. During this draft, write nothing to the CRM, outbound tools, public sites or tables, and mark what you could not confirm as unknown.
3. Store new inference as draft research, not confirmed profile truth. An explicit user correction authorizes the matching profile patch at once: preserve unrelated fields and read it back.

```bash
oxygen knowledge profile update --data-json '<approved_profile_patch>' --summary '<one paragraph of current GTM context>' --json
oxygen knowledge seed --json
oxygen knowledge page upsert --slug icp --type strategy --title "ICP" --status active --tags "icp" --summary "<one line>" --body "<... link [[offers]]>" --json
```

MCP: `oxygen_context_profile_update` with `profile` and an optional `summary`. `seed` is idempotent and usually a no-op on a new workspace: it creates the draft `[[icp]]` and `[[offers]]` stubs and nothing else. Filling a stub and setting `status: active` needs no approval; keep its `[[wikilinks]]`. Create any other page, such as positioning or personas, only when there is real content for it. Save source notes as a `research_note` page when they are worth keeping.

A minimal profile patch has `company` (name, domain, category, target geography, stage), `offering` (product, value proposition, use cases, proof points), `icp` (target accounts, buyer and user personas, disqualifiers), `market` (competitors, alternatives, categories), `gtm_stack` (CRM, outbound tools, channels) and `custom` (constraints, tone, preferences, open questions). Use user-provided or confirmed values; keep researched hypotheses in draft pages.

## Pin canonical brand, voice and positioning

The pinned canonical **voice**, **brand** and **positioning** pages are prepended to every AI message column, background and bulk copy run and inbox reply draft, so nobody pastes voice rules into each prompt. Pinning is approval-gated: **`knowledge page pin` always files a proposal** (a client `--approved` is never honored), and the pin takes effect when that proposal is approved after the user signs off on the content.

```bash
oxygen knowledge page upsert --slug voice --type voice --title "Voice & tone" --status active --body "<how we write: register, rhythm, words to use and avoid, examples>" --json
oxygen knowledge page pin voice --json
oxygen knowledge proposals approve <proposal_id> --json
```

To see what AI copy uses right now, read `oxygen context canonical get --type voice --json` (MCP: `oxygen_context_canonical_get`; free). With nothing pinned it returns `present: false` and `grounding_when_absent`, which says what AI copy uses instead.

Repeat for `--type brand` and `--type positioning`. One canonical page per type; re-pinning another page files a new proposal. Persona pages (`--type persona`) are read on demand, not auto-injected. `knowledge resolve` lists `context.available`, each page with its `state` (`canonical`, `draft` or `active`; only canonical copy is applied), and `context.missing`, each type with no canonical copy; the MCP resources `context://voice`, `context://brand` and `context://positioning` return the raw markdown. A voice learned from the workspace's own sent messages: `knowledge synthesize --kind voice` (this skill's `SKILL.md`). How a column reports what it applied: the `oxygen-tables` skill, `references/ai-columns.md`.

## Paid alternative: `oxygen knowledge bootstrap --live`

When the user explicitly asks OXYGEN to do the research itself, one capped, provider-backed pass exists:

```bash
oxygen knowledge bootstrap status --json
oxygen knowledge bootstrap --domain acme.com --json
oxygen knowledge bootstrap --domain acme.com --live --max-credits <preview_ceiling> --json
```

A status with `effect_outcome: unknown` has an unconfirmed lookup outcome or spend, and `credits_used` is `null`, not zero. A completed pass with `research_available: true` still has usable saved output: read its Run and cited pages. Credit figures in the saved note are the original reported amounts, so they do not settle the current uncertainty. Inspect the Run's provider events in Observability and share the Run ID with Oxygen support for review before starting another pass; do not infer the unknown lookup from a failed event or force a repeat. A `running` marker with reason `worker_outcome_requires_recovery` is a stopped pass, not research in progress, and it will not resume.

Status and free preview include `bootstrap.funding`. Explicit platform-funding ledger evidence can establish `source: oxygen` and `customer_credits_charged: 0` while the supplier outcome and total `credits_used` remain unknown. Missing or conflicting evidence reports funding as unknown. This projection reads without applying grants or expiry; do not use maintenance-capable billing usage/audit for a strictly read-only task. Billing summary's `trialCreditBudget` names the configured subscription-trial allowance, which is distinct from actual signup grants and the current available balance.

A LinkedIn step's `fallbackUsed` can mean falling back from a domain lookup to the company page linked by its own website, through the same tool. Matching tool names alone do not establish an identical-request retry or identify the unconfirmed lookup.

- **`status` first, free.** The workspace may already hold the answer from its signup research; paying again for it is the waste to avoid.
- **Ask before `--live`, every time.** It spends credits, so it needs the same explicit yes as any paid action: preview, show the estimate and the ceiling, then run. Wanting good context is not a request for it.
- **`--live` requires `--max-credits`.** The server clamps it to the platform cap, and a pass that reaches its ceiling writes a partial result from what it already read.
- **Once per workspace.** The attempt is the lock: completed, partial, skipped and failed all block a second run. `--force` without `--live` previews that re-arm for free and changes nothing; `--force --live` replaces the marker for a second, separately confirmed spend.
- **A real company domain.** The command returns `no_company_domain` without one; for a company known only by its LinkedIn page, use the free flow instead of guessing a domain or substituting a personal profile.
- **What it writes:** the typed profile sections it can support and one cited `[[company-research]]` page whose sources are the URLs it read. Both are revisioned writes a human can revert; it writes nothing to the CRM, outbound tools or public sites, and canonical pins still go through proposals.

MCP: `oxygen_knowledge_bootstrap`, with the same preview-then-authorize rules.
