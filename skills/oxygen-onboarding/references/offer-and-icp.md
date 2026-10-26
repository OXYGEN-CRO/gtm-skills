# Offer and ICP

Reference for step 1 of the consultant, and for the ICP that step 3 tests on real matches. The offer says what the user sells and why a buyer should care now; the ICP says which accounts and people that is true for, and when. Both start as drafts from evidence and get sharper when the user reacts to real leads, so draft them fast and never hold the leads back for a perfect version.

## Evidence, in order of trust

1. What the user says now.
2. The user's own material: their website and, in a coding agent, the folder you were started in (README, docs, pitch or pricing notes, customer lists, win/loss or call notes, past campaign copy).
3. OXYGEN's research: the onboarding read's `profile` and `onboarding.hypotheses`, and the cited page from `oxygen knowledge page get company-research --json`.
4. How buyers describe the problem in reviews, communities and their own posts, when you can browse.
5. Your own inference, labelled as such.

Ask only for what evidence cannot answer and what would change your recommendation, one question at a time: usually who their best customers are, and whether they sell for themselves or for clients.

## The offer in five lines

| Line | Strong | Weak |
| --- | --- | --- |
| Product and category, as a buyer would name it | "Invoice chasing for creative agencies" | "AI-powered finance platform" |
| The buyer's problem, in their words, and who feels it | "Agency owners lose two days a month chasing late client invoices" | "Inefficient finance processes" |
| Outcome and proof: a number or a named customer | "Paid 11 days sooner on average across 40 agencies" | "Get paid faster" |
| Price and buying motion: entry price, who signs, how they buy | "$99 a month, self-serve; the agency owner buys" | missing |
| Why it beats the alternative they use today: the status quo, doing it in-house or a named competitor | "Replaces a bookkeeper's chasing; clients now pay by link" | "Best-in-class" |

No number, no claim: a proof line without a number or a named customer is unproven, and you say so. When a line has no evidence, write the most likely answer, mark it as a guess and name the one question that would settle it.

## The ICP

| Part | What to write | Searchable as |
| --- | --- | --- |
| The job | The recurring problem the product solves, who owns it, who operates it and how its first success is measured | — |
| Company fit | Industry, business model, size, stage or funding, geography | `oxygen companies search filters --json` |
| Buyer and user | The person who signs and the person who uses it: titles, seniority, department | `oxygen people search filters --json` |
| Triggers | Events that put an account in market now: hiring for the problem, new funding, a new leader in the buying role, a tool change, posting about the pain | `--source hiring` on company search; `oxygen signals search preview` |
| Who is out | Too small, wrong model, an existing customer, a competitor's customer under contract | exclusion filters |
| Basis | The customers, deals or calls the ICP is drawn from | cited evidence |

Best customers are the strongest basis: when the user names two to five, ask what they have in common and how they differ from deals that were lost. Lookalikes of a logo are not wins, and engagement with the user's posts is not fit.

Quality bar:

- It names the segment, the size, the geography and who is out, or it is not an ICP yet.
- Two people would build the same list from it.
- Company fit, buyer fit and the route to the buyer stay separate judgements.
- Unknown is not a low fit, and there are no invented 0–100 weights; call a match strong, possible or weak and say why.
- One sharp segment beats three vague ones. Name the others as later options.

## Test it on real matches

Do not ask the user to write or approve the ICP before showing anything. Map it to filters, run a free preview (`oxygen companies search preview --filters-json '<filters>' --json` or `oxygen people search preview --filters-json '<filters>' --json`) and show the first matches next to the warm leads. Rule of thumb: when most of the first page plausibly fits, the ICP is sharp; when fewer than half do, tighten it. "Do these look like your buyers?" sharpens an ICP faster than any questionnaire.

## Save what the user confirms

Read before you write: a profile update makes the onboarding read drop the research hypotheses, so keep them in your notes first ([consultation](consultation.md)). Then patch only what the user confirmed or corrected:

- The typed profile, which grounds every later draft and score: `oxygen knowledge profile update --data-json '<patch>' --json`. Read the exact grammar first with `oxygen commands get "knowledge profile update" --json`. `offering` holds `product`, `value_prop`, `use_cases` and `proof_points`; `icp` holds `target_accounts`, `buyer_personas`, `user_personas` and `disqualifiers`; `market.alternatives` holds what the buyer uses today.
- The `icp` and `offers` wiki pages hold the full version, including triggers and the basis. Filling them from draft to active needs no approval; canonical positioning and voice still go through a proposal.

Record the decision so the next session starts from it: `oxygen knowledge log append --event decision --summary "<offer and ICP confirmed>" --json`.
