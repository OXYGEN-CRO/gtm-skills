# Sourcing playbook

Defaults for where leads come from, how sources merge and when to stop. A rule the user states wins; say so when it overrides one here. List size (about 1.4×N for N qualified rows) is in the `oxygen-gtm-consultant` skill's `references/craft.md`.

## Pick the avenue

Take the first row that fits. The free first commands are in SKILL.md's planner table, `warm-leads.md`, the `oxygen-signals` skill and the plays.

| Situation | Avenue |
| --- | --- |
| Customers, deals, a LinkedIn network, followers or post engagers exist | Warm sources, in the order of the `oxygen-onboarding` skill's `references/warm-leads.md` |
| The offer answers an event: hiring for the buyer's role, a new tool, a raise | Signals, ranked below |
| Three or more paying, retained customers, and the buyer is not a local business | Lookalike, then keywords at scale ([play](../plays/lookalike-tam.md)) |
| The buyer is described by what it does, its size and place | Structured TAM |
| The buyer is a business with a physical location or service area | Google Maps ([play](../plays/local-business-maps.md)) |

## Companies, then people

- **Phrases, not pages.** Run each keyword phrase for at most 5 pages (`--max-pages 5`) and add phrases instead: results are ranked by relevance and drift off-topic deeper in.
- **Two contacts per account**: whoever owns the budget and whoever runs the process. Plan once per persona with `--max-per-company 1` and run the second persona into the first run's table (`people search run --table`), so each account gets one of each:
  `oxygen people search plan --from-table <accounts> --linkedin-url-column linkedin_url --titles "<persona titles>" --max-per-company 1 --json`
  Accounts with only a domain: fill the company LinkedIn URL first (`oxygen companies enrich preview <accounts> --missing-fields linkedin_url --all --json`, then `oxygen companies enrich run` with the same flags plus `--approved --max-credits <n>`). Not `--company-domains`: `--max-per-company` caps each account only with `--from-table`.
  Never 5 or more people at one account on a first touch.
- **A second people database only where the first found nobody**: accounts with no person row after the first run (an empty People link column, or no company LinkedIn URL found), one by one, through the specializations in [people](people.md). Never across the whole TAM. Read that column with `oxygen tables query <accounts> --fields <name column>,people --json`; a link column cannot be filtered, because its cells are filled after the query runs.

## Merge and dedupe

- **Keys.** A company is its domain (`--normalize domain` drops scheme, `www.`, path and port), else its company LinkedIn URL; a Maps listing without a website stays keyed on `cid`. A person is their LinkedIn URL (`--normalize linkedin`).
- **The first source sets identity; later sources only fill blanks.** Append each source to one table, warmest first (an upsert overwrites the matched row with the later source's values), then collapse:
  `oxygen tables send <source> <accounts> --automap --dry-run --json`, then without `--dry-run`;
  `oxygen tables dedupe <accounts> --on domain --normalize domain --keep oldest --merge-values fill-empty --json`, then with `--apply --approved`.
- **Placeholder employers are not accounts.** When people rows feed an accounts table, add `--filter '[{"column":"<company name column>","op":"not_in","value":["Stealth Startup","Self-employed","Freelance"]}]'` to the send.

## Signals worth sourcing

Below the warm sources, highest first; capture and arming are the `oxygen-signals` skill.

1. Engagers of a competitor or creator, and a competitor's page followers: far weaker than the user's own audience.
2. Companies hiring for the buyer's role in the last 30 days.
3. Technology adoption.
4. Funding and news, one-shot.

A signal is context, not intent: every signalled row still passes the ICP grade.

## Kill lines

- **After 2 keyword rewrites**, if fewer than half of the 50 preview rows are buyers or `total_results` is under about 300, change instrument once (`--source-intent concept` for what no filter names, `--source-intent technology` for a tool the buyer uses), then switch to the next avenue rather than paging deeper.
- **Grade once, after the merge.** Grading passes, not sourcing, dominate the cost; never re-grade the same rows.
- **Downstream cost against sourcing cost.** Compare the grade's and email finding's dry-run quotes (`oxygen columns run <table> <column> --dry-run --json`, `oxygen enrich-column preview <table> --capability work_email --linkedin-url-column linkedin_url --all --json`) with what sourcing those rows cost. Above 10×, tighten the filters upstream instead of paying to discard rows. The ceiling per qualified lead is the user's to set.
