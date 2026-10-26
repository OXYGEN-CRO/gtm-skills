# Start with a useful job

Pick one job. Replace the bracketed fields with your own inputs. You can paste these prompts into OXYGEN or a connected terminal agent with this kit installed.

If you are starting from an empty workspace, provide your company website, what you sell, who buys, your goal and weekly GTM capacity. Existing workspace context comes first; public research does not establish internal facts such as pipeline, budget or available time.

## 1. Decide what to fix first

> Read the company, offer and ICP context already available in my workspace. Our goal is [goal] by [date], and we have [weekly GTM capacity]. Use existing data to assess our current funnel. Show the strongest evidence for the main bottleneck, what remains unknown and what could change your conclusion. Ask me to confirm the problem before designing a motion. Use free reads only.

Look for: a sourced snapshot, one proposed bottleneck and a question that could change the recommendation.

## 2. Build a target-account list

> Help me find accounts matching [ICP] in [market]. First propose the fit criteria, exclusions, output columns and sourcing approach. Separate verified facts from hypotheses. Show the available preview and the proposed credit ceiling. Wait for approval before paid sourcing. After approval, use a small pilot before expanding the list.

Look for: account-fit criteria, a preview, the proposed scope and a priced next step.

## 3. Find buyers at those accounts

> For [account or table], propose the roles involved in buying [our offer]: likely owner, user and approver. Explain the basis for each role. Show existing contacts first, then preview how you would find missing people and what it would cost. Leave unsupported roles and contact details unknown. Wait for approval before paid enrichment.

Look for: buyer-role hypotheses distinguished from verified people and a clear account-to-contact relationship.

## 4. Research and qualify accounts

> Turn [our ICP] into an account-fit rubric we can review. Separate hard exclusions, positive evidence and unknowns. Propose the research columns and source requirements for [table]. Show how the rubric would treat one existing row without paid research. Preview the cost of filling evidence gaps and wait for approval before running it.

Look for: evidence behind every grade and unknown values kept separate from negative evidence.

## 5. Prioritize warm opportunities

> Review only existing, accessible CRM, conversation and signal data for [audience]. Find relevant unanswered interest or timely reasons to reconnect. Rank by company fit, buyer role and strength of evidence. Engagement alone is not buying intent. Return a review list with sources and a suggested next action. Do not scrape, enroll or send anything.

Look for: actual fit and relationship evidence, prior-contact exclusions and an appropriate next action.

## 6. Prepare an outreach pilot

> For [reviewed audience] and [offer], prepare a draft outreach pilot. Propose the channel and explain why it fits. Check sender readiness, exclusions, do-not-contact and prior outreach. Show the exact audience, copy, schedule, send ceilings and previewed cost. Define a success bar, read window and stop condition. Keep everything unlaunched until I approve the concrete scope and budget.

Look for: a reviewable plan, not an already-running campaign.

## What a useful qualification result looks like

Illustrative example only. These are fictional inputs and an expected output shape, not researched companies or a performance claim.

Input: a company row says it sells B2B software, has a sales team, and operates in your target market. Its contract value is unknown. Your ICP requires a sales-led B2B software business; contract value is a preference rather than a hard gate.

```json
{
  "fit_label": "possible",
  "verified_fit": ["B2B software", "sales team", "target market"],
  "unknowns": ["annual contract value"],
  "disqualifiers": [],
  "rationale": "Observed fields support company fit; the preferred contract value is unverified.",
  "next_action": "research_more",
  "requires_human_review": true
}
```

Every real result should name the fields or sources supporting it. A missing value should not silently become a failed criterion.
