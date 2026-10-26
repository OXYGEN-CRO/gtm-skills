# Whole-market cold email

## When

Cold email across the whole market, evergreen and at full capacity. Email only; LinkedIn is for top-tier leads (`plays/multichannel-top-tier.md`). Signals decide who goes first (`plays/signal-outbound.md`); they never replace this lane.

## Numbers

- **3 emails** on working days 0, +3 and +7; emails 2 and 3 reply in the same thread. Copy: `references/cold-copy.md`.
- **One table and one Sequence per segment** (industry × size band); one segment at a time, opening the next only at the scale bar. KPI order: revenue, booked calls, positive replies, replies; never opens.
- **Daily capacity:** daily sends = TAM contacts × 3 ÷ 42 weekdays, rounded up (the `oxygen-email-infra` skill's cold email playbook §2 sizes the inboxes); new first touches a day = daily sends ÷ 3, the Sequence's `--max-new-enrollments-per-day`.
- **Email 1's CTA** asks for a reply that gets one concrete free thing ("Let me know if I should send over <a personalised plan>."), never a meeting or a calendar link.
- **Spintax** `{a|b}` on the greeting, the pitch verb, the whole CTA sentence and the subject: 2–4 options a block, at most one block a sentence. Never put a `{{column}}` inside a block.
- **A/B:** one variable a round, 2 variants, in order CTA, subject, pitch line, AI prompt. A round is 2,200 contacts with `min_sends_per_variant: 1000`, each in a new Sequence (`oxygen sequences duplicate`) because copy locks at start. The auto-winner needs every variant at that floor and 5 replies; a hash split gives each variant about 1,100 ± 25 sends, which at the typical 0.74% reply rate expect 8 replies, so both reach 5 in about four rounds out of five.
- **Re-contact** non-repliers every 60 days with a new angle, never people who replied, unsubscribed or bounced.

## Steps

OXYGEN cannot enroll only the rows no earlier Sequence emailed: `--from-table` and auto-enroll take every row the Sequence does not hold, and `--exclude-contacted` skips only people mid-journey elsewhere. So batches go by creation order, and these Sequences never use `--from-table` or auto-enroll.

1. Take the round's batch, oldest rows first (`<n>` = 2,200 × rounds already run), and write `{ "leads": [{ "table_row_id": "<_row_id>" }] }` files of 500:
   `oxygen tables query <table> --sort-json '[{"columnKey":"_created_at","direction":"asc"}]' --offset <n> --limit 2000 --fields _row_id --output ./batch.json --json`, then again with `--offset <n + 2000> --limit 200`.
2. Add the `icebreaker` and `idea` columns (`oxygen columns add <table> --key icebreaker --label Icebreaker --prompt '<cold-copy rules>' --json`); price each with `oxygen columns run <table> icebreaker --all --dry-run --json`, then run it with `--all --background --approved --max-credits <n>`.
3. Write `steps.json`; round 1 tests the CTA:
   ```json
   {"steps":[
    {"id":"e1","channel":"email","kind":"email_send",
     "subject_template":"{<subject A>|<subject B>} {{company_name}}",
     "body_template":"{Hi|Hey} {{first_name|there}},\n{{icebreaker}}\n<pitch with one {verb|verb}>\n{{idea}} {<CTA 1>|<CTA 1 reworded>}",
     "variants":[{"body_template":"<same body, CTA 2 spun the same way>"}],
     "auto_optimize":{"metric":"reply","min_sends_per_variant":1000}},
    {"id":"w1","kind":"wait","days":3,"working_days":true},
    {"id":"e2","channel":"email","kind":"email_send","body_template":"<follow-up>"},
    {"id":"w2","kind":"wait","days":4,"working_days":true},
    {"id":"e3","channel":"email","kind":"email_send","body_template":"<follow-up>"}]}
   ```
4. `oxygen sequences create --name "<segment> r1" --slug <segment>-r1 --steps-file ./steps.json --channels email --table <table> --no-auto-enroll-table-rows --max-new-enrollments-per-day <n> --json`.
5. `oxygen sequences enroll <segment>-r1 --leads-file ./leads-1.json --json` per file, then check `oxygen sequences esp <segment>-r1 --json` against the playbook's provider mix.
6. Launch through the ladder in `SKILL.md`, with `--max-live-sends` = enrolled leads × 3.
7. Next round, after `oxygen sequences variants <segment>-r1 --json` shows the decision (none: keep the base). Copy locks at start, so `oxygen sequences duplicate <segment>-r1 --name "<segment> r2" --slug <segment>-r2 --json`, set winner as base and the next variable as variant b (`oxygen sequences update <segment>-r2 --steps-file ./steps-r2.json --json`), then steps 1, 5 and 6. After the last round, feed the last Sequence step 1's batches until the query returns no rows.
8. Re-contact no earlier than 60 days after the cycle's first send, at the same daily pace: duplicate the last Sequence with a new angle and enroll the `_row_id`s from `oxygen sequences contacts <sequence> --contact-state contacted --exclude-contact-state replied --limit 500 --json` for each Sequence of the cycle. Do-not-contact already blocks bounces and unsubscribes.

## Kill and scale

Judge after 1,000 contacted across the segment's Sequences, by `total_count` of `oxygen sequences contacts <sequence> --contact-state contacted --limit 1 --json`, then of `replied` and `positive_reply`.

- **Reply under 0.37%** (bottom quartile, 270 contacts per reply): fix placement (`oxygen-deliverability`) and the list, not the copy.
- **Scale** at 0.7% reply or better and at least 1 positive reply per 500 contacted: open the next segment and grow inboxes through the playbook.
- In between: run the next A/B round.
