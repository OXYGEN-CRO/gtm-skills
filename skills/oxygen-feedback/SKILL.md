---
name: oxygen-feedback
description: "File OXYGEN feedback or a bug only after explicit consent; diagnosis never submits."
allowed-tools: Bash(oxygen *), AskUserQuestion
---

# OXYGEN Feedback

In-app help is the bottom-right chat; the sidebar's **Support** row opens it.

1. Obtain consent; otherwise diagnose with `oxygen-diagnostics`.
2. Check existing issues first. When discovery exposes native workspace chat,
   use `oxygen chat threads list --json` (MCP `oxygen_chat_threads_list`); otherwise use `oxygen support list --status open --json`.
   Continue an existing issue instead of filing it again; Plain does not auto-dedupe.
3. Draft expected/actual, impact, reproduction, IDs, version, and environment.
   Exclude secrets and unrelated data. When the customer chooses a local
   conversation log, attach it explicitly with `oxygen feedback --file <path>`
   (or `--session-id` / `--include-transcript` for the session they selected).
   Review it first; credential redaction is best-effort. Hosted MCP can attach
   only the customer-selected excerpt or gzip transcript, never an unseen local file.
4. Show the exact message/category, context and selected attachment; obtain
   confirmation before sending. File once through `oxygen feedback --message ...`
   (MCP `oxygen_feedback`): enabled dev uses native workspace chat; production
   and deployments without native chat use Plain. Return the provider, Thread ID/link.
5. For a returned `provider: "oxygen"`, use its `thread.id` with
   `oxygen chat threads get --thread-id <thread-id>` and, after confirmation,
   `oxygen chat threads reply --thread-id <thread-id> --body ...`
   (MCP `oxygen_chat_thread_get` / `oxygen_chat_thread_reply`). Keep native IDs
   out of Plain commands. For Plain Threads, retain
   `oxygen support chat <thread-id> --message ...`; a structured Plain filing
   may use `oxygen support file --subject ... --body ...` with its selected transcript.

On `plain_headless_portal_unavailable`, report the Thread ref; never refile. Use
in-app Chat or email `priority@oxygen-agent.com` with the ref for reconciliation.

Never promise a fix date or message another customer.
