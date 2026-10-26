---
name: oxygen-publishing
description: "Use OXYGEN Posts and Publishing to draft, queue, approve, schedule and read back LinkedIn and X posts, answer public comments on owned posts, and read post analytics. Covers approval axes, the uncertain-publish lock, mentions, media, X threads and polls."
allowed-tools: Bash(oxygen *)
---

# OXYGEN Publishing

Posts hold broadcast artifacts and what happened to them: comments, reactions, performance. Publishing schedules, approves, dispatches and retries them with attempt history. A post is a public write in someone's name, so every post the user has not seen stays unapproved.

## Two ways to publish

- The queue (default): `publishing posts create` saves a post for its publish time, a person approves it, and the scheduler dispatches it, retries a rate-limited provider and records every attempt.
- Direct LinkedIn publish: `oxygen posts create --text-file post.txt --account <sender> --json` previews; `--approved` publishes immediately outside the queue.

Channel details: [LinkedIn](references/linkedin.md) (mentions, media, video cover, first comment, own-feed limits), [X](references/x.md) (threads, polls, alt text, reply settings). Public comments: [comments](references/comments.md). Performance: [analytics](references/analytics.md).

## Save a draft for review

A post the user asked for but has not approved is saved, not left in chat:

1. Read the voice page (`oxygen knowledge page get voice --json`) and use only numbers a page states.
2. `oxygen publishing posts create --draft --publish-at <iso> --text-file post.txt --json`. A draft needs no sender, publishes nothing and stays unapproved.
3. Say it is a draft, not live, and give its `web_url`. If the save is refused, say the post exists only in the chat.

"Post it now" also saves first: publishing waits for the user's approval of the exact text and a connected sender.

## Queue a post

1. Check the sender: `oxygen senders list --json` shows it `active`. A post bound to a disconnected or restricted sender never dispatches, and approval refuses it; reconnect first.
2. Write the text from the workspace's stored context (`oxygen knowledge resolve --purpose outbound_copy --json`). Mark any offer detail the context does not state as `[confirm]` for the user instead of inventing it.
3. Create without approval: `oxygen publishing posts create --text-file post.txt --sender <sender_id> --publish-at <iso-instant> --timezone <tz> --json`. A `--publish-at` with `Z` or an offset is that exact instant; without one it is wall-clock time in `--timezone`, which defaults to the sender's own zone. The post lands `status: scheduled`, `approval_status: needs_approval`, and nothing sends.
4. Show the user each post exactly as queued (`publishing posts get <post_id>`; its `web_url` previews it as LinkedIn or X will show it). Edit with `publishing posts update <post_id>`.
5. Approve per post, only the posts the user approved: `oxygen publishing posts approve <post_id> --json` (0 credits). Approval is the moment a private draft becomes a public write.
6. Read back: `publishing posts get <post_id>` shows status, attempts, the provider post id and the deep-link.

Two axes, kept apart: `--status` is where a post sits in the pipeline (`draft`, `scheduled`, `queued`, `publishing`, `published`, `failed`, `canceled`); `--approval-status` filters its review state (`draft`, `needs_approval`, `approved`, `rejected`). A freshly queued post is `scheduled` and `needs_approval` at once. To list what awaits the user, filter `oxygen publishing posts list --approval-status needs_approval --json`.

Changing an approved post's text or content, the first comment included, revokes its approval: approve it again.

## Locks and failures

- `publishing_effect_outcome_uncertain`: the channel never confirmed whether the post went out, so retry, update and reschedule are locked. Ask the user to check their profile. Only when they confirm the post is absent, pass `--confirm-not-published` to `publishing posts update` (fixing the cause in the same call) or `publishing posts retry`; if it is live, nothing is left to publish.
- `publishing_post_in_flight`: the post is publishing right now and nothing changed. Wait, then read it back with `publishing posts get`.
- A rate-limited provider defers the post to a later instant; a deferred post is not a failed one.
- `publishing posts retry` re-queues a failed post. `publishing posts cancel` then `publishing posts delete` removes the OXYGEN copy and its history while the live post stays; `posts delete --post <social_id> --approved` deletes a live LinkedIn post, an irreversible public write. `publishing posts uncancel` reopens a canceled post as an unapproved draft. In-flight posts, replies and amplification stay protected; read the returned guidance.

## Paid and standing actions

- `publishing posts draft --max-credits <n>` writes AI drafts grounded in the Knowledge Graph (paid; drafts only).
- `publishing posts review <post_id> --max-credits <n>` adds a paid AI voice and claims check; its findings never block approval.
- Team amplification, `publishing posts boost` and `publishing amplification create`, makes teammates' connected accounts react and comment in public and spends credits. It needs `--approved`, `--max-credits` and `--acknowledge-risk`; state the LinkedIn restriction risk to the account owners first (`oxygen-sequencer`, `references/linkedin.md`).

Return the post, queue and analytics deep-links for every write.

To set up regular posting in the user's voice (a few posts or a planned week), open the [founder-posting-system](plays/founder-posting-system.md) play first.
