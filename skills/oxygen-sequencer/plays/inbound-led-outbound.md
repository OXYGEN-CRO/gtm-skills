# Inbound-led outbound: post engagers into a capped warm sequence

## The Play
You find the people already paying attention on LinkedIn (reacting to or commenting on posts, following or connected to you, or viewing your profile), score each one against your ideal customer (ICP: the kind of person and company that buys from you), and send a short LinkedIn message only to the good fits. Use it when you want warm conversations this week instead of a bought list. A first sample from posts costs about 150 credits and contacts nobody; reading your own followers, connections or viewers, and sending any message, needs your LinkedIn account connected, which reserves 3,400 credits a month.

## Before You Start
- **Your ICP in one line.** `oxygen context profile get --json` (free) shows company, offer, ICP and competitors. If the ICP is empty, ask "Who buys from you: what role, at what kind of company?" and use the answer in step 5.
- **About 150 credits.** `oxygen billing balance --json` (free; read `spendable_credits`, what is left after connected accounts' monthly reservations; it comes after the list of plans). The pilot costs about 150 credits once; keeping the daily capture on costs up to 150 a day. If short, tell the founder: "This needs about 150 credits; you can add credits at https://oxygen-agent.com/billing."
- **A connected LinkedIn account**, for followers, connections, viewers and sending (post capture works without one). `oxygen senders list --status active --json` (free). Connecting reserves 3,400 credits ($34) a month and the balance must cover the first month, so a workspace holding only the free plan's 250 credits cannot; read `spendable_credits` in `oxygen billing balance --json` (free) before telling the founder whether theirs covers it; `oxygen billing seats --json` shows this workspace's charge in `seats[].after_seats_end.reservation_credits_per_month` (its `seats_retired` status and `can_connect: false` describe the retired dollar seats, not whether this workspace can connect). If none, tell the founder: "Capturing and scoring work now; sending needs your LinkedIn connected, which reserves 3,400 credits a month."
- **What already exists.** The `kit` block of `oxygen recipes show inbound-led-outbound --json` (free). A stage `reused` means a capture is installed and `skipped_active` that it already runs daily: `oxygen workflows get template-linkedin-profile-engager-monitor --json` shows whose posts it watches. Resume from it, and disable a running one before changing its source.

## Steps
1. Ask one question (free): "Whose LinkedIn attention should we turn into conversations?" If unsure, use their own posts when they post weekly, otherwise a competitor founder, and state the assumption.
   - Your posts → your /in/ profile URL: with LinkedIn connected it is `identity.profile_url` in `oxygen senders list --status active --json`; otherwise ask for it.
   - A competitor founder's posts → their /in/ URL. Propose one from the profile's competitors: `oxygen people search preview --filters-json '{"people":{"job_title":{"include":["Founder","CEO"]}},"company":{"linkedin_url":["https://www.linkedin.com/company/<competitor>"]}}' --json` (no `rows` means the company URL is wrong; judge by the rows, because `people_by_company` shows 0 when LinkedIn returns the company under another URL).
   - A creator in your niche → their /in/ URL, from the authors in `oxygen signals search preview --keywords "<topic>" --last-days 30 --sort top --json`, or ask whom they read.
   - A topic → one short buying topic from the ICP, for example "outbound".
   - Posts you paste → each post author's /in/ URL. The capture reads the author's newest posts, so an older post can be missed; one-post capture does not exist yet.
   - Your followers and connections, or your profile viewers → your connected LinkedIn account (step 2).
   Tell the founder: "We'll start with <source>. The first sample costs about <150> credits (0 for your own network) and contacts nobody."
> APPROVAL GATE — connect-linkedin: connecting <name>'s LinkedIn reserves 3,400 credits ($34) a month while it stays connected (`oxygen billing seats --json` shows the exact charge); invites and messages cost 0 on top. Needed now only for followers, connections or viewers; post and topic sources come back here before step 7.
2. Connect LinkedIn: `oxygen senders connect --country <ISO2> --established --json` returns a login link valid for 10 minutes (`<ISO2>` is where the founder usually logs in, such as US or DE; drop `--established` for a new account). Then `oxygen senders list --status active --json` gives `<sender_id>`.
   Tell the founder: "Open this link and log in to LinkedIn. It stays connected until you disconnect it."
3. Install the capture (free: creates tables and a switched-off workflow, calls nothing).
   - Profile sources: `oxygen recipes apply inbound-led-outbound --input-json '{"linkedin-profile-engager-monitor":{"profiles":["<url>"],"max_credits":150}}' --json`. The monitor stage's `pricing_forecast.total_credits` is the quote (about 142 for 2 posts and 20 people). Workflow: `template-linkedin-profile-engager-monitor`.
   - Topic: `oxygen blueprints apply linkedin-keyword-engager-monitor --input-json '{"keywords":["<topic>"],"max_credits":150}' --json`. It returns no quote; expect up to about 50 credits a post, 2 posts. Workflow: `template-linkedin-keyword-engager-monitor`.
   - Followers, connections and viewers need no install.
   Tell the founder: "It's set up and switched off. The next step is the paid sample: about <quote> credits."
> APPROVAL GATE — capture-sample: posts or topic: one live run of <workflow> on <source>, hard cap 150 credits (quote from step 3). Enabling also arms a daily 07:00 UTC run, so it is switched off as soon as this run ends. Followers, connections, viewers: free reads of the founder's own account that keep refreshing until paused (network capture also covers LinkedIn accounts connected later); nothing is sent.
4. Capture one sample. Posts or topic (there is no run-once yet):
   ```bash
   oxygen workflows enable <workflow> --approved --max-credits 150 --reason "one pilot capture" --json
   oxygen workflows call <workflow> --mode live --approved --max-credits 150 --json
   oxygen workflows tail <run_id> --json
   oxygen workflows disable <workflow> --reason "pilot done" --json
   ```
   Followers and connections: `oxygen linkedin network setup --account <sender_id> --json` (pace: `oxygen linkedin network status --json`; stop: `oxygen linkedin network pause --account <sender_id> --json`). Viewers: `oxygen viewers import --account <sender_id> --json` (table link: `oxygen viewers status --account <sender_id> --json`; stop: `oxygen viewers pause --account <sender_id> --json`).
   Tell the founder: "Captured <n> people from <source>, and the schedule is off again." For network or viewers: "People arrive over hours to days."
5. Read the people and price the score (free). `<table>` is the people table the install or status named (`linkedin-engaged-people` for profiles, `linkedin-topic-engaged-people` for a topic); `<url_col>` is `linkedin_url` there and `profile_url` for network and viewers.
   ```bash
   oxygen tables query <table> --fields full_name,headline,<url_col> --limit 25 --json
   oxygen columns add <table> --label "ICP fit" --key icp_fit --score 'low,medium,high' --prompt 'We sell to <ICP line>. Is {{full_name}} ({{headline}}) a likely buyer or champion?' --grounding workspace --json
   oxygen columns run <table> icp_fit --limit 100 --dry-run --json
   ```
   Tell the founder: "<n> people so far; scoring them costs about <dry-run estimate> credits (about 0.075 each)."
> APPROVAL GATE — score-fit: score up to 100 people at the dry-run estimate, hard cap 10 credits.
6. Score them and list the good fits (up to 10 credits, then free reads):
   ```bash
   oxygen columns run <table> icp_fit --limit 100 --approved --max-credits 10 --json
   oxygen table-runs wait <run_id> --json
   oxygen tables query <table> --filter-tree-json '{"type":"group","conjunction":"and","children":[{"type":"leaf","columnKey":"icp_fit","path":"level","operator":"is","value":"high"}]}' --fields full_name,headline,<url_col> --json
   ```
   Tell the founder who scored high (none? show the medium ones) and why, in your words from their headline; the cell's `reason` only states the level and confidence.
7. Draft and preview the message (free; nothing sends). Write `steps.json` with the founder: open with the topic you share, and never say you saw them react, comment, follow or view.
   ```json
   {"steps":[{"id":"check","kind":"branch","condition":"already_connected","then_id":"hello","else_id":"invite"},
     {"id":"invite","kind":"invite"},{"id":"accepted","kind":"wait_for_connection","timeout_days":7},
     {"id":"hello","kind":"message","template":"Hi {{first_name|there}}, <one true line about the topic you share>. <one small question>"},
     {"id":"pause","kind":"wait","days":3},{"id":"nudge","kind":"message","template":"<one short follow-up>"}]}
   ```
   `oxygen sequences create --name "Inbound-led outbound" --slug inbound-led-outbound --steps-file steps.json --table <table> --url-column <url_col> --max-new-enrollments-per-day 10 --exclude-contacted --json`. From here LinkedIn must be connected (step 2). There is no filtered enroll yet, so write the high rows to `leads.json` as `{"leads":[{"table_row_id":"<_row_id>","lead_name":"<full_name>"}]}`, then run `oxygen sequences update inbound-led-outbound --senders <sender_id> --json`, `oxygen sequences enroll inbound-led-outbound --leads-file leads.json --exclude-contacted --json` and the free launch preview `oxygen sequences start inbound-led-outbound --json`.
   Tell the founder: "Here are the exact messages for <n> people. Nothing has been sent."
> APPROVAL GATE — send-messages: real LinkedIn invites and messages from <account> to exactly the <n> previewed people, at most 10 new people a day and 30 actions in total, 0 credits each. The first live start also turns on the free update of the CRM from replies. A sent message cannot be taken back.
8. Send: `oxygen sequences start inbound-led-outbound --approved --max-live-sends 30 --json`. Read replies with `oxygen inbox list --channel linkedin --unanswered --json`.
   Tell the founder: "It's live. Replies come to your LinkedIn and the OXYGEN inbox; answer them yourself."
> APPROVAL GATE — keep-capturing: switch the post or topic capture back on daily at 07:00 UTC, up to 150 credits a day (up to about 4,500 a month) until switched off; scoring new people costs about 0.075 each. The sequence is live, so each week's new good fits are enrolled only after the founder approves that list.
9. Optional, keep it going: `oxygen workflows enable <workflow> --approved --max-credits 150 --reason "daily engager capture" --json` (stop: `oxygen workflows disable <workflow> --json`). Each week re-run step 6, which scores only the new rows, and enroll the approved new good fits as in step 7.
   Tell the founder: "It now runs daily. I'll bring you the new good fits each week."

## If It Goes Wrong
- `invalid_blueprint_input` "profiles must include at least one LinkedIn profile URL" → `--input-json` is missing; a bare `recipes apply --dry-run` always stops here. Pass the URL as in step 3.
- `workflow_disabled` on the live call → enable first (step 4). `workflow_live_preview_not_graph` from `--preview` → this monitor has no preview; use the step 3 quote.
- `provider_response_error` "The LinkedIn lookup timed out upstream" (post search; 6 of 6 timed out in the audit) → do not retry in a loop; ask the founder for a profile URL or try later. The topic capture uses the same search on every run.
- `workflows enable` fails with a server error (4 of 50 enables in production) or the live run fails (18 of 22 live runs of this monitor failed in production in 30 days; cause not recorded) → read the error (a run's: `oxygen workflows tail <run_id> --json`), retry once at most, disable the workflow and give the founder the link.
- A green run with 0 people → the profile has no post in the last 7 days; re-run step 3 with `"lookback_days":30` added and step 4 under a new approval, or pick a profile that posts weekly.
- `insufficient_credits`, `upgrade_required` or `sending_seat_required` on connect → the plan or balance cannot carry the 3,400-credit monthly charge; the founder upgrades or adds credits at https://oxygen-agent.com/billing.
- `sequence_no_senders` → attach the sender (step 7) before enrolling or starting. `inbound-led-outbound` already exists → read it with `oxygen sequences get inbound-led-outbound --json`; reuse it only if its copy fits these people, else pick another slug.
- Fewer sends than the caps → a new account warms up over about two weeks (a few invites a day at first); that is the ramp, not a fault.
- `viewers status` shows `landing_via: feed` → viewers already land through an older capture; use that table and skip the import. Few viewers → LinkedIn hides private viewers; the table is a partial sample.
