# Cold email sending playbook

OXYGEN's recommended cold email setup: pick the playbook for the market, size the inbox count from the TAM, then set up lookalike domains, inboxes, photos and warm-up. Present these numbers to the user as OXYGEN's best practice and explain the reason behind each one. When the user wants other numbers, state the deliverability trade-off once, then plan with their numbers.

## 1. Pick the playbook

| | SMB and small business | Upmarket (mid-market and enterprise) |
| --- | --- | --- |
| Who it targets | Small and medium businesses, founders, agencies, local and SaaS companies. Recipients are mostly on Google Workspace | Larger companies and regulated industries (finance, legal, healthcare, public sector). Recipients are mostly on Microsoft 365 or Outlook, often behind a security gateway |
| Provider mix (share of daily sends) | 50% Google, 50% Microsoft 365 | 30% Google, 70% Microsoft. The Microsoft share can use Azure inboxes |
| Cold emails per inbox per weekday | Google 15, Microsoft 365 15 | Google 15, Microsoft 365 5, Azure 2 (an Azure inbox can never send more than 2) |
| Inboxes per domain | 2 | 2 for Google and Microsoft 365; Azure up to 100 on one domain |
| Warm-up before the first cold email | 2–4 weeks: at least 14 confirmed warm-up sending days, all 28 when time allows | 4 weeks: all 28 confirmed warm-up sending days |

- Microsoft recipients place better when the mail also comes from Microsoft, and Google recipients when it comes from Google. Sending from both providers also means one provider's filtering change cannot stop every send. Never put every inbox on one provider.
- Base the playbook on evidence, not on the first impression. Once leads are enrolled, `oxygen sequences esp <sequence> --json` counts them by Google, Microsoft or other at 0 credits. If one provider clearly dominates, move the mix towards it, keeping both providers in the plan.
- Azure inboxes are cheap per inbox but send very little each, so they add Microsoft volume when the TAM is large. One Azure domain sends at most about 200 a day. Every Azure inbox still needs its own natural address: dozens on one domain means several real senders with a few name variants each, or numbered addresses the user explicitly approves. When neither is available, plan Microsoft 365 inboxes instead.

## 2. Size the volume from the TAM

The target is to reach the whole TAM once every 60 days, sending on weekdays only.

1. **TAM contacts.** Count the people with a sendable email that the user will actually email, not the companies. If the user only knows the company count, multiply it by the contacts per company they plan to email.
2. **Emails per contact per cycle.** Use 1 by default. If each contact will get several email steps within the 60 days, count every step.
3. **Sending days.** A 60-day cycle has 42 weekdays (60 × 5 ÷ 7, rounded down). Public holidays lower this further.
4. **Daily sends** = TAM contacts × emails per contact ÷ 42, rounded up.
5. **Per provider.** Split the daily sends by the playbook mix. Inboxes = provider sends ÷ that provider's emails per inbox, rounded up. Round Google and Microsoft 365 counts up to an even number so every domain holds 2; Azure counts stay as calculated.
6. **Domains** = Google inboxes ÷ 2 + Microsoft 365 inboxes ÷ 2 + Azure inboxes ÷ 100 (each rounded up). A domain stays on one provider.

Worked SMB example: 10,000 contacts × 1 ÷ 42 = 239 sends a day. Each provider takes half, 120 a day, which at 15 per inbox is 8 inboxes. That is 8 Google inboxes on 4 domains and 8 Microsoft 365 inboxes on 4 domains: 16 inboxes and 8 domains for 240 sends a day.

Worked upmarket example: 3,000 contacts × 1 ÷ 42 = 72 sends a day. Google takes 30% (22 a day): 2 inboxes on 1 domain. Microsoft takes 70% (51 a day): 12 Microsoft 365 inboxes on 6 domains, or 26 Azure inboxes on 1 domain.

Show the user the inputs, the result and each rounding step. Ask for the TAM contact count when it is missing instead of guessing it. Warm-up traffic runs on top of these numbers; it is not counted in the cold-email volume. Because warm-up takes 2–4 weeks, order the next inboxes that long before the TAM or the cadence grows.

## 3. Set it up

Each step keeps its own preview and approval. Make one approval cover the whole plan by showing every domain, address, sender and quote together.

1. **Sender and photo.** Each inbox sends as a real person with their LinkedIn photo: create the sender profile from their connected LinkedIn account (`oxygen senders list --json`, then `senders profiles create --from-linkedin`), or upload a photo when there is none. Read back `avatar_durable: true` before ordering ([managed inboxes](managed-inboxes.md)); the name and photo can never be changed afterwards.
2. **Lookalike domains.** Never send cold email from the company's main domain. Search with `oxygen domains search <brand> --json`, then check up to 20 exact names with `oxygen domains check <name> <name> --json`. Good names are recognisable variations of the brand: `get<brand>.com`, `try<brand>.com`, `<brand>hq.com`, `meet<brand>.com`, `<brand>team.com`. Prefer `.com`; fall back to `.co` or `.io`. Avoid hyphens, numbers, misspellings of the brand, and `.xyz`, `.info` or `.biz`. Propose exactly as many domains as the plan needs, with their availability and checked prices. A managed domain's web root forwards to the company website by default.
3. **Inboxes.** For each domain, preview `oxygen managed-inboxes subscribe <domain> --provider <provider> --sender <sender_profile_id> --locals <two names> --max-per-domain 2 --json` (`google` or `microsoft`; Azure omits the limit). Saving the limit stops a later order from putting a third inbox on the domain. Use two natural variants of the sender's name, such as `philipp` and `philipp.hirte`; the same pair can repeat on every domain. Add up the quotes, show the `senders[]` stamp for every domain, and after approval place each order with `--approved --quote <quote_id>`. A domain the workspace already owns grows with `oxygen managed-inboxes add-inboxes <domain> --sender <sender_profile_id> --locals <names> --json` up to its saved limit. Details: [managed inboxes](managed-inboxes.md).
4. **Warm-up.** Keep the warm-up that a managed order includes by default (never `--no-warmup`); other inboxes enroll through [warm-up](warmup.md). Keep warm-up running while campaigns send, and never disable it on an inbox that is still sending.
5. **Daily caps.** New inboxes default to 25 cold emails a day. Set each inbox to its playbook number with `oxygen mailboxes cap set <mailbox> --daily-cap 15 --json` (5 for upmarket Microsoft 365 inboxes). Azure stays capped at 2 without this step. The campaign ramp still climbs to the cap.
6. **Weekdays only.** Sequences send Monday to Friday unless told otherwise: keep `mon-fri` in any sending schedule, and give a `--send-window-file` its weekday `days`, because a window file without days sends every day.

## 4. Readiness check

Until every inbox is ready, re-check after provisioning and then once a day. Report each inbox that is not ready, its cause and its next command; never report the plan as ready on a warming status alone.

- DNS: `oxygen domains list --attention --json` returns nothing for these domains.
- Sending authorization: run `oxygen mailboxes compatibility --mailboxes <planned-addresses> --json` with the plan's exact addresses, comma-separated. Require a matching `email_address` row in `data.compatibility` for every address, with `oxygen_native_send.state` equal to `connected`; missing, unknown or non-connected results remain unresolved. Use `oxygen mailboxes oauth-health --json` to diagnose missing authorization; absence from that bounded list does not prove readiness.
- Warm-up progress: `oxygen mailboxes list --stalled` and `oxygen mailboxes warmup status --json`. `ramp.confirmed_sending_days` must reach the playbook's minimum (14 for SMB, 28 for upmarket) before the first cold email.
- Capacity: add up each ready inbox's `effective_cap` from `oxygen mailboxes get <mailbox> --json`. The campaign ramp holds a new inbox at 5, 10, then 20 a day over its first nine sending days, so full capacity arrives about two weeks after the first cold email. Plan the first weeks' enrollments to fit. Then attach the senders to the Sequence (`oxygen-sequencer` skill).
