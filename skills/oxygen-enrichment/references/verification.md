# Email and phone verification

Checking addresses you already have is a different job from finding one. MillionVerifier is the only default verifier. An error or `unknown` leaves the address unverified. Only a `catch_all` verdict escalates to BounceBan, which can resolve many accept-all domains. Icypeas, Dropleads, Hunter and ZeroBounce remain selectable by name. An existing verification column keeps its configured verifier and escalation. Its preview lists and prices those actual lanes, including disabled escalation and own-key choices.

## A column over a table

```bash
oxygen columns add <table> --capability verify_email --json
oxygen columns run <table> <column> --limit 1 --dry-run --json
```

The column auto-detects an `email` or `work_email` column, creates the exact column and runs nothing (0 credits); web: Add column, Email verification. It writes `valid`, `invalid` or `catch_all` into the cell and writes nothing for `unknown`, so an absent answer never looks graded.

For an explicit single verifier, preview `oxygen enrich-column preview <table> --capability verify_email --provider-order dropleads --limit 1 --json`. The same provider order on `enrich-column run` saves that verifier on the column. A named single verifier disables the default catch-all escalation: `catch_all` remains unconfirmed, and no unnamed supplier runs. Preview the price, then pass the approved row scope and credit ceiling for a live run.

## One or a few addresses

```bash
oxygen verify email a@acme.com b@acme.com --json
oxygen verify email a@acme.com b@acme.com --mode live --approved --max-credits <estimate.recommended_max_credits> --json
```

The free dry run returns `estimate.recommended_max_credits`, the worst case including catch-all escalation. Pass that number: only catch-all addresses pay the escalation, which costs several times more than the first pass, so a ceiling sized as "addresses x first pass" runs out as soon as a few are catch-all. A ceiling is not a charge; you pay for what runs. MCP: `oxygen_verify_email`.

## The verdicts

- `valid`: the mailbox is confirmed.
- `invalid` (also disposable, spam trap, do not mail): not sendable.
- `catch_all`: the domain accepts everything, so the mailbox itself cannot be confirmed. Usable but riskier.
- `unknown`: no verifier could answer. **An absent answer, not a bad address**: never filter these out as invalid; re-run later or treat them as unverified.

## When the escalation could not run

Read the preview first: `catch_all_escalation_available: false` reports a known blocker and its `next_action`; `null` with `catch_all_escalation_availability: "unknown"` means the check itself failed, so retry the preview. Availability is a snapshot, re-checked at run time.

**A catch-all whose escalation could not run stays unconfirmed: record it as unconfirmed, never as verified or invalid.** The result's `escalation_skipped` and `next_action` say why and what to do; read them before any retry. `budget_exhausted` is your own ceiling (re-run those addresses with the recommended one), while a dry or held managed account is OXYGEN's side, so topping up workspace credits does not fix it. Every reason and its fix: [BounceBan](../provider-runbooks/bounceban.md); the first pass: [MillionVerifier](../provider-runbooks/millionverifier.md).

## Phones

The first-class phone verification column remains `coming_soon`. The default managed phone waterfall finds numbers without verification. To validate an existing number directly, use `oxygen tools run clearoutphone.validate_phone`; see [ClearoutPhone](../provider-runbooks/clearoutphone.md) for approval, pricing and verdict handling. A configured optional waterfall verifier keeps unknown or incomplete results as unverified and rejects only explicit invalid verdicts. See [phone enrichment](phone.md) for source-only runs.

## Resetting a column

To put an existing enrichment column back on OXYGEN's default waterfall, preview `oxygen enrichment apply-default-cascade <table> <column> --dry-run --json`, then run it without `--dry-run`.
