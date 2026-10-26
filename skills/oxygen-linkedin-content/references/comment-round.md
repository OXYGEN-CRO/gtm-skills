# Comment round

Comments under other creators' posts put the author's name and headline in front of that creator's audience. This round finds fresh posts, drafts comments, and hands them over. Replies on the author's own posts are a different job: `oxygen-publishing`, `references/comments.md`.

## The hard rule: the author posts, OXYGEN never does

Nothing in this round comments, likes, follows, connects or messages on LinkedIn: not through the connected sender, a Workflow, a Sequence, team amplification or any tool, and not when the user says "just do it". The account is the asset. Return the drafts and the post links; the author pastes each comment themselves.

Reads use the managed scraper, never the connected account, so the author's own limits stay untouched. Relay the scraper disclosure from the `oxygen-sequencer` skill (`references/linkedin.md`) before the first paid read.

## Find the posts

1. The watchlist: the creators the author comments on, names, or meets in their lanes, each marked big or peer by the author. Ask for real profile URLs; never invent a list.
2. Fresh posts, free: `oxygen signals search preview --keywords "<lane term>" --posted-by <profile-url> --last-days 1 --json`, or across the lanes without `--posted-by`. Every keyword is one search on shared capacity; `rate_limit_exceeded` means wait for its retry time. Search rules: the `oxygen-signals` skill.
3. Before reading a thread, quote it: `oxygen tools run scraper.linkedin_post_comments --input-json '{"post":"<post-url>"}' --mode dry-run --json`, then run it live with `--mode live --approved --max-credits <quoted>` only after the user approves that spend. Never repeat a point the thread already made.

## Pick 10 to 12

Keep a post only when the author has a real receipt, stance or question for it, in their lanes. Skip sponsored posts, comment-gated giveaways, job and milestone posts, product pitches, politics, tragedy and anything they would have to fake. Mix 3 to 5 posts from accounts the author marks as big on the watchlist (the preview returns no follower count), under 2 hours old, with peers in their lane. Freshness first: posts under 3 hours, never over 6 unless the post mentions the author. When the window is thin, hand over fewer and say so.

## Draft

- Read the post as the author: what caught them, what would they say in person? Never open with a summary of the post.
- One move per comment, and vary it: opinion, answer, next step, tool used, real question, warm disagreement, agree plus an angle, own story, joke, a win for a peer.
- A personal story only where it is the direct parallel: 2 to 4 comments in 10. Private history (DMs, calls, deals) never appears in public.
- Shape until the author's own comments say otherwise: mostly one line of 6 to 30 words; at most 70 words and 450 characters; questions in at most 4 of 10.
- Every fact comes from the post or Knowledge, every number from the `proof` page. No invented details, feelings, clients or plans; no claim that the product has something not live.

## What reads like a bot

- One shape for every comment, or the same 3 to 5 receipts on repeat.
- Grading the post instead of talking to its author.
- Post voice in a comment: tidy two- or three-paragraph mini posts.
- No personal moment at all, or the whole bio.

Never open with "Great post", "Love this", "So true", "100%", "Spot on", "Well said", "Thanks for sharing" or "This resonates". Run the slop scrub ([body and slop](body-and-slop.md)) plus: no links, "DM me", "let's connect" or pitches. The company by name in at most 1 comment in 10.

## Hand over

Freshest post first: the post link, its author and age, the draft, the move used and any story's source. Name the 2 or 3 to do first because they age fastest. Afterwards, ask what the author actually posted and file the differences on `content-anti-patterns`; their edits are the voice signal.
