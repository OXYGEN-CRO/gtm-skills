# A founder posting system grounded in your knowledge base

## The Play
Your agent writes LinkedIn posts from what OXYGEN already knows about your company, saves them in OXYGEN for you to read, and each one publishes on time in your name only after you approve it. Use it for one to three posts now, or plan a whole week in one sitting. Writing and saving drafts is free; publishing needs your LinkedIn account connected to OXYGEN.

## Before You Start
- What you sell and who buys it: `oxygen context profile get --json` (free). If company, offering or ideal customer is empty or the read fails, write the drafts from what the founder has told you about the company and say so; offer the `day-1-first-win` play afterwards to save those facts. Only when you know nothing about the company, ask: "What do you sell, and who buys it?"
- A LinkedIn account to publish from (drafting works without one): `oxygen senders list --status active --json` (free). Connecting one reserves 3,400 credits (about $34) every month and the balance must cover the first month, so a workspace holding only the free 1,000 credits cannot connect; `oxygen billing seats --json` shows the current charge in `seats[].after_seats_end.reservation_credits_per_month` (ignore its `can_connect`, which counts the retired dollar seats, not whether LinkedIn can be connected). Read the balance before telling the founder anything about it: `spendable_credits` in `oxygen billing balance --json`, after the long `available_plans` list (free). Connecting it also needs a paid plan, whatever the balance: on Free the connect returns `upgrade_required`, so tell the founder to subscribe and link its `upgrade_url`, never a credit top-up. If none is connected, draft anyway and tell the founder that publishing will need LinkedIn connected, on a plan, at about $34 a month in credits, and whether their balance covers it.
- Optional: the workspace's saved voice, `oxygen knowledge page get voice --json` (free); follow it when it exists. Also optional: two or three of the founder's past posts (free). Without either, write in a plain, direct founder voice and say that it is a guess.
- What is already queued: `oxygen publishing posts list --json` (free). Reuse drafts that still fit, and move any whose `publish_at` has passed: `oxygen publishing posts update <post_id> --publish-at <YYYY-MM-DD>T09:00 --timezone <tz> --json`.

## Steps
1. Pick the slots and write the drafts from the profile, or from what the founder told you (free). Default: three posts, next Tuesday, Wednesday and Thursday at 09:00 in the founder's timezone (if unknown, the company's home country; say which). Whole week: plan it with the `oxygen-linkedin-content` skill's week plan. Write every post by that skill's idea gate, hook, body and review steps (`oxygen skills get oxygen-linkedin-content`), with no @ tags and nothing the profile marks unverified. In this play its pillar and proof pages are optional: without them, keep to facts from the profile, say the voice is a guess, and offer that skill's setup for next week. If the founder shared past posts, match them and keep the voice for next time: `oxygen knowledge page upsert --slug voice --title "Voice" --status active --body "<how they write, plus the examples>" --json`.
   Tell the founder: here are next week's drafts; change anything you like, and nothing goes out until you approve it.
> APPROVAL GATE — ai-draft: only if the founder would rather have OXYGEN's AI write them: one call costs about 1.5 credits and returns up to 5 versions of one idea; cap each call at 3 credits.
2. Optional, instead of writing them yourself: OXYGEN's AI drafter (~1.5 credits per call), then queue the version the founder picks (leave out `--sender` while LinkedIn is not connected):
   ```bash
   oxygen publishing posts draft --template personal_story --topic "<one-line idea>" --channels linkedin --max-credits 3 --json
   oxygen publishing drafts accept <draft_id> --variant <n> --publish-at <YYYY-MM-DD>T09:00 --timezone <tz> --sender <sender_id> --json
   ```
   Tell the founder: OXYGEN wrote a few versions; pick the one you like.
3. Save the drafts in OXYGEN (free; nothing publishes). Write posts.json as `{"rows":[{"title":"Tue","content_text":"<post>","publish_at":"<YYYY-MM-DD>T09:00","timezone":"<tz>"}]}`, one row per post, adding `"sender_account_id":"<sender_id>"` if LinkedIn is connected. Then preview, save and list them; `--approved` here only saves, it approves nothing:
   ```bash
   oxygen publishing import --file posts.json --json
   oxygen publishing import --file posts.json --approved --json
   oxygen publishing posts list --approval-status needs_approval --json
   ```
   Tell the founder: your drafts are saved at https://oxygen-agent.com/publishing, and nothing goes out until you approve each one.
> APPROVAL GATE — linkedin-connect: only if no LinkedIn account is connected: connecting reserves 3,400 credits (about $34) every month while it stays connected, the founder logs in themselves, and you say whether their balance covers the first month; get a yes on that cost first.
4. Connect LinkedIn: the founder opens https://oxygen-agent.com/connections?filter=linkedin and logs in (or run `oxygen senders connect --country <login country, e.g. US> --json` for a 10-minute link). Then attach the account to each saved post (free):
   ```bash
   oxygen senders list --status active --json
   oxygen publishing posts update <post_id> --sender <sender_id> --json
   ```
   Tell the founder: LinkedIn is connected, and your posts will go out from your account.
> APPROVAL GATE — post-publish: for each post show the exact final text, the day, time and timezone, and the account it posts from; approve only the posts the founder said yes to, one at a time (0 credits); `oxygen publishing posts cancel <post_id> --json` stops one before it goes out.
5. Approve each post the founder said yes to; it then publishes at its time (free): `oxygen publishing posts approve <post_id> --json`.
   Tell the founder: approved; it goes out on <day> at <time> from your account.
6. Check back (free): `oxygen publishing posts get <post_id> --json` after the publish time, and `oxygen publishing analytics post <post_id> --json` two days later for reactions and comments. Next week, repeat from step 1 after the `oxygen-linkedin-content` skill's learn step.
   Tell the founder: it's live, and here is what people said.

## If It Goes Wrong
- `missing_required_option` for `--publish-at` → every post needs a publish time, even a draft; give each row a `publish_at`.
- `publishing_sender_missing` as a warning on the import preview → expected while no account is attached; add `"sender_account_id"` to each row, or save first and attach it in step 4 (`publishing import` has no `--sender` flag, whatever the warning says). On approve, `publishing_sender_unavailable` (`publishing_sender_missing`) means the same: do step 4, then approve again.
- `publishing_mentions_unresolved` or `linkedin_company_mention` on approve → an @ tag could not be verified; write the name without @, or run `oxygen publishing mentions resolve --account <sender_id> --text-file post.txt --json` and use the exact @handle it returns.
- `upgrade_required` → this workspace's plan does not include connecting or publishing; open the `upgrade_url` from the error with the founder.
- `insufficient_credits` on connect → the balance cannot cover the first month (3,400 credits); add credits or choose a plan at https://oxygen-agent.com/billing.
- The `oxygen posts create` preview says "Re-run … to publish" while no account is connected → that is wrong; nothing publishes before step 4, so use the queue above.
- `linkedin_rate_limited` → the account hit its daily limit; the error names `resets_at` and the post waits; do not retry in a loop.
- A post did not go out → `oxygen publishing posts get <post_id> --json` shows its attempts; `oxygen publishing posts retry <post_id> --json` tries a failed one again.
