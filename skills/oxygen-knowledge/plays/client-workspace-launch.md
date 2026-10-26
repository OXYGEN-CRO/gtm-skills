# Stand up a new client workspace

## The Play
For agencies and freelancers who run OXYGEN for clients: each client gets their own workspace, so their data, mailboxes and spend never mix with yours or another client's. In about an hour the workspace exists and bills to your plan, OXYGEN researches the client's website for free, their brief fills in the rest, and the plays they will run sit in their wiki as pages your team can follow. For your own company, use day-1-first-win instead.

## Before You Start
- **A key that can switch workspaces.** Run `oxygen whoami --summary-json` (free): `auth_type` `user_session` or `oauth` can switch, and `org_api_key` cannot. Do not stop at `oxygen auth doctor --json`: it reads only a stored login, so for a key in `OXYGEN_API_KEY` it answers `switchable: null`. If the key cannot switch, it is locked to one workspace: create a user key at https://oxygen-agent.com/settings/cli and run `oxygen login --token <user key>`. If the key came from `OXYGEN_API_KEY`, first remove that variable where it is set (shell profile or agent settings): it outranks anything `oxygen login` stores. Free.
- **The client's website and a yes to create their workspace.** Only the founder can give these; create nothing until you have both. Never guess the website: OXYGEN researches whatever domain you pass and fills the client's profile from it. Ask: "What is <Client>'s website?" A client with no website can use its LinkedIn company page. The workspace named in the copied prompt is your own: you start there, it pays, and it stays as it is.
- **Your plan.** `oxygen whoami` names the plan; in `oxygen billing balance --json`, `plan.tier` and `spendable_credits` come after the long `available_plans` list. The launch is free on any plan. Once linked, the client's paid work draws on this workspace's credits: the 25-lead pilot (search, work emails, first lines) runs on any plan, Free included, when `spendable_credits` covers about 125. Mailboxes and other sending accounts need a paid plan (from $49 a month), whatever the credits; on a plan they are paid in credits where `oxygen billing estimate --mailboxes 1 --json` shows `"sender_billing": "credit_reservations"`.
- **No duplicate.** With a key that can switch, check `oxygen orgs list --json` for an existing workspace for this client and reuse it. A workspace-bound key lists only its own workspace, so say that this check waits for the new key.
- **The brief.** What the client sells, to whom (titles, company size, countries), why they win, their goal, and who never to contact (competitors, current customers, open deals). Write "unknown" for anything the brief lacks.

## Steps
> APPROVAL GATE — client-workspace-create: the client's name and website, that this creates a new permanent workspace, that OXYGEN researches the website once at no cost, that it bills to your workspace <name>, and the monthly credit cap for it (suggest 2,000 credits); create it only after a yes.
1. Create the workspace, switch into it and bill it to your plan — free.
   ```bash
   oxygen orgs create --name "<Client>" --company-domain <client website> --json
   oxygen orgs use <clerk_org_id from the reply> --json
   oxygen context profile get --json
   oxygen orgs billing-link --owner <id of the paying workspace> --monthly-credit-cap 2000 --json
   ```
   `context profile get` must show an empty profile or the client's, never yours; if it shows yours, run `orgs use` again. In the billing-link reply, `plan_tier: free` means your plan is Free: the client's pilot still runs on your credits, and so do its mailboxes and sending where sending is paid in credits (see Your plan above).
   Tell the founder: "<Client> has its own workspace now, paid from your plan and capped at 2,000 credits a month."
2. Let OXYGEN research the client's website — free, OXYGEN pays. Re-check `oxygen knowledge bootstrap status --json` every couple of minutes until it reads completed, partial, skipped or failed; after 15 minutes, carry on. Writing the profile first cancels this research, so wait for it.
   Tell the founder: "OXYGEN is reading <Client>'s website to fill in their company profile, at no cost to you."
3. Add the brief and a positioning page — free.
   ```bash
   oxygen context profile update --data-json '{"icp":{"segment":"<who they sell to>","titles":["<buyer titles>"],"employees":"<range>","countries":["<codes>"]},"offering":{"what":"<what they sell>","goal":"<e.g. 30 qualified demos a quarter>"},"custom":{"do_not_contact":"<competitors, current customers, open deals>"}}' --summary "Client brief for <Client>" --json
   oxygen knowledge page upsert --slug positioning-<client> --type positioning --title "<Client> positioning" --status active --body "<one-liner, who they sell to, why they win, proof>" --json
   ```
   The update merges into what the research found and keeps it.
   Tell the founder: "<Client>'s profile now says who they sell to and who never to contact, so every draft speaks as <Client>."
4. Install the plays they will run — free; each install writes a wiki page, with no preview.
   ```bash
   oxygen recipes install icp-to-account-map --json
   oxygen recipes install outbound-pilot-50 --json
   oxygen recipes install reply-to-meeting --json
   oxygen knowledge page list --type playbook --json
   ```
   Add email-infra-setup if they will send cold email from new domains, and migrate-from-clay if they come from Clay; add `--draft` to a play the client has not approved yet.
   Tell the founder: "<Client>'s workspace holds the three plays as pages your team can run from."
5. Name the first paid step and stop — free. It is a 25-lead pilot in the client's workspace (`oxygen recipes show outbound-pilot-50 --json`): about 125 credits from your plan (1 to find them, about 85 for work emails at about 3.3 each, about 38 for AI-written first lines at 1.5 each). That play quotes and caps each step before it spends. Do not price it with `oxygen billing estimate --enrich work_email`: it overstates work emails (about three times the measured cost on 2026-10-05) and its plan fit ignores your balance. Sending later needs the client's own mailbox, 100 credits a month each.
   Tell the founder: "Next is a 25-lead test for <Client>, about 125 credits; I'll show the exact price before anything runs."

## If It Goes Wrong
- `orgs use` refuses with `org_scoped_credential`, or `orgs create` refuses a workspace API key → this terminal holds a workspace-bound key: create a user key at https://oxygen-agent.com/settings/cli, then `oxygen login --token <user key> --profile <client> --org <client workspace>`. If `OXYGEN_API_KEY` is set, remove it first, or the old key keeps answering.
- `organization_selection_required` → no workspace is selected: `oxygen orgs use <client workspace> --json`.
- `workspace_creation_failed` with `details.field` set to domain → the website was not accepted; use the bare domain (acme.com) or the client's LinkedIn company page URL.
- `cli_update_required` (seen 26 times on `context profile update` in production) → `oxygen update`, then re-run.
- `oxygen knowledge bootstrap status --json` reads skipped or failed → the brief alone is enough. A manual research run costs up to 150 credits; `oxygen knowledge bootstrap --json` previews it free, and it runs only after the founder agrees.
- `orgs billing-link` refuses → you need admin rights in both workspaces, the paying workspace must pay for itself (`nested_billing_owner_not_supported`), and a client workspace with its own plan must cancel it first.
- An installed play does not shape the client's drafts → it went in with `--draft`; install it again without it.
