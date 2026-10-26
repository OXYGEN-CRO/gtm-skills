---
name: oxygen-signals
description: "Capture and read OXYGEN Signals: your LinkedIn network, followers, viewers, invitations and post engagers; hiring, funding, tech and news signal searches; public profile watchers and keyword post search; competitor ads; standing auto-enroll into a Sequence."
allowed-tools: Bash(oxygen *)
---

# OXYGEN Signals

A signal records that something happened: a website visit, a profile view, a reaction, a new follower, a funding round, a post about a topic. Capturing it contacts nobody. Acting on it is a Sequence (`oxygen-sequencer`) or a Workflow.

## Read the stream

- `oxygen signals list --since 30 --json`: raw events, each resolved onto the person it attached to.
- `oxygen signals leads-today --json`: people to contact today, ranked by their strongest signal in the last 7 days (`--within-days` up to 30; website visit, then profile view, post reaction, new follower; most recent first within a type), with customers, disqualified and unsubscribed people left out and do-not-contact filtered. Read-only and free; start here before ranking CRM records by hand.
- `oxygen signals registry --json`: signal types with intent weight and capture status; tag a type with `tags attach signal_type <type>`.
- `signals record` logs one inbound signal from your own system's webhook: free, idempotent on `--external-event-id`.
- An event the user tells you about (she viewed our pricing page twice): find the person (`oxygen crm search`), create the record if missing (`oxygen crm assert people --identity email=<email> --live`, free), then `oxygen crm activity log people <rowId or email> --type website_visit --direction inbound --summary "<page, count>" --occurred-at <iso> --live`. It shows in `signals list` and on the record; a note or a table row is not a signal. Give the record's `web_url`.

## Sources

| Goal | Start with | Cost | Reference |
| --- | --- | --- | --- |
| Your network, followers, connections, profile viewers, open connection requests | `linkedin network setup`, `viewers import`, `linkedin invitations setup` | Free; metered on the account | [LinkedIn captures](references/linkedin.md) |
| People engaging with your own posts | `engagement engagers`, `engagement harvest --source unipile` | Free; metered | [LinkedIn captures](references/linkedin.md) |
| Captured people enrolled into a Sequence without asking each time | `linkedin intent autoenroll` | Standing grant | [LinkedIn captures](references/linkedin.md) |
| Companies hiring, adopting a technology, raising, acquiring, in the news | `signals search plan --family <family>` | Paid per page | [signal searches](references/signal-feeds.md) |
| Daily engagers of chosen public profiles | `tables watcher preview` | Paid per cycle | [public research](references/public-research.md) |
| Public posts about a topic | `signals search preview --family linkedin_posts` | Free preview | [public research](references/public-research.md) |
| A company page's followers | `tables followers check` | Paid order | [public research](references/public-research.md) |
| Public profiles, companies and posts in table columns | `scraper.*` tool columns | Paid per row | [public research](references/public-research.md) |
| A competitor's ads and paid keywords | `adyntel.*` tool columns, `ads searches save` | Paid per call | [Ads](provider-runbooks/adyntel.md) |
| A qualified audience turned into a campaign | the audience Recipe, then the guide | Varies | [audience campaigns](references/audience-campaigns.md) |

Signal providers: [PredictLeads](provider-runbooks/predictleads.md) (funding, news, technology), [BuiltWith](provider-runbooks/builtwith.md) (technographics), [SignalBase](provider-runbooks/signalbase.md) (own key only), [WhiteWhale](provider-runbooks/whitewhale.md) (custom buying signals and account scores; own key only). Load one after `oxygen tools get <tool_id> --json`.

## Outbound plays on LinkedIn signals

Qualify first ([company and person fit](references/qualification.md)), then open the play for the audience before drafting a Sequence: [post engagers](plays/post-engagers.md), [profile viewers and followers](plays/profile-viewers-and-followers.md), [new connections](plays/new-connections.md), [existing network](plays/existing-network.md).

## Rules for every source

1. Choose the surface by whose data it is: your own data through the connected account (free, metered), anyone else's data cookieless with credits. Disclosure, read budgets and account health: [LinkedIn account safety](../oxygen-sequencer/references/linkedin.md).
2. Capture is read-only. Reaching people is a separate approval: enroll into a Sequence, then its launch ladder.
3. Every paid read previews first and runs with `--approved` and a `--max-credits` ceiling read from that preview.
4. Standing grants need explicit approval and their own ceiling: auto-enroll, standing viewer enrichment, a watcher, a bound feed, a follower order. Before approval, state the recurring spend and who could be contacted; raising a ceiling or changing a cadence asks again.
5. Monitoring runs hosted, as captures, feeds, watchers or Workflows, so every run stays inspectable; a local cron or script loop is not a monitor.
6. Coverage is partial by design: anonymous viewers stay hidden, page caps cut long threads, drips land over days, and a match count is quoted only when a provider published it. Report what landed and what remains, never "everyone".
7. Return the table, feed, watcher and Sequence deep-links.

Plays: [daily-warm-lead-queue](plays/daily-warm-lead-queue.md), [post-engagers](plays/post-engagers.md), [profile-viewers-and-followers](plays/profile-viewers-and-followers.md), [new-connections](plays/new-connections.md), [existing-network](plays/existing-network.md).
