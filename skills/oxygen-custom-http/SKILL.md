---
name: oxygen-custom-http
description: "Register, connect, preview, run and remove reusable custom HTTP integrations in OXYGEN. Covers manifest schema, auth, path/query/body inputs, custom_http tool ids and Table tool columns. Use for your own REST API or disposable HTTP probes."
allowed-tools: Bash(oxygen *)
---

# OXYGEN Custom HTTP

A custom integration turns a public HTTPS API into workspace catalog tools, named `custom_http.<slug>.<operation>`. Registration and credentials require a plan supporting BYOK; removal stays available after a downgrade. Its encrypted credential is injected server-side. Inline HTTP columns are a separate single-column request format; use the oxygen-tables skill for those.

## Register the API

Save a JSON manifest, then apply it. This saves configuration and makes no provider call:

```json
{
  "version": 1,
  "slug": "contact_api",
  "name": "Contact API",
  "description": "Look up a contact in our API.",
  "baseUrl": "https://api.example.com/v1",
  "auth": { "type": "bearer" },
  "operations": [{
    "operation": "lookup",
    "method": "GET",
    "path": "/contacts/{contact_id}",
    "effect": "read",
    "fields": [
      { "key": "contact_id", "type": "string", "required": true, "location": "path" },
      { "key": "include_history", "type": "boolean", "required": false, "location": "query" }
    ],
    "outputPath": "contact"
  }]
}
```

```bash
oxygen custom-integrations apply --manifest ./contact-api.json --json
oxygen custom-integrations list --slug contact_api --json
oxygen custom-integrations connect contact_api --secrets-file ./contact-api.env --json
```

`apply` takes either `--manifest <file>` or `--manifest-json '<object>'`. `slug` and operation ids use lowercase letters, digits and underscores, start with a letter and contain at most 63 characters; imported hyphens normalize to underscores. Reapplying a slug updates its manifest; reapplying a removed slug reconnects its saved definition, but its old credential is gone. Use distinct slugs for distinct APIs.

Required manifest fields are `slug`, `name`, `baseUrl` and nonempty `operations`. `version` defaults to 1, `auth` to none. Each operation requires `operation`, `method` and `path` (starting with `/`). Methods: GET, POST, PUT, PATCH, DELETE. `effect` defaults to read for GET and write otherwise; a non-GET cannot declare read. Optional `displayName`, `summary`, `inputSchema`, `outputSchema`, `outputPath`, `idempotent`, `timeoutMs` (default 10,000, max 300,000) and `maxResponseBytes` (default 1,000,000, max 5,000,000) refine the descriptor. Private hosts and redirects are blocked.

Fields take `key`, `type`, `required`, `description`, `location` and `wireKey`. Types: string, number, boolean, string[], number[], object, object[], array. `required` defaults true. Path inputs replace `{name}`; query inputs become URL parameters; body inputs become JSON properties. `wireKey` renames the field on the wire. Location defaults to query for GET, body otherwise. With no fields, GET forwards raw input as query parameters and other methods forward it as JSON. A GET cannot have a body.

## Attach credentials

| Auth block | Credential use |
| --- | --- |
| `{"type":"none"}` | Skip connect |
| `{"type":"bearer"}` | Authorization: Bearer token |
| `{"type":"api_key_header","header":"X-API-Key","prefix":""}` | Named header, optional prefix |
| `{"type":"api_key_query","param":"key"}` | Named query parameter |
| `{"type":"basic","username":"user"}` | Basic username plus stored password |

Never put secrets in a manifest, Table, tool input or conversation. The `.env` file holds a single KEY=VALUE entry, or one named API_KEY, TOKEN, PASSWORD or SECRET. The terminal or Connections page can attach it without sharing it with an agent. MCP `oxygen_custom_integration_connect` accepts a credential, so use that only when the user deliberately authorizes sending it through the client.

## Preview, then run

```bash
oxygen tools get custom_http.contact_api.lookup --json
oxygen tools run custom_http.contact_api.lookup --input-json '{"contact_id":"123"}' --mode dry_run --json
oxygen tools run custom_http.contact_api.lookup --input-json '{"contact_id":"123"}' --mode live --json
```

Review the exact endpoint, inputs and redacted request before live execution. Custom HTTP charges zero Oxygen credits (`no_bill`); the user owns any upstream API charges. Obtain explicit scope and an upstream spend ceiling before paid calls. Live writes require explicit approval and `--approved`; custom HTTP needs no `--max-credits`. A preview never approves a live write. Do not run a diagnostic request live just to validate registration.

The result's `output` is the projected answer; `data` is the complete response; `request` and `response` are call evidence. A Table stores the answer. Bind reusable row work with a tool column, then preview one row before a bounded run:

```bash
oxygen columns add <table> --label "Contact lookup" --kind tool --definition-json '{"toolId":"custom_http.contact_api.lookup","inputMapping":{"contact_id":{"type":"column","columnKey":"contact_id"}}}' --json
oxygen columns run <table> contact_lookup --limit 1 --dry-run --json
```

## Remove throwaways

```bash
oxygen custom-integrations remove contact_api --json
oxygen custom-integrations remove contact_api --approved --plan <plan_hash> --json
oxygen custom-integrations list --slug contact_api --json
```

Review the returned connection id, tool ids and warning, then approve that exact hash. If multiple rows share a slug, select `--connection-id <id>`; ambiguous removal fails closed. A changed preview needs a fresh review. Removal disconnects only that workspace connection, deletes its encrypted credential and removes its catalog tools. Saved columns, workflows and run history remain; callers of these tools fail until repaired or reconnected. It does not revoke the key at the provider. Connections → Custom HTTP → Disconnect shows the same preview and confirmation.

MCP equivalents are `oxygen_custom_integrations_apply`, `oxygen_custom_integrations_list` and `oxygen_custom_integrations_remove`; removal takes `slug` or `connection_id`, then `approved: true` and the returned `plan_hash`. Use capability discovery to load their exact schemas. A removed tool must disappear from discovery and refuse execution, including when a caller still knows its tool id.
