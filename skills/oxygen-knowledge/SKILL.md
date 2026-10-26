---
name: oxygen-knowledge
description: "Operate OXYGEN knowledge: index-first retrieval, wiki pages/folders, GitHub repository mounts, citations, revisions, sources, synthesis, proposals, and local mirror. Use for company/ICP context, positioning, offers, voice, prompts, rubrics, and learnings."
allowed-tools: Bash(oxygen *)
---

# OXYGEN Knowledge Graph

Typed company/ICP context and wiki pages ground Tables, copy, Workflows, and Agents with recorded provenance.

## Index first

1. Read `knowledge index` before searching or inventing a slug.
2. Search and open relevant pages; follow useful wikilinks and backlinks.
3. Cite the slugs used.
4. File durable findings into the closest existing page and append a log entry.

Plain language uses hybrid recall when enabled; check `match_type`/`semantic_status`. Quotes, OR and exclusions stay lexical. Cite revisions; similarity is not confidence.

Reads cost **0 credits**; `commands get "<name>" --json` reports `spends_credits` for any command. Index `semantic.budget` is Oxygen's embedding spend, never yours.

Discover exact commands and MCP schemas:

```bash
oxygen capabilities search "workspace knowledge <goal>" --json
oxygen commands get "knowledge search" --json
```

MCP: `oxygen_capabilities_search`, then `oxygen_capabilities_schema` for the
selected tool. Start with `oxygen_knowledge_index`; search with
`oxygen_knowledge_search` (`query`), then hydrate the selected page read.

Read a page's evidence ledger with `knowledge page get <slug> --view sources`; use `--view full` for content, links and sources together. Follow `next_cursor` when present. Sources are immutable auto-filed observations; a URL in a page body or its structured data is a citation, not a source-ledger entry.

## Pages and folders

Reuse Markdown pages with `[[wikilinks]]`. Sources hold evidence; pages synthesize it. Revisions and the log preserve history.

Use `knowledge folders list`, `create --name "..." [--parent <id>]`, and `move <id> --parent <id|root>`; moves carry descendants and preserve slugs, links, and permissions. Create files with `knowledge page upsert --title "..." --folder <id> --create-only`; on updates, omit `--folder` to keep placement or pass `--folder root` to clear it. Read back results; honor `truncated`.

MCP: `oxygen_knowledge_folders_{list,create,move}`; move requires `parentId` and page upsert accepts `folderId` (each a UUID or `"root"`) plus `createOnly`.

Moving a page creates a revision and changes `data.knowledge_folder_id`. Archive with `knowledge page archive <slug> --expected-revision <n>`; content/history remain, but links become unresolved. Restore a working page with `knowledge page upsert --slug <slug> --status draft --expected-revision <current>`; omit the body to preserve it. Canonical-copy proposal gates still apply.

## Workspace skills

Create reusable private workspace guidance with `oxygen skills workspace create --name brief-review --description "Review customer briefs" --instructions "Check audience, offer, evidence and next action" --json`.

Import another source's skill with `oxygen skills workspace import --directory ./brief-review --source-url https://example.com/brief-review --json`, or use `--file ./SKILL.md` for one entrypoint. `--url https://…/SKILL.md` imports a public raw file (GitHub file URLs work too); a URL imports only SKILL.md, so upload the directory for supporting files. Imports support up to 50 UTF-8 text files, 120 KB each and 1 MB total; symlinks and binary files refuse. Scripts stay inert.

Find skills by purpose with `oxygen skills workspace list --query "customer briefs" --json`, and use the exact returned `workspace-…` name with `skills workspace get --name <name> [--file references/checklist.md]`. Read before editing; `skills workspace update --name <name> --content <text> --expected-revision <revision>` guards against overwriting newer work. Archive the entrypoint with `skills workspace archive --name <name> --expected-revision <revision>`.

MCP uses `oxygen_workspace_skills_list|get|create|import|update|archive`. Import takes either `files: [{path, content}]` (including root SKILL.md with YAML `name` and `description`) or `url`; optional `source_url` records supplied files' provenance. All operations cost 0 credits. Copilot can author and read the same skills. Knowledge → Skills browses workspace skills alongside Oxygen's shipped library; workspace files open in the ordinary Knowledge editor with revision history. Skills are private to the workspace, shared with its members. They grant no tool, spend or approval authority.

## Write boundary

Working research, learnings, and operational facts can be filed as logged revisions. Canonical customer-facing voice, brand, positioning, offer, and pinned playbook changes require proposals and approval; never silently overwrite live copy. Fill starter stubs draft-to-active and lint structural changes.

Thin or missing company, ICP or offer context, the typed profile, pinning protected canonical copy (`knowledge page pin` files a proposal for sensitive types) and the paid research pass (`knowledge bootstrap --live`, only on the user's explicit request, with `--max-credits` from its free preview, once per workspace): [context bootstrap](references/context-bootstrap.md).

Which voice, brand or positioning AI copy uses now: `context canonical get --type <type> --json` (MCP: `oxygen_context_canonical_get`); `grounding_when_absent` explains the fallback when none is pinned.

Read source and revision provenance before adopting synthesized outreach/reply/deal learnings as canonical strategy.

Learn the workspace's writing voice from its own sent LinkedIn and WhatsApp messages with `knowledge synthesize --kind voice --json` (MCP: `oxygen_context_synthesize`, kind `voice`). It is one low-cost AI call, priced as one low-reasoning AI column cell, and the preview runs it too, so get the user's yes before the first run. To hard-cap it, pass `--max-credits <n>` (MCP `max_credits`): the call is charged exactly its estimate, never more than `n`; a higher estimate is refused before the AI call with nothing charged and reports the estimate, so `--max-credits 0` is a free quote. To save the guide a preview showed, rerun with `--approved --body '<its body>'`, which makes no new AI call and costs 0 credits; `--approved` alone synthesizes and charges again. Saving files a pin proposal (`pinned: false`, `pin.proposal_id`): the canonical voice is live copy, so the guide becomes it only when the user approves that proposal (`knowledge proposals approve <id>`, MCP `oxygen_knowledge_proposal_decide`). Then it grounds message, reply, sequence and post drafts and AI columns. Fewer than 3 sent messages stops before the AI call with `insufficient_source_messages` and no charge. It reads sent messages only, not posts or emails. A UGC creator's voice is `ugc voice import`.

## Local mirror

Hosted Knowledge is authoritative. `knowledge sync` creates a disposable mirror: sync before editing, push deliberate changes, resolve conflicts, and verify revisions/`web_url`. Never make local files or chat a second source of truth. Repository mounts are separate: read [repositories](references/repositories.md).

Plays: [client-workspace-launch](plays/client-workspace-launch.md).
