# Graphics

`oxygen visuals` renders self-contained HTML, CSS and inline SVG to PNG or PDF. Rendering is free.

## When a post gets one

Only when the content itself is a map, list, flow, comparison or scoreboard. Otherwise post text only, or write a designer brief.

## What the renderer can and cannot do

- JavaScript is off. Any remote image, font or stylesheet fails the render (`visual_render_failed`); data URLs don't display. Draw everything in inline SVG and CSS: no photos, screenshots or raster logos.
- One font: Inter, regular weight. No web fonts; bold is synthesized, so build hierarchy from size, spacing and colour.
- Default 1080x1350 (LinkedIn portrait). Up to 12 pages per render, at most 32 million pixels across all pages: at 1080x1350 that is 12 pages at 1x, 5 at 2x (`visual_render_limit` beyond). Each page renders as its own PNG and its own single-page PDF, whose text is not selectable.
- No image generation, motion or video.
- `visual_renderer_unavailable` from `render-preview` means rendering is off here: keep the source and say the render is pending.

## Brand

Without a canonical brand, make a plain unbranded draft (no invented logo, palette, signature or footer) and label its choices as drafts. A missing brand never authorizes copying a reference creator's identity; one graphic never changes the workspace brand.

## Copy on the graphic

- Select the author's own lines verbatim instead of paraphrasing them into smoother copy; never paste the whole post. Keep order, numbers and caveats that change meaning.
- On an instructional graphic, every line tells the reader what to do or states a fact they can act on: "Create 1 folder and 1 rules file", not "the setup takes 1 afternoon". Descriptive lines read as AI filler.

## Layout rules

- One accent per image, placed where it means something.
- Fill the canvas: no third of the page left dead. Split dense material across pages before shrinking text.
- Carousels: 5 to 12 pages (2x only up to 5). Under 5 it is a single graphic. Each page has one job; keep continuity (same headline treatment, page number, kicker).
- A CTA page only when the post has a real next step.

## The loop

```bash
oxygen visuals source-create --name <slug>-p1.html --file p1.html --json
oxygen visuals render-preview --source-file-ids <id1>,<id2> --json
oxygen visuals render-start <render_id> --scope-hash <scope_hash> --json
oxygen visuals render-get <render_id> --wait --json
```

1. One source per page; the preview fixes page order and returns `render.id` and `render.scope_hash`.
2. `render-get --wait` returns `outputs[]` (`file_id`, `page`, `format`) once `completed`. `effect_unknown` never retries itself: read the run before rendering again.
3. Look at every PNG: MCP `oxygen_visual_image_view` with its `file_id` returns the pixels; on the CLI, download it and open the image. Check text accuracy against the post, hierarchy, line breaks, clipping, contrast and connector collisions, at full size and at a small viewing size.
4. Make 1 deliberate refinement pass on the largest visible weakness (hierarchy, line breaks, spacing or crop before decoration), saved as a revision: `oxygen visuals source-create --name <slug>-p1.html --file p1.html --parent-file-id <old_id> --json`. Render and look again.
5. Export for the post:

```bash
oxygen visuals download <file_id> --out p1.png --json
oxygen publishing media upload p1.png --json
oxygen publishing posts update <post_id> --content-merge-json '{"media_asset_ids":["<m1>","<m2>"]}' --json
```

Repeat the download and upload for each page's PNG. OXYGEN has no PDF merge: attach the page PNGs in page order. Changing an approved post's content revokes its approval (`oxygen-publishing`).

## Review

- Name the evidence you had: source only, rendered but not inspected, or rendered and inspected. Never claim a visual review from source code or a successful render alone.
- For a carousel, inspect every page plus continuity; a contact sheet does not prove each page was seen.
- Review is report-only unless fixes were asked for; rerender and reinspect anything you changed.

Editable flowcharts and 3D dioramas need a local agent with its own tools.
