# Day 1: from your offer to your warmest leads

## The Play

In one free session the founder gets three things: a short answer to "what do we sell, and who buys it" saved in the workspace, a table of about ten people to contact first with the reason for each, and first messages drafted for the top three to five. Warm contacts (customers, open deals, unanswered replies, the founder's LinkedIn network) come first when the workspace has them; otherwise a free search finds real people who match the buyers. Nothing is sent and no credits are spent.

## Before You Start

- **Signed in:** `oxygen whoami --json`, free. If it asks for a login, run `oxygen login`. Tell the founder: "Approve this terminal once in your browser."
- **What you sell and who buys it:** `oxygen context profile get --json`, free. Empty `offering` and `icp` are fine: step 2 drafts them from the website, so ask the founder nothing yet.
- **Optional, where the founder's contacts live:** CRM records, a connected mailbox or LinkedIn account, or a customer list or LinkedIn `Connections.csv` in your working folder; step 1 shows which exist, free. Connecting LinkedIn or a mailbox needs a paid plan and then reserves 3,400 credits a month (an own mailbox: 100 a month) from the balance; the connect step previews the price. Day 1 works without either. If none exist, tell the founder: "You have no contacts in OXYGEN yet, so I'll start from people who match your buyers. LinkedIn's free Connections export would add warmer names."

## Steps

1. Read what the workspace already holds — free.
   `oxygen knowledge resolve --purpose onboarding --json`
   Note `profile.data.offering` and `profile.data.icp` (empty means not saved, even when `status` says `ready`), `onboarding.researchState` (`completed` means OXYGEN researched the company), `workspace.data.records.objects` (0 means no CRM yet), `workspace.access.linkedin_accounts`, `workspace.access.mailboxes` and `workspace.campaigns.signal_sources`. Also look in your working folder for a customer list, a CRM export or `Connections.csv`; reading a file uploads nothing.
   Tell the founder: "I checked what OXYGEN knows about you and where your contacts are. Nothing was spent."
2. Write down the offer and the ideal customer, labelled as drafts — free.
   If both are saved, use them and go to step 3. Otherwise read `oxygen knowledge page get company-research --json` when `researchState` is `completed`, else the company website. Draft the offer (what it is, the buyer's problem, proof or "unproven", price, why it beats what buyers do today) and the ideal customer (buyer titles, company size, industry, countries, who is out), then save it without waiting:
   ```bash
   oxygen context profile update --data-json '{"offering":{"product":"<what it is>","value_prop":"<the problem it solves, for whom>","proof_points":["<a number or a named customer, or unproven>"],"pricing":"<entry price, who buys>","status":"hypothesis"},"icp":{"target_accounts":"<industry, size, countries>","buyer_personas":["<titles>"],"disqualifiers":["<who is out>"],"status":"hypothesis"},"market":{"alternatives":["<what buyers use today>"]}}' --json
   ```
   Tell the founder: "Here is what I think you sell and who buys it. I saved it as a draft; correct anything that's off."
3. Read only the warm sources that exist — free.
   - CRM objects above 0: `oxygen crm pipeline --json` (open and stalled deals).
   - A mailbox or LinkedIn account: `oxygen inbox list --status interested --unanswered --json` (interested replies waiting on the founder).
   - A LinkedIn account: `oxygen linkedin network status --json` (captured connections and the table that holds them).
   - Signal sources and CRM objects above 0: `oxygen signals leads-today --within-days 30 --json` (people who visited, viewed or engaged).
   - A customer list or `Connections.csv` in the folder: read it.

   Give every missing source one line on what would fill it, then move on.
   Tell the founder: "These are the contacts you already have: …", or "You have no contacts in OXYGEN yet, so I'll start from people who match your buyers. LinkedIn's free Connections export, saved into this folder, would add warmer names at no cost."
4. Fewer than ten names so far? Fill up with the free people search — free, up to 50 people per preview.
   ```bash
   oxygen people search preview --filters-json '{"people":{"job_title":{"include":["Founder","Co-Founder","CEO"]},"location":{"country_code":["US","GB"]}},"company":{"industry":{"include":["Software Development"]},"employee_range":["11-50"],"hq":{"country_code":["US","GB"]}}}' --json
   ```
   Swap in the titles, size, industry and countries from step 2. The answer leads with `total_results` (how many people match), `company_fit` (what a person row cannot show, and the filters every person matched) and `next_step` (what saving them and finding their emails costs); the rows come last, up to 50 compact entries (about 20 KB in all). Save it (`… --json > people-preview.json`) and read every row's `full_name`, `title`, `company_name`, `company_domain`, `location` and `linkedin_url` before you judge the fit. The rows do not say what each company does, so say which fits you could not check. If fewer than half of the first rows look like buyers, tighten once (narrower titles, or `company.keywords.include` for the niche) and preview again.
   Tell the founder: "About N people match your ideal customer; here are the ten that fit best."
5. Rank about ten people and save them with first messages in one table — free.
   In admitted guided onboarding, reuse the activation's First leads Table and stable person keys. Resume from its native resource links; do not create another shortlist on refresh. The standalone create below is for a workspace without that bound Table.
   Keep one row per person. Drop do-not-contact entries, anyone already enrolled in a campaign, sample records (marked `_sample: true`), investors, and companies that sell what the founder sells. Keep unanswered replies: the founder owes them an answer, so their draft replies to their last message rather than opening cold. Rank customers first, then open deals, unanswered replies, engaged contacts and new matches; within each group, the strongest fit first.
   ```bash
   oxygen tables create "Day 1 leads" --columns-json '[{"key":"rank","label":"Rank","dataType":"numeric"},{"key":"name","label":"Name","dataType":"text"},{"key":"title","label":"Title","dataType":"text"},{"key":"company","label":"Company","dataType":"text"},{"key":"linkedin_url","label":"LinkedIn","dataType":"text"},{"key":"why","label":"Why this person","dataType":"text"},{"key":"first_message","label":"First message (draft)","dataType":"text"}]' --json
   oxygen tables insert <table> --rows-json '[{"rank":1,"name":"<full name>","title":"<title>","company":"<company>","linkedin_url":"<url>","why":"<warm source or fit, in one line>","first_message":"<draft>"}]' --json
   ```
   `<table>` is the id that `tables create` returned. Write `first_message` for the top three to five only: a short note to the person by name, built on `why`, in the founder's voice. Nothing is sent.
   Tell the founder: "Your ten people and first drafts are here: <web_url>. Send the top three yourself today."
6. Log the day so the next session starts from it — free.
   `oxygen knowledge log append --event decision --summary "Day 1: offer and ideal customer saved as drafts; top people in Day 1 leads; next: <step>" --json`
   Tell the founder the one next step: send the drafts, then the `daily-warm-lead-queue` play once LinkedIn or a mailbox is connected, or `outbound-pilot-50` for a small capped first campaign (`oxygen recipes show <slug> --json`).

## If It Goes Wrong

- `crm_object_not_found` from `oxygen crm pipeline` or `oxygen signals leads-today` → the workspace has no CRM yet, so there is nothing to read; skip that source. When the founder wants the lists, `oxygen crm setup --live --without-enrichment --json` creates them for free without switching on paid enrichment.
- `unknown command 'crm pipeline'` → the command words reached the CLI as one quoted argument (a loop variable); run each command on its own line.
- `rate_limit_exceeded` from the people preview → wait until `details.reset_at`, then run it once more.
- `invalid_filters` or `invalid_provider_enum_value` → a filter key or value is not in the list. Keys are in the `fields` array at the top of `oxygen people search filters --json`; use its exact values (country codes are two letters: GB, not UK).
- `live_route_not_ready` from `oxygen people search run` → saving a whole search as a table is not available yet; keep to the free preview and add the people you picked with `oxygen tables insert`.
- No company research and no website access → ask the founder for two sentences (what you sell, who buys it), or preview OXYGEN's research for free with `oxygen knowledge bootstrap --domain <domain> --json` (the hint's `domain=` is spelled `--domain` here). Running it costs up to 30 credits and needs the founder's OK.
- `cli_update_required` → run `oxygen update`, then rerun the command.
