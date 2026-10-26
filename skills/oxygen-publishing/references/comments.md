# Public comments on owned posts

Comments on the workspace's owned LinkedIn posts published within the last 30 days collect in a durable work queue. Older published posts linked to creator programs retain the polling exception; this is not full lifetime history.

## Read the queue

```bash
oxygen publishing comments list --view all --limit 1 --json
oxygen publishing comments list --json
oxygen publishing comments get <comment_id> --json
```

- For compact counts, scope and refresh status, use `--limit 1`: this limits comment rows, while those metadata fields accompany every page. Read the freshness warnings before treating stored counts as current.
- The default view is `unanswered` (`needs_reply`, `draft`, `awaiting_approval`, `action_unavailable`); `--view all` covers every state on recent owned posts. A view and an exact `--status` do not combine.
- Before trusting an empty queue, read `empty_queue_is_current`, the freshness fields, `next_sync_at` and any errors. Replies made on LinkedIn directly reconcile on the next sync.
- Poll timestamps cover posts and account discovery together. The latest start or completion can belong to a different target from the earliest due time or latest recorded error. A new successful discovery poll therefore does not make a delayed comment queue current. Comment-row `last_seen_at` and `synced_at` record when that row was observed, rather than every workspace poll.
- These reads cost nothing and call no provider. Live reads (`posts comments`, `posts reactions`) draw on the account's read budget and do not fill this queue.

## Reply in public

```bash
oxygen publishing comments reply <comment_id> --text "<exact reply>" --json
oxygen publishing comments approve <action_id> --content-hash <sha256> --approved --json
```

`reply` is a preview: it calls no provider, posts nothing and returns `approval.action_id` and `approval.content_hash`. Show the account, the comment it answers and the exact text. `approve` is the only public write, bound to that action and hash, and runs after the user approves that text. When the result is `effect_unknown`, open the returned comment link and check the public thread; a new reply is a new preview.

`publishing comments update` (local draft, notes, assignee, triage status) and `publishing comments resolve` (resolved, ignored, spam, reopen) change local work state only and say nothing in public.

## Related moves

- A private message to a commenter: a new conversation is a Sequence, an existing one is Messages.
- Collecting everyone who engaged with a post into a table: `engagement harvest` (`oxygen-signals` skill).
- Answering many comments can reach the account's comment cap. Raising it follows the caution rule in the `oxygen-sequencer` skill (`references/linkedin.md`).
