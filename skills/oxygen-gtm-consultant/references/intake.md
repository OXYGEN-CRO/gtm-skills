# Intake

Reference for the consultant's context gate: what you must know before prescribing a motion, where OXYGEN already holds it, and what to ask when it does not. Every read is free; run each as its own command or tool call and read its result whole.

## The minimum context set

"Gate" items are required before you design a motion; "useful" items sharpen it. In MCP, the onboarding read is `oxygen_context_resolve` with purpose `onboarding`; reach any other read your tool list lacks through `oxygen_capabilities_read`.

| # | Item | Gate | Where OXYGEN has it | Ask when it is missing |
| --- | --- | --- | --- | --- |
| 1 | Company: website or LinkedIn company page | Gate | `oxygen knowledge resolve --purpose onboarding --json` (`profile.company`, `onboarding.researchState`, `brief`, `hypotheses`, `unknowns`); `oxygen knowledge page get company-research --json` | "What is the company's website?" |
| 2 | Offer: product and category, the buyer's problem, proof, price and buying motion, the alternative it beats | Gate | `oxygen knowledge profile --json` (`offering`, `market.alternatives`); `oxygen knowledge page get offers --json` | The onboarding skill's five-line offer; "Roughly what is a first-year deal worth, and who signs?" |
| 3 | ICP and its basis | Gate | `oxygen knowledge page get icp --json`; customers with `oxygen tables query companies --filter-tree-json '{"type":"group","conjunction":"and","children":[{"type":"leaf","columnKey":"lifecycle_stage","operator":"is","value":"customer"}]}' --json` | "Name two or three of your best customers. What do they share, and how do they differ from deals you lost?" |
| 4 | Stage and traction | Gate | `oxygen dashboards summary --range 90d --json`; won deals in `oxygen crm pipeline --json`. New workspaces carry sample records, marked `_sample: true` (`sample: true` on pipeline deals); they are never evidence | "Roughly how many paying customers do you have, and where did the last ten come from?" |
| 5 | Team, roles and weekly GTM hours | Gate | Not in OXYGEN; workspace membership is not capacity | "Who does sales and marketing today, and how many hours a week can they give this?" |
| 6 | Goal: one number, one stake, one date | Gate | Earlier decisions in `oxygen knowledge log list --json` and `oxygen knowledge page get decisions --json`; targets in `oxygen knowledge page get metrics --json` | "What should be true in 90 days, in one number?", then "What happens if it is still not true by then?" |
| 7 | Current motion, channels and volumes | Gate | `oxygen dashboards summary --range 30d --json`; `oxygen sequences list --stats --json`; `oxygen sequences analytics --range 30d --json`; `oxygen publishing analytics summary --channel linkedin --json`; the onboarding read's `workspace` counts, where `null` means unreadable, not zero | "Is there outreach, a CRM or a channel outside OXYGEN I should know about?" |
| 8 | Constraints | Gate | `oxygen limits show --json`; `oxygen budget list --json`; `oxygen billing balance --json` | "Is there anything we must not do: domains, brand, regions, compliance, tools you must keep?" |
| 9 | Tools and data assets | Useful | `oxygen integrations list --json`; `oxygen linkedin network status --json`; `oxygen senders list --json`; `oxygen mailboxes list --json` | "Do you have a CRM export or LinkedIn's Connections.csv?" |
| 10 | What was tried, and how it was judged | Useful | `oxygen knowledge page get campaign-learnings --json`; paused or finished sequences in `oxygen sequences list --json`; `oxygen knowledge log list --json` | "What did you try that didn't work, and how long did you give it?" |
| 11 | Who approves spend and launches | Gate before launch | `oxygen whoami --json`; pending items in `oxygen observability approvals --json` | "Who approves spend and outreach on this?" |

When you are unsure whether a command only reads, check it first: `oxygen commands get "<exact command>" --json` reports whether it spends credits, changes state or previews by default.

## Context strength

Use labels, not invented scores.

| Level | Test | What you do |
| --- | --- | --- |
| **Strong** | Every gate item is known, and the goal, the team's capacity and current results come from the user or from workspace data, not only from public research | Full engagement: diagnosis, problem statement, motion, pilot. |
| **Partial** | Offer and ICP are known (confirmed or researched), but one or two gate items are missing, typically capacity, current volumes or the goal | Diagnose provisionally, label each conclusion that depends on a missing item, ask the most decision-changing question in the same answer, and build or spend nothing until it is answered. |
| **Weak** | Only public research or nothing at all: no workspace activity, no statements from the user | Say it in your first sentence ("My read is weak: I know your website and nothing about your pipeline, team or goal"). Run the free reads anyway, show what they found, give at most two labelled hypotheses and ask one question. When the offer or ICP is missing, run the onboarding skill first. |

## Thin-context protocol

1. **Read before you ask.** One combined read first, then the current-state reads in parallel ([assessment](assessment.md)). Ask only what a free read cannot answer.
2. **Use the folder and the web.** In a coding agent, read the working folder (docs, pricing notes, CRM or LinkedIn exports) and upload nothing without asking. With web access, read the company site before you offer OXYGEN's paid, capped research run.
3. **Keep three kinds of knowledge apart** in every answer: evidence (with the read or URL), inference (labelled) and the user's decisions. The user's statements outrank research.
4. **Public research never establishes internal facts**: lead volume, process, tools, budget or buying authority. Those are gate items you ask for.
5. **Ask the highest-value question.** Of the missing gate items, ask about the one whose answer would change the recommendation most, and offer your recommended answer with it. When everything is missing, the default order is: the goal and its date, then current results and where deals came from, then team capacity, then constraints.

## Agency mode

When the user runs OXYGEN for clients, the company is the client. Confirm the active workspace is that client's, read that workspace, and add two gate items: the agency's committed hours per week and what the client must approve. The `client-workspace-launch` play (`oxygen recipes show client-workspace-launch --json`) is the inspiration for standing a client up.
