---
name: oxygen-linkedin-content
description: "Plan and write a week of LinkedIn posts from the workspace's Knowledge: pillars, funnel job, idea gate, hook, body, slop scrub, graphics rendered with OXYGEN visuals, review, hand-off to Publishing for approval, and learning from post analytics. Also a manual comment round."
allowed-tools: Bash(oxygen *)
---

# OXYGEN LinkedIn content

A post is a public write in the user's name. This skill writes drafts; `oxygen-publishing` queues them and nothing goes out until the user approves each post. Drafting here costs 0 credits.

## 1. Ground

Read before writing a word (all free):

```bash
oxygen context canonical get --type voice --json
oxygen knowledge resolve --purpose outbound_copy --json
oxygen knowledge search "content pillars" --json
oxygen knowledge search "proof cleared numbers" --json
oxygen publishing analytics summary --channel linkedin --range 90d --sort engagements --limit 50 --json
oxygen publishing posts list --status published --order newest --limit 30 --json
```

- Pages this skill uses, found by search before you mint a slug: voice (canonical), `content-pillars`, `proof`, `content-performance`, `content-anti-patterns`. Open each with `oxygen knowledge page get <slug> --json`.
- A page counts as a stub when it is missing, `status: draft`, or still says "Stub"; a voice read with `present: false` has none pinned. If voice, pillars or proof is a stub, stop and say which, then offer setup: pillars in [pillars and learning](references/pillars-and-learning.md); voice and proof through the `oxygen-knowledge` skill. Drafting from an empty identity produces the generic posts this skill exists to avoid.
- A stub voice does not block editing a draft the user supplies: keep their wording and say the voice is not calibrated.
- Read the analytics as `oxygen-publishing` teaches (`oxygen skills get oxygen-publishing --file references/analytics.md`).

## 2. Plan the week

- Cadence: use the one on the pillars page. If none is set, ask, and offer 4 a week, 1 per pillar.
- Each post gets exactly 1 pillar, topic, subtopic and funnel job.
- At most 1 hard ask in the week.
- Do not reuse a subtopic from the last 4 weeks or a topic from last week. Posts carry their topic and subtopic as tags (step 8): check with `oxygen publishing posts list --tag subtopic:<slug> --order newest --limit 1 --json`. Posts published before this skill have no tags; read their text instead.
- Never create a new pillar or topic to fill a slot, and never fabricate a post to hit the count: plan what the material supports and name the source still needed for the rest.

Tree, funnel stages and the starting weekly mix: [pillars and learning](references/pillars-and-learning.md).

## 3. Idea gate

Every idea passes all six before drafting:

1. Traceable receipt: a real source (result, call, ship, named event, metric, first-hand experience).
2. The author lived it: they can say "we built", "we tested", "we booked", "I saw".
3. Useful to the workspace ICP (from `knowledge resolve`).
4. Specific: at least one number, period, named tool, event, company, workflow or before/after.
5. Fits a pillar and the positioning.
6. Honest and private: no invented metric, no identifiable customer detail without clearance.

Verdict per idea: PASS, REPAIR (name the failed gate and the exact proof needed) or REJECT. Do not repair by inventing a stronger claim; missing proof stays missing. Rank passing ideas against each other in pairs, never on a 1-10 score. Offer 3 to 5 ideas; the author picks.

Numbers: a number appears only if it is on the `proof` page with its definition, unit, period, source and public-use status. Never round up, never sum metrics from different sources, call a window above 1.5x its trailing average a spike. If an uncleared number would carry the hook, write the line without it and flag it.

## 4. Hook

Line 1 and the opening: [hooks](references/hooks.md). Pick a hook family that differs from the families of the last 2 published hooks.

## 5. Body

Structure, the skim test, the shape targets, the slop scrub and the banned closers: [body and slop](references/body-and-slop.md).

## 6. Graphics

Whether a post gets a graphic, and rendering it with `oxygen visuals` (free) and inspecting the pixels: [graphics](references/graphics.md). Visual identity comes only from the workspace's canonical brand page (`oxygen context canonical get --type brand --json`); never invent a brand, logo or palette.

## 7. Review

Show each draft exactly as it will post, then, outside the copy:

- pillar, topic, subtopic, funnel job, and which post carries the week's ask;
- hook family, line 1 character count and total characters;
- the skim skeleton, verbatim;
- slop scrub: `0 hits` or what was caught and rewritten;
- every number left out pending clearance on the `proof` page;
- the graphic's evidence state (see graphics).

No process commentary inside the copy. A planned date is not a scheduled post.

## 8. Hand off to Publishing

Queue through `oxygen-publishing` (sender check, scheduling, approval, locks and media live there):

```bash
oxygen publishing posts create --text-file post.txt --sender <sender_id> --publish-at <iso> --timezone <tz> --tags "pillar:<slug>,topic:<slug>,subtopic:<slug>,funnel:<top|middle|bottom>" --json
```

- It lands `needs_approval`; nothing sends until the user approves that post. Approval, revocation on edit, and locks: `oxygen-publishing`.
- A link goes in `--first-comment`; a link to the user's own site carries UTM parameters (source `linkedin`, one campaign slug per piece).
- Write drafts yourself; the paid `publishing posts draft` templates do not apply these rules.

## 9. Learn

After posts have run, compare the top 5 with the bottom 5 and file the finding, and log every rejected draft or user edit: [pillars and learning](references/pillars-and-learning.md).

## Comment round

Comments under other creators' posts, drafted for the user to post by hand: [comment round](references/comment-round.md). OXYGEN never comments, likes, connects or messages for the user in this round. Each paid thread read needs its dry-run quote, the user's yes and `--max-credits`.

Return the Knowledge slugs used, the queued post deep-links and the analytics deep-link.
