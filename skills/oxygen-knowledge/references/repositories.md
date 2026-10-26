# GitHub and Obsidian repository mounts

The local mirror contains server-rendered wiki pages under the CLI config directory (`OXYGEN_CONFIG_DIR` when set, otherwise the platform default). It is a manual editor cache. It is separate from a GitHub repository mount, which retains original repository-relative paths, eligible non-Markdown attachments, immutable file revisions, and an optional automatic two-way transport.

Connect the GitHub App first, then discover the immutable repository and branch IDs before previewing a mount:

```bash
oxygen integrations connect github
oxygen integrations github repositories --connection-id <connection_id> --json
oxygen integrations github branches --connection-id <connection_id> --repository-id <repository_id> --json
oxygen knowledge repositories preview --connection-id <connection_id> --repository-id <repository_id> --branch main --root-path "" --mode two_way --json
oxygen knowledge repositories connect --connection-id <connection_id> --repository-id <repository_id> --branch main --root-path "" --mode two_way --preview-token <token> --approved --json
```

The Oxygen GitHub App requests Contents read and write plus Metadata read on the repositories you select, and push events; it requests no account or organization permissions. When a deployment has not enabled GitHub, `integrations list --json` reports GitHub `availability.status` as `unavailable` with a reason and `next_step`, and connecting fails with `github_not_configured`.

Preview has no activation side effect. Connect requires the exact preview token and `--approved`. `import` copies once; `two_way` grants standing writes to that exact repository, branch, and root. Import and “sync now” are queued worker operations, so read `knowledge repositories list` until status and freshness advance rather than claiming the GitHub branch changed immediately. Successful automatic polls are scheduled roughly every 4.5–5.5 minutes; a push webhook or explicit sync request can make work due sooner, but processing remains asynchronous.

Use `knowledge files list|get|upsert|archive|download` for original paths and file revisions. Every write carries `--expected-revision` (`0` only for create). `--file` sends exact bytes; MCP file upsert uses `bytes_base64` for opaque originals. `--properties-json` changes only named Markdown frontmatter properties. In the web app, open a connected repository to add a file at an exact repository-relative path; open an existing file to edit readable source, replace its original bytes, or archive it. `.base` files render as tables, cards, or kanban views in Knowledge; edits keep frontmatter and use Base Board lane order and `kanban_order`. Attachments retain exact bytes and SHA-256 verification. Downloads refuse to overwrite an existing local path.

Repository conflicts retain the base, Oxygen, and GitHub versions. Inspect them with `knowledge repositories conflicts --mount-id <id> [--path <path>]`, then resolve with the exact reviewed local revision and remote SHA plus `--approved`. A resolved edit to pinned canonical voice, brand, positioning, or playbook content still becomes a Knowledge proposal; repository transport never bypasses that gate.

Limits: 25,000 eligible files, 1 GiB retained bytes per workspace, 100 MiB per attachment imported through GitHub, and 1.5 MB for editable UTF-8 Markdown. An inline `knowledge files upsert` request has a 2 MB JSON-envelope limit; base64 overhead makes its usable binary payload smaller, so move larger originals through the connected GitHub repository. Credential files, machine state, symbolic links, submodules, and GitHub workflow files are excluded. Obsidian settings, Base Board data, scripts, and plugins may be preserved as inert files; Oxygen never runs imported plugins or scripts.

GitHub previews label the size of Git blobs. Expanded Git LFS object sizes are additional and checked during import; the retained workspace quota can pause an import after some files are saved. Progress and accepted files remain available.
