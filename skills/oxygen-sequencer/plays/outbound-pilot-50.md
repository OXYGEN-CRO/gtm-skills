# Launch a 50-lead outbound pilot

## The Play

You get 25 decision makers who fit who you sell to, each with a checked work email and a drafted first line, in one table you review before anything is sent; then you email those 25 from a connected inbox and see within two weeks whether the list and the message earn replies. Only after replies come in do you add the next 25 (that makes the 50) and raise the daily volume. Finding and drafting the first 25 costs about 125 credits; sending costs no credits but needs warmed inboxes on a separate domain.

## Before You Start

- **What you sell and who buys it.** `oxygen context profile get --json` (free): `is_empty` is false and `offering` and `icp` are filled. If not, ask the founder: "What do you sell, in one sentence, and which people at which kinds of companies buy it?" Save the answer (free): `oxygen context profile update --data-json '{"offering":{"summary":"<what you sell>"},"icp":{"summary":"<who buys>"}}' --json`.
- **About 150 credits.** `oxygen billing balance --json` (free): read `spendable_credits`, which comes after the `available_plans` list. `available_credits` still includes credits already committed to inboxes and other monthly charges. The pilot costs about 125 and its caps add up to 142; nothing here adds a monthly charge. If short, tell the founder: "This needs about 150 credits and you have N; add credits at https://oxygen-agent.com/billing."
- **Inboxes, only for step 6.** `oxygen mailboxes list` (free; without `--json` it prints the inbox count and every inbox that needs action first; with `--json`, `count` and `summary` come after the full list); inboxes need a paid plan ($49 a month and up) whatever the credits, and a step that answers `upgrade_required` means this workspace needs one: tell the founder to subscribe and link its `upgrade_url`. Without inboxes, steps 1-5 still give reviewed drafts and a ready sequence. Tell the founder: "To send, you need two inboxes on a separate domain, never your own work inbox: about 1,700-2,250 credits the first month, then 1,000 a month, plus 14 days of warm-up; the email-infra-setup play sets them up."

## Steps

1. Describe the people and preview them (free). Default: founders, CEOs and heads of sales at 5-50-person companies in the founder's country (its two-letter code in place of `US`, in both places); `company.keywords` holds the words buyers use for their own business. Set `company.industry.include` to the buyers' industry, spelled as `oxygen people search filters --json` lists it (software buyers: `Software Development`), or drop it when they span industries: keywords alone also match investors, recruiters and agencies that describe their clients' business. Already graded accounts with icp-to-account-map? Read them with `oxygen tables query <accounts> --fields company_name,linkedin_url,icp_fit --json` and replace the `company` block with `{"linkedin_url":["<up to 50 high or medium fits>"]}`.
   ```bash
   echo '{"people":{"job_title":{"include":["Founder","CEO","Head of Sales"],"exclude":["Assistant","Intern","Investor","Advisor","Managing Partner","Consultant","Recruiter"]},"location":{"country_code":["US"]}},"company":{"industry":{"include":["<buyers industry>"]},"keywords":{"include":["<what buyers do>"]},"employee_count":{"min":5,"max":50},"hq":{"country_code":["US"]}}}' > filters.json
   oxygen people search preview --filters-json ./filters.json --json
   ```
   The reply is long (about 20 KB for 50 people) and `total_results` comes after the rows: save it to a file and read all 50 rows, not the first screen. Read `full_name`, `title` and `company_name` per row and `total_results` at the end. Investors, advisors and consultants often match the same words as buyers: if any appear, add their title words to `job_title.exclude` and preview once more. Never ask for the pilot-spend approval on a list that still contains them.
   Tell the founder: "Here are 10 of the 25 people I'd contact; nothing is spent yet."
> APPROVAL GATE — pilot-spend: show who they are (about 10 names, titles and companies from the preview) and each paid step with its cap: save them 2 credits (expect 1), work emails 100 (expect ~85, about 3.3 a person), first lines 40 (expect ~38, 1.5 each); at most 142, about 125 expected. One approval covers steps 2-3; stop and ask again if a quote is above its cap.
2. Save them and find their work emails (1 credit, then ~85 capped at 100). The email run writes `email` and `email_status`: `verified`, `catch_all` (the company accepts any address, so it may bounce), `unknown` or `invalid`; people without an email are skipped when sending.
   ```bash
   oxygen people search run --source people_search --source-filters-json ./filters.json --target-count 25 --table-name "Outbound pilot" --mode live --max-credits 2 --approved --json
   oxygen table-ingestions wait <ingestion run id> --timeout-seconds 100 --json
   oxygen enrich-column run <table> --capability work_email --email-waterfall-profile linkedin_url --linkedin-url-column linkedin_url --only-missing --limit 25 --approved --max-credits 100 --json
   oxygen table-runs wait <run_id> --timeout-seconds 100 --json
   ```
   Tell the founder: "Your 25 people are in a table (<web_url>); emails found for N: X verified, Y catch-all."
3. Draft a first line for each (~38 credits, capped at 40). Put the founder's problem in the prompt; the column sees only the table's facts. The dry run is free and shows one rendered prompt and the price; wait on the run as in step 2.
   ```bash
   oxygen columns add <table> --label "First line" --key first_line --reasoning-level low --prompt 'Write the first two lines of a cold email to {{full_name}}, {{title}} at {{company_name}}. Line 1: Hi, their first name and a comma. Line 2: one sentence of at most 25 words linking their role to this problem we solve: <the problem, in the founder words>. Use only these facts. No flattery, no exclamation marks.' --json
   oxygen columns run <table> first_line --limit 25 --dry-run --json
   oxygen columns run <table> first_line --limit 25 --approved --max-credits 40 --json
   ```
   Tell the founder: "First lines are written; about 125 credits spent in total."
4. Review with the founder (free). Show 5 first lines and the table link. Delete the row of anyone whose email domain differs from `company_domain` (the audit found "verified" emails at the wrong company) and every row the founder rejects (customers, investors, friends, competitors); to block a person or company for good, also `oxygen suppressions import --file ./never.txt --reason manual --json` (one email or domain per line). New wording: `oxygen columns update <table> first_line --prompt '<new prompt>' --json`, then step 3's run with `--force` (~38 credits).
   ```bash
   oxygen tables query <table> --fields full_name,title,company_name,company_domain,email,email_status,first_line --limit 50 --json
   oxygen tables delete-rows <table> --row-ids-json '["<_row_id>"]' --json
   ```
   Tell the founder: "Would you put your name on these? Tell me who to drop and what to change."
5. Prepare the emails (free; nothing sends). Fill each `<...>` with the founder and use the buyers' time zone. The last command is the free launch preview, a read-only command: nothing changes; it renders real emails, names the sending inbox and lists blockers such as no inbox.
   ```bash
   cat > steps.json <<'EOF'
   {"steps":[{"id":"s1","channel":"email","kind":"email_send","subject_template":"Question about {{company_name|your team}}","variants":[{"subject_template":"{{company_name|Your team}} and <your company>"}],"auto_optimize":{"metric":"reply"},"body_template":"{{first_line|Hi there,}}\n\n<What you do in one sentence, with one proof point.>\n\nWorth a 15-minute call next week? If not, just say so and I will not write again.\n\n{{sender_first_name}}"},
    {"id":"w1","kind":"wait","days":3},{"id":"s2","channel":"email","kind":"email_send","body_template":"Following up once: is <the problem> on your list this quarter?\n\n{{sender_first_name}}"}]}
   EOF
   oxygen sequences create --name "Outbound pilot" --slug outbound-pilot --steps-file ./steps.json --channels email --table <table> --enroll --max-live-sends 50 --max-emails-per-mailbox-per-day 20 --company-reply-pause default --schedule-timezone America/New_York --schedule-days mon-fri --schedule-hours-start 09:00 --schedule-hours-end 17:00 --json
   oxygen sequences preview outbound-pilot --json
   ```
   Tell the founder: "Here is the exact first email for <name>; nothing has been sent."
> APPROVAL GATE — first-send: show who (the count after drops and do-not-contact), from which inbox (name and address, on the separate sending domain, never the founder's own), two rendered emails from the preview, when (weekdays 09:00-17:00 in the chosen time zone, up to 20 a day per inbox, one follow-up 3 days later) and the cap of 50 emails, 0 credits. Say that the first live start also switches on the workspace's standing rule that files replies into the CRM.
6. Send (0 credits; needs the warmed inboxes, and a paid plan only if a step answers `upgrade_required`), then read `oxygen sequences stats outbound-pilot --json` after 3, 7 and 14 days: sent, replies, bounces.
   ```bash
   oxygen sequences start outbound-pilot --approved --max-live-sends 50 --json
   ```
   Tell the founder: "Sending to 25 people, up to 20 a day; I'll check replies in 3 days."
7. Decide whether to scale (free), only after the pilot ran. Go on when `sequences stats` shows every lead contacted, at least one positive reply and hard bounces under 2%, and `oxygen mailboxes list --json` shows at least two inboxes on a separate domain warmed 14+ days (email-infra-setup). Otherwise change the list or the message and run steps 1-6 again. Next 25: steps 2-4 again, with `--table <table> --target-count 50` in place of `--table-name` (still 1 credit; people already in the table are not added twice), under the pilot-spend gate (~125 per 25). Past 50 people, run the whole-tam-email play instead.
   Tell the founder: "N replies and B% bounces from 25: worth sending more" (or "not yet, and here is what I would change").
> APPROVAL GATE — volume-increase: show the pilot's reply and bounce rates, how many new people get enrolled (they are emailed from the next send window) and the one limit being raised; raise one limit at a time and re-read stats after 2-3 sending days.
8. Send more (0 credits).
   ```bash
   oxygen sequences enroll outbound-pilot --from-table --json
   oxygen sequences update outbound-pilot --max-new-enrollments-per-day 20 --sequence-prioritization followups --json
   oxygen sequences start outbound-pilot --approved --max-live-sends 150 --json
   ```
   The two subject lines are the A/B test: once both have enough sends the auto-winner pauses the weaker one (reversible), and `oxygen sequences variants outbound-pilot --json` shows the scores. More volume means more warmed inboxes, never a higher cap per inbox.
   Tell the founder: "Sending to N more people, at most 150 emails in total; nothing else changes."

## If It Goes Wrong

- `workflow_disabled` or `workflow_live_preview_not_graph` → that is the old template route (`blueprints apply dm-outbound-pilot`): it must be switched on as a standing automation and never shows a price. Leave it and use steps 1-6.
- `invalid_filters` → a key or shape is wrong: `oxygen people search filters --json` lists the keys; only keys ending in `.include` or `.exclude` take `{"include":[...]}`, and countries are two letters (the UK is `GB`). `rate_limit_exceeded` → wait a minute and retry once.
- `approval_required`, `spend_cap_required`, `send_cap_required` or `people_search_quote_changed` → a flag is missing (`--approved`, `--max-credits`, `--max-live-sends`) or the cap is below the quote; run the same people search with `--mode dry_run` in place of `--mode live --approved` (free; it creates no table), or the column with `--dry-run`, to read the quote. If your agent's safety layer refuses it, show the founder the command and the caps from the pilot-spend gate: it spends and writes nothing.
- The email preview estimates hundreds of credits → it overestimates (the audit's 25 emails were quoted 1,579 and cost 84); keep `--max-credits 100`. If the cap stops the run, found emails stay and the same command fills the rest.
- `insufficient_credits` or `committed_credits_blocked` → top up at https://oxygen-agent.com/billing; `upgrade_required` → a paid plan, and the drafts and sequence stay ready.
- A `wait` stops at its timeout (exit 8) while the run is still going → run the same wait again.
- `invalid_sequence` → in steps.json every step needs an `id`, every email a `body_template`, the first email a `subject_template`.
- `sequence_no_sendable_mailboxes` or `sequence_no_senders` → no connected inbox: email-infra-setup.
- Your agent refuses `sequences start` without `--approved` → run `oxygen sequences preview outbound-pilot --json` instead: the same free preview as a read-only command; `oxygen sequences get outbound-pilot --readiness --json` gives the launch check without the copy scan.
- The sequence paused itself → hard bounces passed 3% of sends; delete the bad rows, then `oxygen sequences resume outbound-pilot --json`.
