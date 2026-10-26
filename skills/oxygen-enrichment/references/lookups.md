# One-shot lookups

For a single contact or company with no table, use the find commands. They resolve the same input-aware waterfall the enrichment columns use, so a one-shot lookup and a column never diverge in routing or billing.

```bash
oxygen find email --linkedin-url https://www.linkedin.com/in/ada --json
oxygen find email --full-name "Ada Lovelace" --company-domain acme.com --json
oxygen find phone --linkedin-url https://www.linkedin.com/in/ada --verify --json
oxygen find linkedin --full-name "Ada Lovelace" --company-domain acme.com --json
oxygen find personal-email --linkedin-url https://www.linkedin.com/in/ada --json
oxygen find person --linkedin-url https://www.linkedin.com/in/ada --json
oxygen find company --domain acme.com --fields headcount,industry,funding_stage --json
```

- **The default mode is a free dry run.** It returns the resolved order (`would_attempt`), the selected profile and an `estimate` block with per-lane prices, `min_credits` and `recommended_max_credits`, the ceiling that funds the whole resolved chain.
- **Live spends and needs a ceiling copied from that estimate**: `--mode live --max-credits <estimate.recommended_max_credits>`, after the user approves. A name-and-domain email find can resolve to a chain with a verified pattern pre-step plus several finder lanes, so a hand-picked ceiling is routinely too low; and a ceiling that is too low does not stop the run, it skips each lane priced above what is left (`spend_cap_too_low`) and still runs the cheaper ones.
- **`--max-credits` caps Oxygen credits, including own-key platform fees.** Each successful own-key provider call incurs the OXYGEN platform fee even on a miss. The provider may separately bill your account under its own rules, outside this ceiling; provider free-on-miss pricing does not waive the OXYGEN fee. A live run that dispatched an own-key lane lists it in `own_key_spend`. Cap own-key calls with an enforced `oxygen limits provider set` (admin).
- **`retry_safe` is true only when a re-run spends nothing**: no lane errored, charged Oxygen credits, ran on the workspace's own key, or reported unknown billing. An own-key miss is not retry-safe: repeating it calls that provider again.
- **The chain depends on the input.** A LinkedIn URL unlocks the full phone chain; an email or a name uses the lanes that accept them. `--verify` (phone only) validates the number and keeps it on any non-verdict; only a genuine "not valid" is discarded.
- **Recently enriched is not charged.** A match reused from OXYGEN's lead cache within the reuse window returns `cache: { reused: true, credits_saved, reused_from }` and bills 0; `enrich-column preview` reports the window under `cache_reuse`.
- **A managed lookup at a ceiling of 0 answers only from that cache.** `oxygen tools run <tool_id> --mode dry-run` on a managed lookup reports `preview.cache.hit` for that exact input; when it is true, `--mode live --approved --max-credits 0` returns the cached result for 0 credits, and a miss at 0 is refused with nothing called or charged. `find company --max-credits 0` can still call providers on zero-credit lanes and reuse priced lanes with a cached answer.
- `find person` takes a LinkedIn URL, a public id, a Sales Navigator link or an email and returns the profile block (name, current company and its LinkedIn URL, job title, start date, education, headline, bio, location, followers) in one managed lookup.
- `find personal-email` resolves a personal address by LinkedIn URL, bills only on a hit and grades the address; it never touches the work email.
- Company fields: [company data](company.md). Checking an address you already have: `oxygen verify email` ([verification](verification.md)).
- Capability names accept natural phrasing too (work email, mobile, linkedin profile, company data).

MCP: `oxygen_find_email`, `oxygen_find_phone`, `oxygen_find_company` and the other find tools take the same inputs and the same `mode` and `max_credits`.

## Provider attribution and settlement

New `person_enrich` presets run `oxygen.person_profile`: Blitz first, then the managed LinkedIn scraper on a Blitz miss. Older presets may still call `scraper.linkedin_profile` directly; inspect the payload column’s `definition.toolId` before attributing its run. Both shapes feed the stored profile extractors; followers fill only when the scraper supplies them.

A provider-native `cost_hint` marked `customer_charge: false` is not an OXYGEN free-call promise. Preview the exact inputs and read the run’s capture, release or pending hold. Confirmed pre-result rejections release; a managed scraper timeout or unreadable response retains an unknown-outcome hold and blocks automatic retry. BetterContact result-priced submissions wait for terminal usage; FullEnrich submit-priced jobs charge on accepted submission even if the eventual result misses. Firecrawl target 404/blocked status and timeout billing remain unknown without an actual settlement receipt; a successful HTTP scrape response is not proof of a free miss. Never generate a paid failure to discover these rules.
