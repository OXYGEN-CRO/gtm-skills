# LinkedIn posts

## Limits and the sender

Posting to an account's own feed counts against that sender's `posts_per_day` (all callers together) and nothing else: it is outside the working hours, the action spacing and the daily action total that govern outreach, because a member posting to their own feed is ordinary use. A post over the cap is deferred, not failed. The sender must be `active`; account safety for every other LinkedIn action is in the `oxygen-sequencer` skill (`references/linkedin.md`).

Post from a personal profile. Company-page posting (`posts create --as-organization`) is advanced and fragile through the provider.

## The post id for live reads

`oxygen posts get --post <post-url-or-activity-id> --account <sender> --json` returns the composite `social_id`. Live reads take that id, not the activity URN: `posts comments`, `posts reactions`, `posts delete` and an own-post `engagement harvest --source unipile`. Live reads cost 0 credits but draw on the account's metered read budget and do not fill the comment queue ([comments](comments.md)).

## Mentions

- Tag a person with `@<public-identifier>` and a company page with `@<handle>` from its `linkedin.com/company/<handle>` URL, directly in the post text. A display name alone does not tag, and a `content.mentions` array is rejected.
- Approval checks each tag's identity and literal handle; a company also needs a numeric page ID. Follow `next_step` on `publishing_mentions_unresolved` or `linkedin_company_mention`: use the verified public handle, choose the identity again, or write the name without `@`.
- For a tag correction without provider reads, use only the preview's existing verified `publicIdentifier`. Use `oxygen publishing posts update` to match the text, `raw`, `identifier`, `start`, and `end` to that handle, preserving `publicIdentifier`, `providerId` and any `verifiedIdentifier`. To tag a different company handle, choose or resolve it again and use the newly returned identity. Company aliases are bound to the exact input in `verifiedIdentifier`; changing text does not verify another page.
- Text-only edits keep the old previews. `--content-merge-json` replaces arrays whole, so carry every preview you want to keep. Read the post back and leave it unapproved until the user approves scheduling.
- Current resolved previews with handle mismatches are refused before verification reads. Approval can reuse current person previews and explicit matching numeric company tags. Company handles and aliases are rechecked through the selected sender and the server identity cache; a free provider read may be needed even with stored previews. Client preview fields cannot authorize a company page ID.
- Check before approval: `oxygen publishing mentions resolve --account <sender_id> --text-file post.txt --json` resolves through the sender, free and without notifying anyone; it also takes explicit profile or company URLs, provider ids and URNs with `--identifier`, and never rewrites or publishes the text. `--source scraper` resolves without a sender but is paid (`--approved --max-credits`).

## First comment

`--first-comment "..."` on `publishing posts create|update` posts a comment right after the post, the usual home for a link. `--clear-first-comment` removes it; both keep the rest of the content.

## Media and video cover

```bash
oxygen publishing media upload ./hero.png --json
oxygen publishing posts update <post_id> --content-merge-json '{"media_asset_ids":["<media_id>"]}' --json
```

- `content.media_asset_ids` is the contract that attaches media; a media record's `scheduled_post_id` is provenance only.
- `--content-json` replaces the whole structured content, so carry `first_comment`, `external_link` and other keys along, or change single keys with `--content-merge-json`.
- Raw LinkedIn `content.attachments` take only `[{"content":"<base64>","content_type":"image/png","filename":"image.png"}]`, never media ids or URLs.
- A video post can carry a cover image: `--video-thumbnail-file cover.jpg` or `--video-thumbnail <media_id>` (JPEG or PNG), `--clear-video-thumbnail` to remove it; `publishing posts get` returns it as `video_thumbnail`. In the web editor, Cover picks a frame and Preview shows the post as LinkedIn will.

## Direct publish

`posts create` publishes at once after `--approved`, with `--external-link`, `--attachments-json`, `--repost` or `--include-job-posting`. It skips the queue's retries and attempt history, so prefer the queue for anything scheduled or more than one post.
