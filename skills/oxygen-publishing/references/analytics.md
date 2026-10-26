# Post analytics

Every command reads stored snapshots: no provider call, 0 credits. Return the response's `web_url` (Analytics, Content).

Account followers use a daily background refresh. Freshness comes from the capture time of each stored account snapshot, not from a local sender identifier: an X account can have `sender_account_id: null` and still have a current snapshot. Use its returned `channel` and `account_key` to distinguish it.

For MCP value projections, `max_chars` budgets the serialized response, including metadata and the MCP envelope. A selected value can therefore fragment below that ceiling. If the metadata cannot fit, increase the window as the error directs; follow `next_cursor` until `complete` before reconstructing a value.

| Question | Command |
| --- | --- |
| Which posts performed, and by how much | `oxygen publishing analytics summary --channel linkedin --range 30d --sort engagements --json` (`--sort impressions` ranks by reach; `leader` states the top post's lead) |
| Is it growing | `oxygen publishing analytics timeseries --channel linkedin --range 30d --tz <zone> --json` |
| One post over time | `oxygen publishing analytics post <post_id> --json` (daily series, totals, 24h and 7d benchmarks, earned-media value) |
| Followers per account | `oxygen publishing analytics account --json` |

## Reading the numbers

- `null` means unavailable, never zero. Each null carries a reason in `null_reasons`: `not_exposed_by_provider`, `not_synced_yet` or `not_returned_by_provider`. When impressions are empty, say so rather than offering a proxy as reach.
- Read `totals`, `coverage`, `freshness` and `guidance` together: a thin coverage window is why a total looks low.
- Impressions come from LinkedIn's own post analytics, shown only to the post's author: real for the connected member's original posts and empty for anything else. Saves and sends are not exposed. Reposts stay out of performance totals (`reposts_excluded`) because their reactions and impressions belong to the original author.
- `timeseries` reports engagement earned per day across every tracked post, with each metric's direction against the previous period or, when tracking began inside the range, the second half of the tracked days against the first (`trend.basis`, `trend.compared`). `not_enough_history` means tracking began too recently (`history_starts`). When `estimated_days` equals `tracked_days`, every compared day spread a gain across an unread gap: call the change approximate.
- Totals combine every connected account. When a co-founder's account is connected too, name each post's author (`top_posts[].account`), or count only chosen accounts with `--account <key>` (repeatable; a LinkedIn sender id from `oxygen senders list` works).
- LinkedIn covers owned posts discovered from the provider; X covers only posts published through OXYGEN.
