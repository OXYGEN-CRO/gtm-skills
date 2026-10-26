# Work email (and personal email)

Find and verify work emails for an existing contacts table through the native work-email waterfall. To find the companies and their decision makers first, use the `oxygen-sourcing` skill; its free previews feed this table.

## Inputs and profile

Inspect the table first (`oxygen tables describe <contacts_table> --json`, `tables query <contacts_table> --limit 5 --json`). Pick the profile that matches the strongest identity the rows hold:

- `linkedin_url`: rows have a person LinkedIn URL.
- `name_domain`: rows have a full name plus the company domain.
- `first_last_domain`: rows have separate first and last names plus the company domain.

When no company column is mapped, the column infers a `company_domain` or `company_name` column from the table to lift the match rate.

```bash
oxygen enrich-column preview <contacts_table> --capability work_email \
  --email-waterfall-profile linkedin_url --linkedin-url-column linkedin_url \
  --full-name-column full_name --company-domain-column company_domain \
  --target-column work_email_enrichment --only-missing --json
```

`oxygen columns add <table> --capability work_email --json` creates the same column without running it (0 credits); a missing input is named with the `columns update --input-mapping` command that maps it, and `columns run` quotes 0 and refuses until it is mapped.

## Read the preview

Confirm `provider_preflight` has ready lanes for the profile, then read `selected_providers` (the order the lanes run in, which weighs coverage as well as price), `provider_availability` (whether OXYGEN's managed account behind each lane, the verifier and the catch-all escalation included, can take a call right now), `provider_cost_breakdown`, `expected_credits_per_row` (the average, which sizes `recommended_max_credits`), `estimated_credits_per_row` (the worst case, every lane running) and `recommended_max_credits`. Domain-based profiles run a pattern check through the verifier before paid finder steps (`--email-pattern-validation disabled` turns it off), and the winning address is verified afterwards. Lanes run in the listed order, chosen by cost and coverage across the providers the mapped inputs allow, so quote that order rather than sorting by price; a lane that runs only on the workspace's own key is blocked until that key is connected. `--provider-order` replaces the profile's order and is for a deliberate, narrower sequence (for example `--provider-order icypeas,hunter,leadmagic`).

### Managed-only or custom lanes

An email profile follows the current default waterfall, including any own-key lanes. Changing its stored `providers` does not pin a custom order while `emailWaterfallProfile` or `emailWaterfallProfiles` remains present. A definition-level `credentialMode` does not change a lane's credential mode.

For a new or existing column, preview and run with an explicit `--provider-order`, inspecting every preview lane's `credential_mode`. The run pins those source providers for later column runs, replacing the source profile and its pattern pre-step. An automatic column retains its current live verifier and catch-all legs, including when pattern validation was disabled; removed live legs are cleared. Columns without a profile keep their explicit verifier choices. The preview lists and prices retained legs, and explicit verification opt-outs stay disabled.

To edit the definition directly, replace `providers` with the approved managed operations and remove both profile keys in the same update. For example, a single managed Icypeas finder:

```bash
oxygen columns update <table> <column> \
  --definition-unset emailWaterfallProfile,emailWaterfallProfiles \
  --definition-json '{"providers":[{"providerId":"icypeas","operation":"email_discovery","credentialMode":"managed"}]}' --json
oxygen columns run <table> <column> --limit 1 --dry-run --json
```

MCP exposes the same update through `oxygen_columns_update` using `definition_unset` and `definition`. Inspect any separately configured verification, catch-all and pattern-validation lanes too. Run only when the full preview matches the approved scope; a pinned finder order does not automatically add the profile's verifier.

## Run after approval

Approval names the pilot row, the lane order, the estimated credits, the row cap and the fallback behaviour. The run below queues a live background run that spends up to the ceiling once a worker picks it up; without `--approved` the server refuses with `approval_required` (exit 7), and `oxygen table-runs cancel <run_id>` before pickup spends nothing.

```bash
oxygen enrich-column run <contacts_table> --capability work_email \
  --email-waterfall-profile linkedin_url --linkedin-url-column linkedin_url \
  --full-name-column full_name --company-domain-column company_domain \
  --target-column work_email_enrichment --only-missing \
  --approved --max-credits <recommended_max_credits> --json
oxygen table-runs items <run_id> --status failed --json
```

## Personal email

A person's personal address is an option of the same column: `--include-personal-email` (MCP `oxygen_columns_add` with `column: {"capability":"work_email","include_personal_email":true}`; web: the Personal email switch). The personal lane is keyed on the person's LinkedIn URL only; the preview finds that column itself, or name it with `--linkedin-url-column`. It bills only on a hit, has no catch-all escalation and no pattern pre-step, and the verifier grades the winning address. It writes the cell's `personal_email` (`{{work_email_enrichment.personal_email.value}}`) plus the `personal_email`, `personal_email_provider`, `personal_email_status` and `personal_email_enriched_at` columns when the table has them, and never the work `email`. `oxygen enrichment catalog --intent find_personal_email --json` names the lane. One person: `oxygen find personal-email --linkedin-url <url> --json`. A personal address is for a play that asks for one (ad audiences, say), not B2B outreach by default.

## Where values land

A column added with `--capability` fills only its own cell; the flat companion columns (`email`, `email_status`, `personal_email`, ...) are created by `enrich-column run`, and any later run fills them once they exist. `oxygen enrichment catalog --intent <id> --json` lists each output's column `key` and, inside the cell, its `path`.

## QA

- An address on another domain than the row's company is the provider's answer for this person, usually their current employer; the column keeps it and its charge. Check the company before sending.
- Keep provider confidence and verification status, and keep the final outbound-eligible email in its own column, apart from the raw provider output.
- `unknown` is an absent answer, not a bad address; `catch_all` that could not be escalated stays unconfirmed ([verification](verification.md)).
