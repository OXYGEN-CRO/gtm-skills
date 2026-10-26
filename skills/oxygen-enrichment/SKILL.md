---
name: oxygen-enrichment
description: "Enrich OXYGEN Table rows and single records: person and company profiles, funding, revenue, hiring and tech stack, work and personal email, mobile phone, LinkedIn URL and email or phone verification, through native waterfalls with free previews, one-row pilots and approved ceilings."
allowed-tools: Bash(oxygen *)
---

# OXYGEN Enrichment

Start with the data. Use native waterfalls by default when the user has not named or restricted suppliers. Honor explicit supplier and verification constraints; discover the current native operations and their inputs before proposing an approved run. `oxygen enrichment catalog --json` lists every data type a table can fill (person profile, work email, phone, headcount, funding, tech stack, hiring, decision makers, news, signals) with its status, the inputs it needs, the fields it fills, region coverage, the expected and up-to credits per row and the exact add command. Filter with `--intent <id>`, `--group company`, `--region DACH` or `--status default`. A `no_default` or `coming_soon` row is an honest refusal: report it, and leave its provider column unbuilt. The column you add is named after the data; provider ids appear in `--json` and previews so you can debug a miss or pick your own key.

## Pick the path

| Data | Start with | Read |
| --- | --- | --- |
| Person profile from a LinkedIn URL | `columns add <table> --preset person_enrich --input url=<column>` | — |
| Company profile, funding, revenue, open roles, tech stack | `--preset company_enrich`, `company_funding`, `company_revenue`, `company_hiring`, `company_tech_stack` | [company](references/company.md) |
| Any other company field on existing rows | `companies enrich preview <table> --missing-fields <keys>` | [company](references/company.md) |
| Work email, with personal email as an option | `columns add <table> --capability work_email` | [email](references/email.md) |
| Mobile phone | `enrich-column preview <table> --capability mobile_phone` | [phone](references/phone.md) |
| LinkedIn URL from a name and company, or an email | `columns add <table> --capability linkedin_url` | [LinkedIn URL](references/linkedin-url.md) |
| Grade emails you already have | `columns add <table> --capability verify_email` | [verification](references/verification.md) |
| One person or company, no table | `find email`, `find phone`, `find linkedin`, `find person`, `find company`, `verify email` | [one-shot lookups](references/lookups.md) |

`oxygen tools search --for-table <table> --json` reads the table's identity columns and suggests what is worth adding next, each with a price label and its add command, free. Presets fill their companion columns in the same write and spend nothing until run. Questions over a person's profile and web research questions are Table columns: the `oxygen-tables` skill.

## Run loop

1. Preview, free: `oxygen enrich-column preview <table> --capability <capability> --json` or `oxygen columns run <table> <column> --limit 1 --dry-run --json`. Read `provider_preflight` (a `blocked` lane cannot run: fix its inputs or access, or order only `ready` lanes), `provider_availability.lanes[]` (`ok`, `degraded`, `unknown`; `will_produce_results: false` means a live run returns nothing), `credits_quote_basis`, the expected cost, the worst case and `recommended_max_credits`.
2. Pilot one row after approval and read the value and its receipt.
3. Run the approved scope with `--only-missing` or `--limit`, `--approved` and `--max-credits <recommended_max_credits>`, then `oxygen table-runs wait <run_id> --json` and `table-runs provider-summary <run_id>` for which lanes paid.

## Gates

- **Approval and a ceiling from the preview.** A live run needs the user's approval of the rows, the lanes and the cost, and `--max-credits` copied from `recommended_max_credits`; never a hand-picked number. A ceiling that is too low does not stop a waterfall: it skips the pricier lanes and still bills the cheaper ones.
- **Phone, personal email and reveal options need their own explicit yes.** They cost several times a work email.
- **Own-key lanes are real spend.** A lane on the customer's own provider key bills their account plus OXYGEN's per-call BYOK platform fee when one applies (`oxygen billing usage --meter byok_calls`), and still needs approval.
- **Enrich only what survives.** Dedupe and qualify first; never pay twice for a duplicate or a row you will discard. Never re-run a miss on the same provider: a miss is an answer.
- **Keep the default waterfall native.** With unrestricted suppliers, use the native waterfall and its available verification and catch-all escalation (`provider_availability`). With an explicit supplier restriction, use only those approved native lanes; do not silently add a verifier or another provider. If the requested verification is unavailable within that scope, report the limitation. A returned address alone is not verified: an unconfirmed `catch_all` stays unconfirmed.
- **Queued is not spent.** A queued run captures nothing until a worker starts it; `oxygen table-runs cancel <run_id>` before pickup spends 0.
- **A found value is not permission to use it.** Emailing or calling a found contact, or writing it to a CRM or a campaign, is its own approval.

## Provider runbooks

Load only the selected provider's file, after `oxygen tools get <tool_id> --json` (current inputs, price, availability). Each runbook says whether OXYGEN funds the provider or it runs only on the workspace's own key, and its generated price table quotes example payloads.

- Contact and profile data: [AI Ark](provider-runbooks/ai_ark.md), [Apollo](provider-runbooks/apollo.md), [BetterContact](provider-runbooks/bettercontact.md), [ContactOut](provider-runbooks/contactout.md), [Crustdata](provider-runbooks/crustdata.md), [Findymail](provider-runbooks/findymail.md), [Forager](provider-runbooks/forager.md), [FullEnrich](provider-runbooks/fullenrich.md), [Hunter](provider-runbooks/hunter.md), [Icypeas](provider-runbooks/icypeas.md), [LeadMagic](provider-runbooks/leadmagic.md), [Lusha](provider-runbooks/lusha.md), [People Data Labs](provider-runbooks/peopledatalabs.md), [Prospeo](provider-runbooks/prospeo.md), [RocketReach](provider-runbooks/rocketreach.md), [Scalelist](provider-runbooks/scalelist.md), [Wiza](provider-runbooks/wiza.md).
- Verification: [MillionVerifier](provider-runbooks/millionverifier.md), [BounceBan](provider-runbooks/bounceban.md), [ClearoutPhone](provider-runbooks/clearoutphone.md).
- Public LinkedIn profiles and companies, managed with no account or on the workspace's own HarvestAPI key: [Professional Network Data](provider-runbooks/scraper.md).
- Search and sourcing providers (Blitz, Dropleads, Exa, Serper, Firecrawl): the `oxygen-sourcing` skill.
