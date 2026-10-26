# Answer inbound leads in minutes

## The Play
Every new signup or demo request lands in one table the moment your form sends it; OXYGEN looks up their company, scores how well they fit the customers you want (your ICP) and adds them to your contact list (CRM), so you can answer the best ones the same day. It is the right play when signups already arrive and nobody replies within hours. Replies stay personal until you choose to switch on a follow-up email.

## Before You Start
- Company, offer and ICP are saved: `oxygen context profile get --json` (free). Missing → fit scores are guesses; tell the founder "I need one line on what you sell and to whom" and run day-1-first-win first.
- Contact lists (CRM) exist: `oxygen crm objects --json` (free). `objects: []` → Step 1 creates them for free.
- A signup table or address from an earlier session: `oxygen tables webhook list --json` (free). If one exists, reuse it instead of Step 2's create: check its `authMode` (switch a header-free address that has had no deliveries to `--auth-mode secret` with `oxygen tables webhook update <endpoint_id> --auth-mode secret --json`, free) and its `upsertKey`, and hand the founder an example body that matches that key.
- Something can send each signup as JSON to a web address: the founder's app backend, or their form tool through Zapier or Make (no check command; a one-off setup, free on OXYGEN's side). Missing → tell the founder "I'll give you an address and an example; your developer or a Zapier step connects the form in minutes."
- Only for the automatic follow-up email: a connected mailbox, `oxygen mailboxes list --json` (free). An own mailbox costs 100 credits a month (connect it as the reply-to-meeting play does). Missing → the founder replies by hand from their inbox, which is free and fastest.
- Credits: `oxygen billing balance --json` (free; read `spendable_credits`, which comes after the six-plan price list, and quote that number: a dry run's `available_credits` also counts credits held for monthly account charges). The test costs 1–3 credits; each later work-email signup costs about 1.1 (at most 2.1), a personal-email signup 0.075. Short → tell the founder "The test needs about 3 credits; everything before it is free."

## Steps
1. Create the contact lists without the automatic paid lookups a plain setup would switch on (free, nothing recurring; skip when they exist): `oxygen crm setup --live --without-enrichment --json`.
   Tell the founder: "Your contact lists are ready, and nothing in them spends credits on its own."
2. Make the signup address (free):
   ```bash
   oxygen tables create "Signups" --columns-json '[{"key":"email","label":"Email","dataType":"text"},{"key":"first_name","label":"First name","dataType":"text"},{"key":"last_name","label":"Last name","dataType":"text"},{"key":"payload","label":"Raw signup","dataType":"jsonb","kind":"source","definition":{"webhook_payload":true}}]' --json
   oxygen tables webhook create signups --name "Signups" --mode upsert --upsert-key email --auth-mode secret --json
   ```
   Hand the founder `webhookUrl`, the one-time `secret` (sent as the header `x-oxygen-table-webhook-secret`) and an example body: `{"email":"jane@acme.com","first_name":"Jane","last_name":"Doe"}`. Do this for a reused address too; its body must carry the address's `upsertKey`. Keep `endpointId` (`tw_…`) for later steps. If their form tool cannot add a header, switch to a header-free address and keep it private: `oxygen tables webhook update <endpoint_id> --auth-mode none --json`.
   Tell the founder: "Send each signup to this address; your developer or a Zapier step can do it."
3. Add the company lookup, the fit score, the CRM link and one made-up signup (free; nothing runs yet):
   ```bash
   oxygen columns add signups --kind formula --key work_domain --label "Work domain" --data-type text --definition-json '{"expression":"if(email_type(email) = \"work\", email_domain(email))"}' --json
   oxygen columns add signups --preset company_enrich --input domain=work_domain --json
   oxygen columns add signups --key icp_fit --label "ICP fit" --score "low,medium,high" --prompt "How well does {{company_name}} fit our ideal customer? {{company_industry}}, {{company_headcount}} employees. {{company_description}}" --grounding workspace --json
   oxygen columns add signups --bind-object people --bind-map email=email --bind-create --key crm_person --label "CRM person" --json
   oxygen tables upsert signups --key email --rows-json '[{"email":"test@<founder company domain>","first_name":"Test","last_name":"Signup"}]' --json
   oxygen columns run signups company_enrich --limit 1 --dry-run --json
   ```
   Personal addresses (gmail and the like) get no work domain, so their company lookup is skipped (only the 0.075 fit score runs). Test with the founder's own domain so you know which company should come back.
   Tell the founder: "Every signup will get its company looked up and a fit score."
> APPROVAL GATE — enrich-pilot: one test row: the company lookup costs about 1 credit (the dry run may say 2, the worst case) and the fit score 0.075; caps 3 and 1.
4. Run the test (about 1.1 credits; the CRM link is free). Wait for the lookup before scoring, because the score reads its fields:
   ```bash
   oxygen columns run signups company_enrich --limit 1 --approved --max-credits 3 --json
   oxygen table-runs wait <runId> --json
   oxygen columns run signups icp_fit --limit 1 --approved --max-credits 1 --json
   oxygen columns run signups crm_person --limit 1 --approved --json
   oxygen crm search <test email> --object people --json
   ```
   Check that `company_domain` matches the email's domain: a different one means the lookup matched another company (the audit saw oxygen-agent.com come back as copia-ai.com), so do not trust those fields. A reused test row whose company lookup already has a value is skipped by `--limit 1` (it runs only rows whose cell is empty): add a fresh test row with Step 3's upsert, or run the lookup and the score with `--row-id <_row_id> --force`, and quote the dry run of that exact command.
   Tell the founder: "The test signup is in your CRM with its company and fit score; it cost about 1 credit."
> APPROVAL GATE — auto-run-arm: from now on every signup the address receives is looked up and scored without asking, about 1.1 credits per work-email signup and at most 5 per delivery (rows beyond it are skipped with `credit_limit_reached`); 100 signups a month ≈ 110 credits, at most about 210. It runs until `oxygen tables webhook update <endpoint_id> --clear-auto-run --json`. Arm it only on an address whose `authMode` is `secret`; on an open address anyone holding the URL could trigger paid lookups, so first run `oxygen tables webhook update <endpoint_id> --auth-mode secret --json` (free; it returns a new secret) and hand the founder the header.
5. Switch on the automatic lookup for new signups: `oxygen tables webhook update <endpoint_id> --auto-run-columns company_enrich,icp_fit --auto-run-max-credits 5 --json`. Leave `crm_person` out: a CRM-link column blocks the whole automatic run. OXYGEN has no command to send a test delivery yet, so ask the founder to submit one real signup, then check that `oxygen tables webhook deliveries <endpoint_id> --limit 5 --json` shows it with auto-run `queued`.
   Tell the founder: "New signups are now looked up the moment they arrive, at most 5 credits each."
6. Every morning (free): add new signups to the CRM with `oxygen columns run signups crm_person --limit 25 --approved --json`, then list the newest with `oxygen tables query signups --sort-json '[{"columnKey":"_created_at","direction":"desc"}]' --fields email,first_name,company_name,company_industry,company_headcount,icp_fit --limit 25 --json`. Replying by hand to the best fits is free and the fastest first touch.
   Tell the founder: "Here are the newest signups with their company and fit; answer the high-fit ones first."
7. Prepare the follow-up email (free; it sends nothing). Save this as `signup-followup.json`:
   ```json
   {"steps":[{"id":"s1","channel":"email","kind":"email_send","subject_template":"Quick question, {{first_name|there}}","body_template":"Hi {{first_name|there}},\n\nThanks for signing up. What do you want to get done first? Reply here and I'll point you to the fastest way.\n\n{{sender_first_name}}"},{"id":"w1","kind":"wait","days":2},{"id":"s2","channel":"email","kind":"email_send","body_template":"Hi {{first_name|there}}, did you get what you needed? One line back is enough.\n\n{{sender_first_name}}"}]}
   ```
   ```bash
   oxygen sequences create --name "Signup follow-up" --slug signup-follow-up --steps-file signup-followup.json --from-table signups --max-live-sends 20 --json
   oxygen sequences enroll signup-follow-up --from-table --json
   oxygen sequences start signup-follow-up --json
   ```
   The last command is the free launch preview; `--dry-run` would switch the sequence on in simulated mode instead.
   Tell the founder: "Your follow-up email is written and waiting; nothing has been sent."
> APPROVAL GATE — outreach-live: this emails real people. Show the preview's first rendered email, the sending mailbox, the send window (weekdays 09:00–17:00 UTC unless changed) and the cap of 20 emails in total. Say that each morning's enroll then emails the new signups in the next window, and that starting also switches on the free rule that files replies onto the CRM person.
8. Start the follow-up: `oxygen sequences start signup-follow-up --approved --max-live-sends 20 --json`, then add `oxygen sequences enroll signup-follow-up --from-table --json` to the morning step.
   Tell the founder: "New signups now get the follow-up email automatically, at most 20 emails until you raise it."

## If It Goes Wrong
- `crm_object_not_found` while adding or running `crm_person` → the contact lists are missing: Step 1.
- `approval_required` on `columns run` → read the `--dry-run` first, then add `--approved` and `--max-credits` set to its `recommended_max_credits`.
- Two prices in one preview (`estimated_credits` 2 beside "≈1" in `credit_guidance`) → the larger is the worst case when the first provider misses; billing usually lands near the smaller.
- A delivery shows `failed_to_enqueue` with `bind_create_auto_run_unsupported` → `crm_person` is in the automatic run: `oxygen tables webhook update <endpoint_id> --auto-run-columns company_enrich,icp_fit --json`. Rows skipped with `credit_limit_reached` → raise `--auto-run-max-credits`.
- `work_domain` empty for a company address → `oxygen formulas validate signups --expression 'if(email_type(email) = "work", email_domain(email))' --json`.
- `crm_relationship_target_not_found` from `oxygen crm assert people` with `company_domain` → assert the company first (its dry run does not catch this); the `crm_person` column avoids it.
- Launch preview blocker `sequence_no_sendable_mailboxes` → connect a mailbox with the email-infra-setup play, or keep replying by hand.
- `sequence_schedule_not_set` → emails go out on weekdays 09:00–17:00 UTC; change it with `oxygen sequences update signup-follow-up --schedule-timezone Europe/Berlin --schedule-days mon-fri --schedule-hours-start 09:00 --schedule-hours-end 17:00 --json`.
