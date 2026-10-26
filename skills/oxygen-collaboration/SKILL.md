---
name: oxygen-collaboration
description: "Get a second party's documented go/no-go inside OXYGEN: threaded internal comments on any workspace object, approval requests assigned to named members, the opt-in gate that blocks a live launch until someone approves, and the restricted client role. Not for public comments on a published post, and not a substitute for a paid action's own approval."
allowed-tools: Bash(oxygen *)
---

# OXYGEN Collaboration

**Beta.** `/collab` has no web sidebar entry, and the Beta features toggle does not add one: people open it from a notification email, by URL, or with **⌘K → Approvals**. The CLI, MCP tools, and every link below work regardless; nothing in this skill depends on it. If someone cannot find Approvals in the sidebar, that is expected, not a broken workspace: send them the `web_url` from the response.

The review conversation lives next to the work instead of in a Google Doc. Everything here is internal, free, and sends nothing externally. Two ideas, deliberately separate: a **comment thread** is a conversation ABOUT an object and resolving one approves nothing; an **approval request** is a decision someone owes, and it blocks work only where an admin armed the matching **gate**.

Address a subject as `<kind>:<id>` (`sequence:seq_123`, `table:tbl_9`); on a table, `--path` scopes a thread to one part of it — `row:<rowId>` for a row, `row:<rowId>#<columnKey>` for a cell, `column:<columnKey>` for a whole column. `oxygen comments add --help` lists the commentable kinds, `oxygen approvals gate list` shows what is armed today.

## The agency → client sign-off motion

```bash
# 1. Arm the gate once (workspace admin). Until this exists, a request is advisory.
oxygen approvals gate set --on table:tbl_9 --gate signoff --required --json

# 2. Ask the client to decide, and say what you are asking for.
oxygen approvals request --on table:tbl_9 --gate signoff \
  --assignee client@acme.com --title "Q3 target list" \
  --body "142 rows, ICP filter in column J." --expires-hours 72 --json

# 3. The client (their own login) sees only what they owe.
oxygen approvals inbox --json
oxygen comments add --on table:tbl_9 --path row:row_18 "Wrong segment — drop this one." --json
oxygen approvals decide req_8f2c --changes-requested --note "Fix row 18, then resend." --json

# 4. You revise, then ask again. Approval is what opens the gate.
oxygen approvals decide req_9a01 --approve --json
```

`launch` gates a sequence; `signoff` gates a table. Once a gate is required and unapproved, that primitive's LIVE path refuses with `approval_required` and names the pending request — previews and dry runs stay open, so the client can always inspect what they are being asked to approve.

## Rules that decide outcomes

- **`--changes-requested` is a real decision and it does NOT open the gate.** Never report it as "approved with notes"; read `opens_gate` rather than inferring from status.
- **The requester cannot decide their own request** — and cannot assign it to themselves in the first place (a list containing your own address is refused whole, not quietly narrowed). Withdraw it with `oxygen approvals cancel <requestId>`; assignees (or a workspace admin who did not file it) decide. In a one-member workspace an armed gate therefore cannot be satisfied: invite the person who should sign off, or have an admin run `oxygen approvals gate set --on <kind>:<id> --gate <gate> --not-required`.
- **Gate policy is admin-only**, per object or as a workspace default per subject kind. A member who can switch the gate off is not a gate.
- **Assignees are emails of existing members, other than you.** A non-member — or your own address — is a named error, not a silent drop.
- **Expiry decides nothing, and it never expires a yes.** `--expires-hours` is a deadline on the ANSWER: an undecided request lapses to `expired`, which still blocks — cancel it and ask again. An approval given before the deadline is not time-limited; the gate stays open until the approved content changes (`approval_stale`) or an admin re-arms it. If a client should re-confirm on a schedule, ask for a new request; there is no expiring approval.
- **An approval covers the campaign as it was.** Change the journey, the email copy (subjects and bodies), channels, senders, the email track's connected account, the sending schedule, the send caps, the dispatch mode, or the cold-WhatsApp / reply-stop rules after a `launch` approval and the live path refuses with `approval_stale` — ask again instead of assuming the yes still holds. Renaming, re-tagging, and everything the sending itself moves (credits, sends, enrollments) leave the approval intact.

## Handing a client a login

`oxygen approvals client grant <email>` restricts an existing member to reading the workspace, commenting, and deciding what is assigned to them. `revoke` returns them to normal. It cannot restrict you, and it cannot restrict a workspace admin.

`oxygen approvals client list` returns the same grant and clear that the workspace's `/collab/members` page offers, plus, per member, `can_restrict` and `restrict_blocked_reason` — whether a grant on that person would be refused and why, before you attempt it. Clearing is never blocked: that is how an admin removes an overlay from someone who has since become a workspace admin.

**Granting on an invitation.** `grant` accepts an address that has been INVITED but has not joined: it records the role against the invitation, and the person lands restricted the moment they accept. `approvals client list` shows those under `pending_invitations` with `oxygen_role_on_join`. Nothing changes for them until they join — read `pending_invitation: true` in the response and do not report the client as restricted yet. An address with no membership and no invitation is still refused, with the invite link in the error.

**Demoting an admin so the role can be granted.** `oxygen orgs member-role <email> --role admin|member` moves somebody between the two workspace roles. This is the only Clerk membership change Oxygen makes, and it exists for one reason: a workspace admin's role overrides the client restriction, so `approvals client grant` is refused until they are a plain member. On a workspace where everybody is an admin, run `orgs member-role … --role member` first. You cannot change your own role, Oxygen will not touch a role it does not assign (`owner`, Clerk custom roles), and Clerk refuses to leave a workspace with no admin.

**Inviting is Clerk's.** Oxygen sends no invitation email. Point the user at workspace settings (`/settings`) or the "Add member" button on `/collab/members`; do not claim a CLI command can invite somebody.

Return the `web_url` from every response so the other person can open it. Given only an id: `oxygen comments show` / `oxygen approvals show`.
