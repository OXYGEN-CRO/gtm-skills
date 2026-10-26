# Pillars, funnel and learning

## The pillar tree

Start from 4 pillars, 4 topics per pillar and 4 subtopics per topic: a starting point the user may change, not a requirement to manufacture 64 ideas.

- A pillar is a recurring reader need the author can credibly address, with a promise (what the reader gets) and a boundary (what does not belong). Test: can you name what it argues against? If not, it is a category.
- A topic is a recurring question inside a pillar; a subtopic is a one-sentence thesis that can carry many posts, never a post title.
- Contrarian, list, story and giveaway are formats, not pillars.
- Replace, do not add: a new idea replaces the weakest. A topic with no post in 6 months gets parked.
- Each topic carries its usual funnel job: T, M or B.
- Names stay proposals until the user adopts them; preserve an existing taxonomy unless asked to revise it.

## Setup interview

Ask only what `knowledge resolve` did not answer: the reader and the buyer (an audience that spreads content is not always the one that buys); what the author can credibly speak about from their own work; the real next step they offer today (a missing offer can stay open while top and middle posts are planned); cadence, posting days and time zone. Then file the tree on one page:

```bash
oxygen knowledge search "content pillars" --json
oxygen knowledge page upsert --slug content-pillars --title "Content pillars" --type strategy --status draft --body "<the tree>" --json
```

Per pillar: promise, boundary, what it argues against, topics with subtopics and funnel letter; then the weekly grid and the cadence. Set `--status active` once the user adopts it.

## The funnel job

| Stage | Job | What it may ask for |
| --- | --- | --- |
| Top | Earn attention from the right reader | Nothing: no product, no link, no ask |
| Middle | Teach the method and build trust | A conversation, a resource, a reply |
| Bottom | Connect the problem to what is sold | The actual next step: signup, call, purchase |

- One stage per piece; a post that tries two does neither. Undecided means top.
- Top names one person's situation and ends without an ask; that restraint lets the bottom post land.
- Middle is usable without buying and names the tradeoff, not just the win.
- Bottom shows a real case with dates, says who it is not for, and has exactly one next step.
- Starting mix: 2 top, 1 middle, 1 bottom a week. Adjust on the account's own evidence and record why on the pillars page.

## The learning loop

Before each weekly plan, from the 90-day summary read in Ground:

1. Read `totals.published_posts`, `coverage` and `freshness` first. Under 10 posts the top 5 and bottom 5 overlap: report the numbers and draw no rule.
2. Compare the top 5 `top_posts` with the bottom 5. Above 50 posts the list's tail is not the range's bottom: say the bottom 5 are unavailable.
3. For each group note line 1, hook family, funnel job, length and whether a graphic ran. Pillar, topic and subtopic come from the post's tags: match `top_posts[].id` against `oxygen publishing posts list --tag pillar:<slug> --status published --json`.
4. Name one difference between the groups that the next week can test. A fading winner gets a new mechanism, not a bigger number ([hooks](hooks.md)).
5. File it on `content-performance` (date, range, the comparison, the next test) with `--expected-revision` from the page you read, then `oxygen knowledge log append --event note --slug content-performance --summary "<finding>" --json`.

After every review, add each rejected draft and user edit to `content-anti-patterns`: what was written, what the user changed, the rule it suggests. A pattern seen twice becomes a rule there. The user's edits are the strongest voice signal.
