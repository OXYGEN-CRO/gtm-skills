# X posts

An X post publishes through a connected X account: `publishing posts create --provider x --provider-connection <connection_id>` (find the id with `integrations list`; connect with `integrations connect`). It follows the same queue and approval as LinkedIn.

Each option has its own flag on `publishing posts create|update`:

- Thread: `--thread-post "<text>"` once per following post, in order; `--thread-media 2=<media_id>` attaches media to post 2 or later.
- Poll on the first post: `--poll-option "<text>"` two to four times (25 characters each) and `--poll-duration 2d` (5 minutes to 7 days, default 1 day). A poll post takes no media.
- Media per post: one to four images, one GIF or one video, never mixed (`publishing media upload`, then `media_asset_ids`).
- Accessibility and tags: `--alt-text <media_id>="description"` (up to 1,000 characters), `--photo-tag <username>` (up to 10).
- Replies: `--reply-settings everyone|following|mentioned|subscribers`.
- Remove one key without replacing the content: `--content-merge-json '{"poll":null}'`.

Before approval, `oxygen publishing posts get <post_id> --json` returns `publish_plan`: every post that will be sent, in order, with its media, alt text, poll and reply settings. It is free and makes no call to X.

X analytics cover only posts published through OXYGEN ([analytics](analytics.md)).
