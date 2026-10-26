# LinkedIn captures from your own accounts

These captures read what a connected account owns. They are free of credits, read-only on LinkedIn and contact nobody, and every read draws on the account's metered daily budget, so large captures land over days. Each one is a standing background job: it keeps running until paused. Account safety, read budgets and health: `oxygen-sequencer` skill, `references/linkedin.md`.

## Whole network

`oxygen linkedin network setup --json` (optional `--account <ref>`; web: New table, LinkedIn Network) fills one "LinkedIn Network" table, one row per person, with a Relationship column (connection, follower or both). It is a standing permission: accounts connected later are armed automatically, so check that every account in the response's `senders[].display_name` is the customer's. `linkedin network status` reports each account's state and pace; a capture in `backfill` for days is working as designed, and no completion date exists until the first walk ends. `linkedin network pause` stops reading and keeps the rows; setup again continues where it stopped.

`followers import` and `connections import` keep the older separate tables, each refreshing itself; `followers status` and `connections status` show progress.

## Profile viewers

`oxygen viewers import --account <ref> --json` (omit `--account` for every account; web: New table, Professional Network Profile Viewers) drips named viewers into one table per workspace. The import is a partial sample: LinkedIn hides anonymous and private-mode viewers, so name what was captured rather than promising everyone who viewed.

- `view_count` counts capture walks a viewer reappeared in, and `last_viewed_at` is approximate (LinkedIn reports "3 weeks ago"-style recency); `viewers import --help` explains both.
- `viewers status` returns `health`; read it before `last_error`. Its help lists every state and repair, for example `unbound` (armed with nowhere to land: it reads every tick and writes nothing) and `stalled` (`health_note` names the fix).
- Viewers and `linkedin intent setup` are two capture mechanisms with different table shapes and the same default table name; crossing them fails with `table_missing_columns`. Pick one per workspace. When `viewers status` says `landing_via: feed`, the intent feed already lands viewers: keep it and skip `viewers import`.
- `viewers pause --account <ref>` switches one account off and keeps the rows; `viewers import --account <ref>` switches it back on. `linkedin network pause` does not touch viewers.
- `viewers enrichment --on` is standing paid enrichment of every new viewer at the per-person price `viewers status` quotes. Switch it on only when the user asks for that spend.

## Open connection requests

`oxygen linkedin invitations setup --json` keeps one table of every pending request, received and sent, checked about twice a day; a request that disappears is marked `accepted` or `no_longer_pending`. It never accepts, declines or withdraws. To act on sent requests: `linkedin invitations list`, then `linkedin invitations withdraw --ids <ids>` previews and `--approved` withdraws. A withdrawn person cannot be invited again from that account for 21 days.

## Intent capture and auto-enroll

`oxygen linkedin intent setup --account <ref> --json` creates the linked LinkedIn Engaged People and LinkedIn Touchpoints tables and arms follower, connection and profile-viewer captures; `--post <social_id>` adds one post's engagers. Rows carry `signal` (`new_follower`, `new_connection`, ...) and `signal_at`. The first cycle records the existing network as a silent baseline, so only people new since arming become signals. These feeds cycle followers and connections daily and profile viewers weekly, while a standalone `viewers import` re-walks about every 6 hours. Watch the captures with `feeds list linkedin-engaged-people`, `feeds get <feed_id>` and `linkedin intent status`; `feeds pause` and `feeds resume` switch one off and on.

`oxygen linkedin intent autoenroll --account <ref> --sequence <ref> --json` previews, writing nothing: the sender's effective caps, the audience split (already connected, needs an invite, suppressed, owned by another sender), the spend and enroll caps and a 7-day send forecast. `--kinds` chooses captures; `own_posts` adds a rotating capture of engagers across the sender's recent posts.

> APPROVAL GATE, standing auto-enroll: `--approved` arms a standing grant. Every later cycle enrolls newly captured people under the shown caps (`--max-enrolls-per-day`, `--max-credits-per-cycle`) without asking again. Before approval, state two facts: the connections import is a metered drip, so a real network lands over days (`linkedin ingestion status`), and without `--include-existing-network` only people who connect, follow, view or engage from now on are enrolled. Reaching the existing network is the user's own explicit decision, never a flag added for them. `--disable` revokes the grant at once without approval; the captures keep filling.

Enrolled people still flow through the Sequence's own caps, suppressions and sender bindings.

## Engagers on your own posts

Get the post's composite `social_id` with `oxygen posts get --post <post-url> --account <ref> --json`, then:

- `oxygen engagement engagers --post <social_id> --json` reads reactors and commenters now as one de-duplicated list; `truncated: true` means the page cap stopped a source.
- `oxygen engagement harvest --post <social_id> --source unipile --recurring --json` drips engagers into a table and asserts each into CRM people; `engagement status` shows progress. The drip is slow by design: poll it rather than re-arming it.

## Mutual connections

For shared connections with one profile, read `oxygen tools get linkedin.users_get --json`, then run it live with the connected account id and `"notify": false`. It is non-notifying and costs no credits; `unavailable` means hidden, not zero.

## When a capture stalls

`linkedin ingestion status` shows every drip, `next_slice_at` and the remaining ingest budget: a spent budget waits until the next day. A disabled feed, or one in `error` or `exhausted`, shows its cause in `feeds get <feed_id>`; fix the account (`senders health <id>`) and `feeds resume <feed_id>`.
