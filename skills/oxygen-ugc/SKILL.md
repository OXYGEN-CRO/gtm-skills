---
name: oxygen-ugc
description: Operate UGC programs, independent creators, voice, posts, approvals, sponsorship and bounded amplification in OXYGEN.
---

# OXYGEN UGC

Verify host, user and workspace with `oxygen whoami --json`; discover `oxygen ugc --help`. Read [operations.md](operations.md) before changing posts, leaving a program, sponsoring or engaging. JSON reads return `web_url`; use it for inspection links. MCP uses the `ugc` pack.

Setup is lean: create a program from its product link (name and icon come from the site), write a brief, set posts per week, per month or in total, and invite several creators with `--emails`; one creator can have their own deal (`creators invite --posting-target`, later `creators set-target`). A brand can make a program public; creators find public programs with `ugc programs discover` and apply with `ugc programs apply`, using the LinkedIn URL on their profile. A public program can let creators join automatically (`--join-policy automatic`): share its `join_url` from `ugc programs get`, and `ugc programs apply` then joins at once (`joined: true`).

Creators keep independent workspaces. Sponsorship is optional: paid by card, each host pays a seat and its own credit grant; paid by credits, a creator costs one LinkedIn account reservation however many hosts sponsor it. A brand paying by credits can sponsor creators as it invites them (`creators invite --sponsor`): the preview shows the monthly reservation (one connected LinkedIn account, 3,400 credits at current prices), approving the invitation approves it, and nothing is reserved until a creator accepts and connects LinkedIn. Creators approve their own posts; brands cannot require approval. Delegation is the creator's choice: it lets the organizer edit, schedule and approve enrolled posts, never spend the creator's wallet. Keep approval and spend gates separate.

Invitation email needs communication authorization and its preview token; provider acceptance is not delivery. `--link-only` sends no email. A placeholder address (example.com, `.test`, `.invalid`) is refused on every path, `--link-only` included; ask for the creator's real address. Pilot preparation authorizes no email, sponsorship, paid generation or live engagement.

Accepting uses the LinkedIn URL on the creator's profile. Voice is private; save real preferences/examples for free. Follow [operations.md](operations.md) for import preview, matching connection, paid execution and resumable progress.

Ground posts in real experience. Preview paid work; obtain exact approval and a credit ceiling. Reuse the draft `request_id` for approval and status; uncertainty requires reading that ID before starting another paid request.

Read `ugc memberships list` in the creator workspace; choose Personal or one Program before first save. `--ugc-participation-id` saves an unapproved draft; enrollment never publishes. Before publication starts, creators can remove the active `enrollment_id`, retaining the personal draft and immutable history. Bind edits, approvals and history reads to current `enrollment_version`; re-enrollment needs fresh approvals. Follow every history, calendar and analytics cursor.

UGC engagement excludes the author. For your own post, start with `oxygen engagement --help`; preview and approve public actions.

Read creator allowance/access separately from host billing; preview cancellation. Amplification starts disabled. Hosts use their own accounts, voice and wallet. The peer switch permits engagement; each creator must authorize their own sender, actions, caps, active voice and wallet. Joining, sponsorship and delegation grant no engagement consent. Read policy and paginated receipts. Reconcile `effect_unknown` only from observed provider evidence; reconciliation never calls the provider, retries or expands approval.
