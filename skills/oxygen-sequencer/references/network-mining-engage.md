# Engage focus leads when they post (Network Mining, dev)

Network Mining workspaces only. When a focus lead (`crm focus`, the top 25 by default) publishes a LinkedIn post that OXYGEN captures on their People record (`post_published`), the Engage Workflow enrolls them into an Engage Sequence: like the post, comment on it in the sender's voice, and send a DM only if you are already connected. Everyone else is skipped with a reason (`not_in_focus`, `no_person_record`, `no_linkedin_profile`).

Nothing here bypasses a Sequence's limits: the sender's daily caps (comments 5/day, likes 20/day), half volume on weekends, the health pause, pacing, suppression and reply-stop all apply. AI comments and DMs are drafted at send time (paid) and each draft must pass the automatic check, or the step is skipped.

1. Create the Sequence from this journey, with the People table as its source (`crm describe people` shows its table id), one staff sender and caps: `oxygen sequences create --name "Engage focus leads" --slug engage-focus --steps-file engage.json --table <people-table-id> --senders <sender-id> --json`, then `oxygen sequences update engage-focus --max-credits <n> --max-new-enrollments-per-day <n> --json`.

```json
{
  "steps": [
    {
      "id": "like",
      "channel": "linkedin",
      "kind": "like_post",
      "reaction": "like",
      "post_recency_days": 7,
      "on_no_post": "stop"
    },
    {
      "id": "pause",
      "kind": "wait",
      "hours": 4
    },
    {
      "id": "comment",
      "channel": "linkedin",
      "kind": "comment_post",
      "post_recency_days": 7,
      "on_no_post": "stop",
      "ai_prompt": "Leave a short, specific comment on this post that adds a real thought from your own work. No pitch, no question about buying."
    },
    {
      "id": "connected",
      "kind": "branch",
      "condition": "already_connected",
      "then_id": "dm",
      "else_id": "end"
    },
    {
      "id": "dm",
      "channel": "linkedin",
      "kind": "message",
      "ai_prompt": "Follow up on their post and your comment with one line that opens a conversation about the topic. No pitch, no link."
    },
    {
      "id": "end",
      "kind": "stop"
    }
  ]
}
```

2. Review a pilot and launch it yourself: enroll at least 10 focus leads from the People table, `oxygen sequences standing-approval engage-focus --draft-samples --max-credits <n> --json` (paid: drafts each comment and DM), review every draft, approve the batch, then start it in person (`sequences start engage-focus --approved`). The first launch always needs a person.
3. Grant standing approval on that pilot (`--approve-standing <preview_hash>`). The Workflow enrolls as an Agent, so without a covering standing approval every enrollment is refused (`sequence_standing_approval_required`, or `_scope_changed` after any edit to the journey, voice, sender, schedule or caps).
4. Apply the Workflow with your Sequence's slug in place of `<engage-sequence-slug>` (`oxygen workflows lint`, then `oxygen workflows apply`). It ships disabled; enable it once the dry run looks right.

```json
{
  "manifest_version": 2,
  "workflow": {
    "id": "network-mining-engage",
    "name": "Engage focus leads when they post",
    "status": "disabled"
  },
  "specification": "When a focus lead's LinkedIn post is captured, enroll them into the approved Engage Sequence: like, comment in the sender's voice, DM only if connected. Focus leads only; the Sequence's standing approval, caps and suppression decide everything after.",
  "trigger": {
    "type": "event",
    "source": "crm",
    "event": "activity_created",
    "filters": [
      {
        "path": "activity_type",
        "op": "eq",
        "value": "post_published"
      }
    ],
    "status": "disabled"
  },
  "nodes": [
    {
      "id": "start",
      "kind": "trigger",
      "name": "A lead's post was captured",
      "ui": {
        "x": 0,
        "y": 0
      }
    },
    {
      "id": "engage",
      "kind": "tool",
      "name": "Enroll the author if they are a focus lead",
      "ui": {
        "x": 260,
        "y": 0
      },
      "tool": "oxygen.engage_enroll",
      "effect": "external_write",
      "params": {
        "sequence": {
          "type": "literal",
          "value": "<engage-sequence-slug>"
        },
        "activity": {
          "type": "ref",
          "path": "trigger.input"
        },
        "focus_limit": {
          "type": "literal",
          "value": 25
        }
      }
    }
  ],
  "edges": [
    {
      "id": "start-engage",
      "source": "start",
      "target": "engage"
    }
  ],
  "source_hash": "",
  "compiler_version": "oxygen-workflows-v2"
}
```

A lead enters a Sequence once for life, so each focus lead is engaged on their first captured post.
