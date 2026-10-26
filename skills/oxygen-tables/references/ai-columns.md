# AI, Classify and formula columns

Formula for deterministic extraction, normalization and arithmetic; Classify for closed labels, yes/no decisions and ordered scores; an AI column for synthesis and prose over data the row already holds. An AI column has no web access: for a web fact use a research column ([research](research-columns.md)).

## An AI column is a prompt

Pass the prompt with `--prompt` (inline text or a prompt file) and reference the row's columns as `{{column_key}}`. `--kind ai` and the data type are implied; no `--input-mapping` is needed.

```bash
oxygen columns add leads --label "ICP Fit" \
  --prompt "Score {{company_name}} for this ICP: B2B SaaS selling to GTM teams. Return tier and reason." --json
oxygen columns run leads icp_fit --limit 1 --dry-run --json
```

- Tokens are checked against the table's real columns before the column is saved, on every surface: a typo fails at once with `invalid_prompt_column` and the near-miss keys. `oxygen tables describe <table> --json` lists the exact keys.
- A token may reach into a JSON cell (`{{research.summary}}`), and a whole jsonb cell interpolates as JSON (`{{page_content}}`).
- Naming a column in prose delivers nothing: only a `{{token}}` moves the value.
- `--input-mapping` carries what a prompt cannot name itself, literals and workspace context: `--input-mapping '{"icp":{"type":"context_profile","path":"icp"}}'` with `{{icp}}` in the prompt. Row columns belong in the prompt; `oxygen columns deps <table> --json` prints what every column reads and what reads it.
- `oxygen columns update <table> <column> --prompt "..."` rewrites a prompt with the same token check.
- `--definition-json` holds definition fields with no flag (`credentialMode`, `webSearch`, `promptTemplateSlug`); flags merge on top, and declaring `prompt` in both is refused.

## Fields, not prose

End a prompt with `Return the following sections:` and one `Label: what goes here` line per field, and the column answers in exactly that shape. Each section becomes a sub-column you can reference (`{{icp_fit.Score}}`), filter, sort and export before the column has ever run. `oxygen columns fields <table> <column>` lists what a column exposes (also `output_fields` in `tables describe`); a typo'd field is rejected when the prompt is saved. A prompt without sections stays prose, which is right for copy; `--no-structured-output` forces prose. For a typed object, pass a JSON Schema with `--output-schema-json` or `--output-schema-file`: a text column stores the validated JSON as text, a jsonb column stores the object.

## Template keys

`--prompt-key <key>` with `--input <name>=<column>` (or `--input-mapping`) materializes a maintained prompt and output schema instead of your own text; `oxygen columns catalog --json` lists keys, inputs and per-row credits ([templates](templates.md)). Copy-class keys (`email_draft_v1`, `sequence_outline_v1`, `personalization_fact_v1`, `subject_line_variants_v1`, `email_qa_critique_v1`) refuse an input mapping that reads only manual name, title or company columns: enrich or research first, then write. Chain them by field: `{{email_draft.subject}}`.

## Workspace knowledge

AI and research columns retrieve relevant workspace knowledge by default; cell inputs record which pages grounded the request. To disable automatic knowledge retrieval for a column, set `--definition-json '{"knowledgeRetrieval":false}'` when adding or updating it. Classify uses workspace knowledge only with `--grounding workspace`.

AI message columns also receive the workspace's pinned canonical voice, brand and positioning pages (pinning them: the `oxygen-knowledge` skill, `references/context-bootstrap.md`). A `columns run` envelope reports `context: { applied, available, missing }`. `definition.copyContext: "off"` disables that separate copy preamble; `"on"` forces it on. Use both `knowledgeRetrieval: false` and `copyContext: "off"` to exclude both sources of automatic context from a copy column.

## Row selection

For a requested subset or ranking, resolve the user's filters and order and carry the exact row identities into the native run selection. `--limit` alone is not a ranked Top N. Read the requested values back on that same cohort and disclose any shortfall. Use the column's native schema and requested criteria; neither the number of axes nor their labels and order are a fixed recipe.

## Preview, condition, model

- `oxygen columns run <table> <column> --row-id <row_id> --dry-run --json` resolves the model, the credit estimate and the prompt rendered with that row (`ai.prompt_preview`), free. `prompt_preview.includes_grounding: false` describes the preview text, not the live run's setting: workspace knowledge and web evidence are added at run time and can bill.
- `--run-condition '<formula>'` with `--run-condition-columns <csv>` runs the column only on matching rows; others are skipped as `run_condition_false` at 0 credits, before any model call.
- Managed columns use a reasoning tier: `--reasoning-level low|medium|high`, billed per tier. To pin a model, connect an OpenRouter key and use `--definition-json '{"credentialMode":"byok"}' --model <openrouter-model-id>`. BYOK changes only the model bill: web grounding still spends credits, a live BYOK run always needs approval, and `--max-credits` may be omitted only when the preview reports an exactly known zero estimate.

## Classify every row

Classify uses the non-generative TypeSafe JEV classifier. It writes a typed decision, confidence and review status without generating prose. Its engine is `definition.decision`; generic AI model settings do not select its provider. Legacy `modelProvider`, `credentialMode` and reasoning fields may remain in saved column settings or receipts. Token usage and dollar cost record provider accounting. Confirm the actual engine, provider and charge from the classification preview and `oxygen table-runs provider-summary <action-run-id> --json`.

For ICP fit as ordered levels, save the ICP first, then add a Classify column over company evidence:

```bash
oxygen columns add leads --label "ICP Fit" --score "low,medium,high" \
  --prompt "How well does {{company_name}} fit our ICP? Description: {{description}}. Employees: {{employee_count}}. Do not infer missing facts." \
  --grounding workspace --json
oxygen columns run leads icp_fit --all --dry-run --json
```

`--classify <labels>` picks one label, `--yes-no <question>` answers yes or no and `--score <levels>` scores ordered levels. Name every evidence column the decision needs: once a prompt names one field, unmentioned row fields are not sent. The dry run's `evidence` lists selected, missing, omitted and shortened fields; workspace grounding is loaded only during execution, where evidence records its status and page revisions. Score cells hold `score` and `level`, plus `confidence`, `uncertain` and `reason`; the score is not a percentage, and `level` is nearest to it. Below the confidence floor (`--min-confidence`, default 0.85, or 0.7 for `--yes-no`), or with missing/shortened evidence or unusable workspace grounding, the best guess stays marked `uncertain` for review. Follow `classification_review.next_action`. Without `--grounding workspace` the classifier judges only the row and the question. Web: Add column, Classify. MCP: `oxygen_columns_add` with `column.definition.decision`.

## Formula columns

```bash
oxygen columns add leads --label "Primary Email" --kind formula --data-type text \
  --definition-json '{"expression":"path(person_enrichment, \"response.email\")"}' --json
oxygen formulas validate leads --expression 'normalize_company_name(company_name)' --json
```

A formula evaluates on read, so `tables query` shows its values without a run; `columns run` skips rows that already store a value unless `--force`. The exception is a fill-empty field (`fill: "empty"`), which is what an enrichment bundle's extractor columns are: its cell is stored and editable, `columns run` fills it only where it is empty, and a value someone typed is never overwritten. Formulas take bare column keys, no `{{ }}`. A field of another column is read directly as `{{column.field}}` in a prompt, so an extraction formula is needed only for a filterable scalar. String literals consume escapes: a regex backslash is doubled in the formula and doubled again inside JSON. Useful functions: `path`, `first`, `email_hash(email)` (SHA-256 for ad audiences; `email_hash(email, "md5")`), `normalize_company_name`, `clean_job_title`, `email_type`, `to_json_list`.

## Template overlap in generated copy

```bash
oxygen columns add <table> --kind formula --label 'copy_novelty_score' \
  --definition-json '{"version":1,"expression":"novelty_score(email_draft)"}' --json
oxygen table-runs provider-summary <run_id> --json
```

`novelty_score(<copy_column>)` returns 0 to 1 per row; a low score means the row's text repeats other rows, usually because the research it reads is too thin. The run's provider summary rolls it up as `copy_quality.template_overlap_ratio`, `weak_personalization_count` and `flagged_row_ids`; check the flagged rows before any send.
