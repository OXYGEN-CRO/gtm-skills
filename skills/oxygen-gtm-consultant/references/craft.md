# Craft

Operator defaults behind a motion's numbers and words, distilled from real runs. Every ratio here is a starting point, not a law: override it when the user or the data says otherwise, and say so. The feature skills hold the mechanics; spend gates and stop-after-pilot rules are in the `oxygen-gtm` skill (`guides/cost-precheck.md`).

## Sizing a list

- **Size for free first.** Previews, plans and count probes cost nothing; quote a market size only when a provider published the count.
- **Over-provision, then filter.** Provider coverage is a property of the company, not of your query: some rows never resolve. To deliver N qualified rows, source about 1.4×N candidates and keep the best N, then stop.
- **Price the run at the coverage you expect** (about 70% is the usual starting assumption). That number is the pilot's kill line for the stop rule in the `oxygen-gtm` skill's `guides/cost-precheck.md`.
- **Companies first, then people.** Resolve the company set (domain, size, geography, signal) before sourcing people; people-first searches pay for contacts at companies you would have filtered out.
- **Gate paid enrichment on cheap columns.** Add deterministic `icp_fit`, `title_fit`, `geo_fit`, `account_fit`, `dedupe_key` and `enrichment_eligible` columns (formulas or Classify) and enrich only where `enrichment_eligible` is true.
- **Prefer pay-on-match when coverage is uncertain.** Lanes that bill only on a found result beat per-call lanes on an unknown segment; each provider runbook names its billing behaviour.
- **No single source of truth for a field that gates outreach.** Providers disagree, which is why waterfalls exist. A verifier's "invalid" against contradictory evidence (a working MX record) means "not provable": fall back to the next verifier rather than drop the row.

## Voice while operating

The neutral honesty rules are the `oxygen-gtm` skill's (`guides/cost-precheck.md`, Report honestly). On top of them:

- **Narrate.** Say what you are about to do and why, then what happened, naming things the way the user does ("the Accounts table", "the email waterfall"), never by internal id. The user is often not watching the terminal.
- **It is their product to run.** Describe what OXYGEN lets them do ("you can…"), not your own abilities.
- **Lead with a first win, not a catalog.** Answer "what can I do?" with three or four outcomes the user will recognize, then offer to run the smallest real version of one: an ICP account list with a free preview before anything paid; decision makers at those accounts with verified work emails; a scored list with the reason behind every row; a bounded outbound pilot where every message is previewed and approved.

## Copy

- **Evidence before words.** Never write copy from raw names and titles: read which columns hold ICP fit, company and person context, pains, signals and research first, and enrich or research when they are thin.
- **Copy lives in table columns** so every edit, its provenance and the QA stay inspectable; workspace voice, brand and positioning come from the pinned canonical pages, not from each prompt.
- **Structured for decisions, prose for messages.** Scoring and qualification columns return fields later columns can filter and route on; an email body is one answer.

A qualification column's answer, when possible:

```json
{ "fit_label": "high|medium|low|disqualified", "fit_score": 0, "persona_match": "string",
  "relevant_signals": ["string"], "disqualifiers": ["string"], "rationale": "string",
  "next_action": "research_more|contact|nurture|exclude" }
```

An email column's answer:

```json
{ "subject": "string", "body": "string", "personalization_source": "string",
  "evidence_used": ["string"], "risk_notes": ["string"], "requires_human_review": true }
```

A multistep outline has the step count of its play in the `oxygen-sequencer` skill (`plays/`), each step with `step`, `subject`, `core_value_prop`, `body`, `personalization_source` and `evidence_used`. Chain subject-line variants and an automated critique (`email_qa_critique_v1`, verdict `pass`, `tighten` or `block`) off the draft.

**One variable per round.** Two variants differ in one element only, in the order the `oxygen-sequencer` whole-market play sets (`plays/whole-tam-email.md`); a paraphrase spends the send cap and teaches nothing, and spintax already varies wording.

**QA gate before any batch, sync or send:**

- blank or generic personalization, and rows with no source evidence;
- claims the evidence does not support;
- conflicts with a disqualifier;
- fields too long for the destination platform;
- template overlap: inspect rows whose `novelty_score` is under 0.4 (usually the research behind them is too thin);
- rows the critique marked `block`;
- a `lead-sourcing audit` of the table against the ICP spec.

## Journey shapes

Two branch patterns cover most competitor journeys; each arm ends in a `stop` so the arms stay separate. Step syntax and branch mechanics: the `oxygen-sequencer` skill (`references/journeys.md`).

- **Connect or fall back** (the HeyReach default): invite, wait for the connection with `on_timeout: "continue"`, then branch on `already_connected`. Connected people get a warm message thread; the rest get an InMail when their profile is open, else a visit and a follow with no message. Some touch always happens.
- **Matched or fallback sub-sequences** (lemlist style), keyed on what you know: branch on `{ "has_column": "email" }` (`"present": false` for the missing case); people with an email get an email sub-sequence, the rest a LinkedIn sub-sequence. A journey that mixes email and LinkedIn needs a `--max-live-sends` ceiling.

Follow-ups stay linear: reply-stop ends a lead's enrollment on any reply, so never branch on a reply.

## Migration parity

After a migration (Clay or another tool), judge each rebuilt column against its retained original by field type, not one number:

| Field type | Bar | A match is |
| --- | --- | --- |
| Deterministic (formula, direct lookup) | 100% | the same value after trivial whitespace and case normalization |
| Classification or scoring | 90% agreement | the same label, or a score within the stated tolerance |
| Email found-rate | 95% | an email found on the rows the source found one (found against not found; providers legitimately disagree on the address) |
| Open-ended research or generation | 85% | a non-empty, non-error result where the source had one; wording is expected to differ |

A column under its bar is not automatically wrong: inspect a handful of mismatches (a stale source value, a provider OXYGEN does not carry, or a rebuild bug) and report the rate with your read before calling it done.
