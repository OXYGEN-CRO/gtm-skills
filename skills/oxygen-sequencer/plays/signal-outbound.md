# Signal-based email outbound

## When

People or companies showed a signal. Which signals come first: `oxygen skills get oxygen-sourcing --file references/playbook.md`. Signals rank who goes first; they are not the only lane, so the whole-market play (`plays/whole-tam-email.md`) runs beside this one. Engagers and profile viewers are warm: LinkedIn first (`plays/multichannel-top-tier.md`). This play emails the rest.

## Numbers

- **First touch** within 24 hours of an intent signal and within 7 days of a market signal. Drop a signal older than 30 days.
- **2 emails** on working days 0 and +3, the second in the same thread; size inboxes at 2 emails per contact (`oxygen-email-infra` skill).
- **Copy:** written per lead (`references/cold-copy.md`, Signal leads), naming the pain, never the signal ("saw you're hiring" is out). Email 1's CTA asks for a reply that gets one concrete free thing ("Let me know if I should send over <a personalised plan>."), never a meeting or a calendar link.

## Steps

The `oxygen-signals` skill owns capture and routing.

1. Capture into one audience table:
   - Market signals: `oxygen signals search plan --family hiring --scope market --keywords "<role>" --last-days 30 --estimate --json > plan.json`, then `oxygen signals search run --plan-json ./plan.json --mode live --approved --max-credits <n> --bind-feed --every daily@9 --max-credits-per-cycle <n> --json` into a company table (`oxygen skills get oxygen-signals --file references/signal-feeds.md`, which says which families can be armed). The feed adds companies, not people: the people at each new company go into the audience table through the `oxygen-sourcing` skill.
   - Website visits and signups: read `oxygen signals leads-today --json` each day and add the fits with `oxygen tables upsert <table> --key linkedin_url --rows-json '<rows>' --json`.
2. Add the columns the router checks: a verified `email` and `email_status` (`oxygen-enrichment`), a qualification column whose rule makes a signal older than 30 days ineligible, and `signal_line` and `idea` AI columns written per the cold-copy rules.
3. Write `steps.json`:
   ```json
   {"steps":[
    {"id":"e1","channel":"email","kind":"email_send","subject_template":"<subject>","body_template":"Hi {{first_name|there}},\n{{signal_line}}\n<pitch>\n{{idea}} <CTA>"},
    {"id":"w1","kind":"wait","days":3,"working_days":true},
    {"id":"e2","channel":"email","kind":"email_send","body_template":"<follow-up>"}]}
   ```
4. `oxygen sequences create --name "Signals" --slug signals --steps-file ./steps.json --channels email --table <table> --no-auto-enroll-table-rows --json`, so only the router enrolls: without the flag the launch enrolls every row, qualified or not.
5. Launch through the ladder in `SKILL.md`, then preflight and apply the `qualified-audience-router` Blueprint (`oxygen blueprints preflight qualified-audience-router --input-json '<inputs>' --json`, then `oxygen blueprints apply`), as `oxygen skills get oxygen-signals --file references/audience-campaigns.md` describes. List `signal_line` and `idea` among its evidence columns so no lead enrolls before its copy exists. The router runs daily at 09:00 UTC by default and enrolls at most 20 rows a cycle.

## Kill and scale

- **`emailFunnel.sent` at 40 or more with `emailFunnel.positive` at 0** (`oxygen sequences stats signals --json`; 40 sends is about 20 people): change the angle before blaming the signal.
- A source that keeps firing without positive replies: `oxygen feeds pause <feed> --json`.
