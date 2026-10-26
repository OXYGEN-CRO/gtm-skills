# Turn de-anonymized website visitors into warm pipeline

## The Play
You see which companies, and often which people, visit your website: each one lands in your OXYGEN CRM with the page they viewed and a score for how well their company fits who you sell to, and you pick the good fits for a personal note. It needs RB2B, a separate paid tool that names a minority of visitors (mostly US business visitors); OXYGEN does not identify visitors by itself, and today only OXYGEN support can connect RB2B to your workspace, because it needs a secret for your workspace that only support can give you; there is no self-serve step yet. With little business traffic it finds almost no one.

## Before You Start
- What you sell and who buys it: `oxygen context profile get --json` (free). If the ideal customer is empty, run the `day-1-first-win` play first and tell the founder you need to know who they sell to before you can say which visitors fit.
- RB2B on the website: no command can check it, so ask the founder; if nobody can say, treat it as not installed, explain what it takes and stop. Draft the step 5 support message only after the founder confirms RB2B is on the site. RB2B bills separately, not in OXYGEN credits. If they don't have it, tell them: identifying visitors needs RB2B installed on your site; sign up, add its snippet, and I'll ask OXYGEN support to connect it.
- CRM lists for companies and people: `oxygen crm setup --json` (free preview; `"action": "create"` means they are missing). Creating them also switches on automatic enrichment of every new company and person, which the preview quotes: roughly 10 credits per new visitor. The US mobile-phone lookup stays off unless the founder switches it on; then it adds 10 for each number it finds and nothing for a miss. When the lists already exist, quote what is switched on now instead: `oxygen crm enrichment list --json` gives each object's `credits_per_record`, and a visitor costs one company plus one person (lists created with `--without-enrichment` cost nothing and score nothing).
- Only to send messages later: a mailbox (reserves 100 credits a month) or a LinkedIn account (3,400 a month), a mailbox from the `email-infra-setup` play, LinkedIn from `inbound-led-outbound`, not here.

## Steps
1. Check what exists (free): `oxygen context profile get --json` and `oxygen crm setup --json`, then ask the founder whether RB2B is on the site. If it is not, stop after explaining what it takes; nothing else in this play works without it.
   Tell the founder: OXYGEN can show you who visits once RB2B is installed and connected; here is what that takes and costs.
> APPROVAL GATE — crm-enrichment: creating the CRM lists switches on paid enrichment of every new company and person, from any source, until it is turned off: roughly 10 credits per new visitor. Ask yes or no on the US mobile-phone lookup: off by default; on, it costs 10 per number found and nothing for a miss.
2. Create the lists (skip `crm setup --live` if the preview showed nothing to create), read the live per-record price, and set the phone lookup to the founder's answer: `enable` on a yes; on a no, `disable` only if the list shows it on:
   ```bash
   oxygen crm setup --live --json
   oxygen crm enrichment list --json
   oxygen crm enrichment enable person_mobile_phone --object people --json
   oxygen crm enrichment disable person_mobile_phone --object people --json
   ```
   Tell the founder: your CRM is ready, and each new visitor costs about <N> credits to fill in.
3. Install the visitor rule (free; it stays off): `oxygen recipes apply website-visitor-outreach --json`. The rule's id is `kit.stages[0].workflow.id` in the reply.
   Tell the founder: the rule that writes visitors into your CRM is installed but not switched on.
> APPROVAL GATE — signals-arm: a standing rule that writes every visitor RB2B reveals into the CRM (company from the email domain, the person, the page they viewed); free per visitor, cap 1 credit per delivery, running until `oxygen workflows disable <workflow_id> --json`. Switch it on before RB2B is connected: visits that arrive while it is off are not added later.
4. Switch it on (free): `oxygen workflows enable <workflow_id> --approved --max-credits 1 --reason "Website visitors into the CRM" --json`.
   Tell the founder: visitors will land in your CRM as soon as RB2B is connected.
> APPROVAL GATE — rb2b-connect: show the exact message that goes to OXYGEN support in the founder's name (free), and say that once support connects RB2B, every visitor it reveals flows into this workspace.
5. Ask OXYGEN support to connect RB2B (free); the answer arrives in the app's support chat and in `oxygen support list --json`:
   `oxygen support chat --message "Please connect RB2B website-visitor reveals to my workspace <workspace name>; RB2B is installed on <website>." --category configuration --json`
   Tell the founder: I asked OXYGEN support to connect RB2B; they will tell you what to enter in RB2B.
6. Once visits arrive, read them (free): `oxygen signals list --types website_visit --json` shows each visit, and `oxygen signals leads-today --json` ranks the people, with each company's fit.
   Tell the founder: these companies visited, and these fit who you sell to best.
7. Reach the good fits: for a handful, the founder writes a personal note; for more, run the `outbound-pilot-50` play with only those people. Before any message, check by hand that none is a customer, a competitor or someone who asked not to be contacted, because visitors known only by email skip the automatic do-not-contact check; never claim they read a specific page.
   Tell the founder: here are the good fits; write to them yourself, or I set up a small capped campaign.

## If It Goes Wrong
- `crm_object_not_found` from `signals list` → the CRM lists do not exist yet; do step 2 first.
- Nothing in `signals list` after support says RB2B is connected → `oxygen workflows runs --workflow <workflow_id> --limit 10 --json`: no runs means RB2B is not delivering yet, so reply on the support thread; a failed run says why.
- `workflow_standing_authorization_required` → `workflows enable` needs `--approved` and a positive `--max-credits`.
- `workflows enable` fails with a server error (seen in production) → run it once more, check `oxygen workflows get <workflow_id> --json`, then tell support.
- Credits going faster than expected → `oxygen crm enrichment list --json` shows what runs; `oxygen crm enrichment off --object people --json` (and the same with `--object companies`) stops it, and existing values stay.
- A company's fit reads `unknown` → the profile has no ideal customer yet; fill it with the `day-1-first-win` play.
- A company's fit is empty and `oxygen crm enrichment list --json` shows `company_icp_fit` with `"enabled": false` → visitors' companies are not being scored. Switching it on is part of the crm-enrichment gate. The score reads the company's LinkedIn profile, so after the founder's yes switch on both: `oxygen crm enrichment enable company_linkedin_profile --object companies --json` and `oxygen crm enrichment enable company_icp_fit --object companies --json`. Quote their `credits_per_record` added together (today 1 + 1.5, about 2.5 credits per new company).
