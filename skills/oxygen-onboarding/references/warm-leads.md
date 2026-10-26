# Warm leads

Reference for step 3 of the consultant: find the warmest people the user can reach now, rank them, and say what each missing source would add. A blank workspace (`plays.workspace` is `blank`: nothing connected or running and only the sample CRM records) has no warm rung to read: go straight to the net-new previews. Every read here is free. A step that spends credits, sends or runs on a schedule says so, previews first and runs only after the user approves a cap.

## Inventory first

Before recommending anything, know what you can read. The onboarding read's `workspace.access` shows the connected LinkedIn accounts, mailboxes and integrations, and `workspace.data` shows what tables and records exist. In a coding agent, also look in the folder you were started in for a customer list, a CRM export or LinkedIn's `Connections.csv`: reading a local file costs nothing and often holds the warmest names of all.

## The warmth ladder

Work top-down and stop descending once you have about ten strong leads. A name on a warmer rung beats ten on a colder one.

| Rung | Who | Read it with | Needs |
| --- | --- | --- | --- |
| 1. Existing relationships | Customers who could expand or refer, open and stalled deals, closed-lost deals worth a second look, replies showing buying interest whose last message is theirs, conversations that went quiet | `oxygen crm pipeline --json`; `oxygen inbox list --status interested --unanswered --json`; customers with `oxygen tables query companies --filter-tree-json '{"type":"group","conjunction":"and","children":[{"type":"leaf","columnKey":"lifecycle_stage","operator":"is","value":"customer"}]}' --json` | CRM records, a connected mailbox or LinkedIn account |
| 2. People who know the user | LinkedIn connections and followers, profile viewers, people who reacted to or commented on their posts | `oxygen crm signals leads-today --within-days 30 --json`; `oxygen linkedin network status --json`, then the table it names with `oxygen tables query <table> --json` | A connected LinkedIn account; network capture running |
| 3. People showing intent | Website visitors, people posting about the problem, ICP accounts with a fresh trigger | `oxygen crm signals leads-today --json` (visits come first); `oxygen signals search preview --keywords "<the buyer's problem>" --json`; `oxygen companies search preview --source hiring --filters-json '{"job":{"title":{"include":["<role that owns the problem>"]}}}' --json` | Armed signal sources for visits and views; nothing for the previews |
| 4. Net-new ICP matches | People who fit the ICP with no relationship yet | `oxygen companies search preview --filters-json '<ICP filters>' --json`; `oxygen people search preview --filters-json '<ICP filters>' --json` | Nothing |

The post preview spends a small hourly search budget shared across OXYGEN, one search per keyword: use one keyword, and when the preview says this hour's searches are used, say so and move on.

For net-new matches, start from the enumerated fields the filter list shows (industry, employee count, HQ country, job title, job level), and add `keywords.include` with one or two words for a niche the industry list cannot name. Every filter group takes an object, for example `{"keywords":{"include":["outbound agency"]}}`. People filters nest, for example `{"people":{"job_title":{"include":["Head of Growth","Founder"]}},"company":{"employee_count":{"min":10,"max":200}}}`. If most of the first page misses, tighten once and preview again.

Account stages are workspace-configurable; read them with `oxygen crm describe companies --field lifecycle_stage --json` before filtering. One account or person: `oxygen crm search "<name or domain>" --json`.

Where `plays.leads` starts with a `focus` read, run that read first. It ranks CRM people across rungs 1 to 3 at once (warmth, then fit, then decayed inbound intent), with reason codes, evidence ids to cite and who on the team knows each person. It already leaves out do-not-contact, enrolled and closed leads, so read the other rungs only for what it cannot see: open deals, unanswered replies, posts and net-new previews.

`crm signals leads-today` ranks CRM people by their strongest recent signal (a website visit, then a profile view, a post reaction, a new follow) and skips do-not-contact entries. It sees only people already in the CRM, so an empty answer means no source is armed or delivering yet, not that nobody is warm. To run one LinkedIn audience as a campaign, start with the user's own post engagers, then profile viewers, then followers.

In MCP, the onboarding read lists these same reads under `plays.leads`, each with its exact call through `oxygen_capabilities_read`.

## When a rung is empty

Say in one line what would fill it, then move on to the next rung. Never stop the analysis to wait for setup.

- **No CRM data:** a customer list or CRM export in the folder is the fastest first look. Read it locally and show the warm names; importing it (`oxygen tables import --file <path> --create "<name>" --json`, free) needs the user's yes. Connecting HubSpot, Attio or Pipedrive brings records in through `oxygen crm sync import`, preview first.
- **No LinkedIn account:** LinkedIn's own data export (Settings, Data privacy, Get a copy of your data, Connections) gives the user a `Connections.csv` to read right away. Connecting an account lets `oxygen linkedin network setup` capture connections and followers into a table; connecting carries a monthly cost the connect preview shows, and capture fills over days, so start it early.
- **No mailbox:** past replies stay invisible until one is connected.
- **No signal sources armed:** the post and hiring previews on rung 3 still work today. Arming visitors, profile viewers, engagers or followers is a standing step with its own cap.

## Rank and present

1. **Merge by person.** One person can appear in several sources; keep one row and list every touchpoint as evidence.
2. **Gate on fit and eligibility.** Drop do-not-contact entries, people already in an active conversation or sequence, and anyone who is plainly outside the ICP. Engagement is not fit, and a phone number or email address is not permission to contact. A new workspace starts with sample records, well-known companies such as Stripe and Vercel with their CEOs (on `.example` addresses) and deals with them. Every read marks them `_sample: true` (`sample: true` on `crm pipeline` deals) and pipeline totals leave them out; they illustrate the CRM and are never leads. When they are all the CRM holds, say it has no real relationships yet. Only the user makes one real (`oxygen crm keep`).
3. **Rank by warmth, then fit, then recency.** A customer or an open deal beats an unanswered reply, which beats any one-way signal; among signals, a comment or repeated engagement beats a single reaction, follow or profile view. Call fit strong, possible or weak and say why.
4. **Need a person.** A company event such as funding or hiring is a reason to reach someone at that company, not a lead by itself.

Show about ten in one table:

| # | Person | Company | Why warm | Fit | Next step |
| --- | --- | --- | --- | --- | --- |
| 1 | Name, title | Company | Rung and evidence the user can check, for example "replied 'interested' on 12 Sep, never answered" | Strong: B2B SaaS, 40 people, Head of Growth | Personal reply today, drafted below |

Never end on an empty list. When the warm rungs are empty, show about ten real, plausible matches from the free previews and say which source would add warmer names.

- **A near-empty preview is a filter too narrow for the data.** When a company or people preview returns fewer than about ten, loosen it once (drop keyword filters first, then widen the size band or the titles) and preview again before you report what you found.
- **Two plausible segments: list the stronger one first.** When the research or the user's answers point at more than one segment, do not ask which one before the first list. Build and save the list for the segment the evidence favors, then offer the other segment as your closing question.

## The right next step per rung

- **Customers:** a personal referral or expansion ask, never a sequence.
- **Open and stalled deals:** a follow-up that references the last conversation.
- **Unanswered replies:** answer today; this is the highest-value message in most workspaces.
- **Closed-lost and quiet conversations:** revisit when something changed: a new trigger, a new feature that answers the lost reason, or two or more recent signals.
- **Network and engagers:** a personal note that references the connection or the post they engaged with.
- **Intent:** a timely message tied to the trigger, sent while it is fresh.
- **Net-new matches:** a small, capped sequence on the strongest fits, after the warmer rungs are worked.

A strong fit gets a message in the user's own voice from their own account. New LinkedIn accounts start slow on purpose, a few invites and messages a day, so a blast is never the plan.

## Scoring more than a handful

When the user wants a larger set scored against the ICP, add an AI fit column to the table: `oxygen columns add <table> --label "ICP fit" --score "weak,possible,strong" --prompt "<fit rule from the ICP>" --grounding workspace --json`, then `oxygen columns run <table> <column> --dry-run --json` to preview the cost before running it live with an approved cap. Score a sample of 25 rows first (`--limit 25`) and read it with the user before scoring the rest.
