# CSV → Clean Table → Native CRM Contacts (bind + promote)

Use this when a lead list (CSV export, scraped list, event badge scan) should become **native OXYGEN CRM records** — no external CRM involved. This is the "Records are truth, Tables are work" loop: the table is the disposable working set; the CRM records are the durable truth the team works from. The whole flow is **free** (0 credits): import, dedupe, bind, and promote never call paid providers.

Direction check: to pull records **from** a connected HubSpot or Attio, use [import](import.md). To mirror table rows **out** to a provider, use [sync](sync.md). This page is the native, in-workspace path. Deduplication and auto-dedupe are Table features (the `oxygen-tables` skill, `references/import-and-folders.md`); the loop below uses them before binding.

## The loop

```sh
# 1. Import the CSV into a working table (creates the table + columns from headers)
oxygen tables import --create founder-leads --file leads.csv --json

# 2. Remove duplicates (preview first), then keep future writes deduplicated
oxygen tables dedupe founder-leads --on email --normalize email --json
oxygen tables dedupe founder-leads --on email --normalize email \
  --keep most-complete --merge-values fill-empty --apply --approved --json
oxygen tables auto-dedupe set founder-leads --on email --normalize email --json

# 3. Connect rows to the CRM: a bind column matches each row to a people record
#    by normalized identity (email). --bind-create also creates records for rows
#    that match nothing — that is a truth-write, so live runs need --approved.
oxygen columns add founder-leads --label "CRM Contact" --key crm_contact \
  --kind bind --bind-object people --bind-map email=email --bind-create --json
oxygen columns run founder-leads crm_contact --limit 1 --dry-run --json   # preview first
oxygen columns run founder-leads crm_contact --approved --json            # then live

# 4. Promote chosen table columns onto the bound records (per-field provenance
#    names this table run on every written field). Free but approval-gated.
oxygen tables promote founder-leads --object people --map name=full_name --dry-run --json
oxygen tables promote founder-leads --object people --map name=full_name --approved --json
# promote queues a background run: watch with `oxygen table-runs wait <run_id>`
```

## What each state looks like

- Bind cell payload per row: `{status: matched|created|no_match|ambiguous, record_id, confidence, matched_on}`. `no_match` rows with `--bind-create` become new records on an approved run; rows with a blank identity fail honestly (`bind_create_no_identity`) and stay unbound.
- Promote rejects identity attributes (email is people's identity — it can never be overwritten from a table) and relationship/system attributes (`promote_attribute_invalid` names the offender). Policies: `fill_empty_only` (default), `overwrite`, `skip_conflicts`.
- Verify like the founder would: `oxygen crm search "<name>" --suggest --json`, `oxygen crm get people <record_id> --json`, and the record's `web_url`. Use `--suggest` whenever you have a FRAGMENT — a partial name, a half-remembered email — because it matches prefixes and substrings across the record label plus the email/domain/LinkedIn columns and returns a ranked, compact list. Plain `crm search` is the exact-identity resolve: give it a full email, domain, or LinkedIn URL and it returns the whole record. It is also what the web CRM's own breadcrumb search bar calls, so a founder and an agent get the same ranked answer.

## Gotchas

- A malformed email (inner spaces, no domain) can still bind-create, so scrub the identity column first (`tables tidy-suggest`, formula `normalize_email(email)`) if the source is dirty.
- One bind column per identity mapping; re-running it only fills rows whose bind cell is still empty/no_match (re-runs retry misses, never re-match settled rows).
