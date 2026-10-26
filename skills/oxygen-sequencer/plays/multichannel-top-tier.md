# Email + LinkedIn for top-tier leads

## When

High-fit accounts and signal leads only. Invites are capped per account (`oxygen senders limits get <id> --json`), so LinkedIn cannot carry market volume: the rest of the market gets `plays/whole-tam-email.md`. Two orders:

- **Top tier, cold:** email first, LinkedIn alongside.
- **Warm signals** (engagers on your posts, profile viewers): LinkedIn first, email as the fallback.

## Numbers

- **Cold order:** email 1 on working day 0, invite on day 1, email 2 on day 3, email 3 on day 7; people who accepted get the LinkedIn message 1 day after email 3. An unaccepted invite is withdrawn about 14 days after it went out.
- **Invite note:** a hook only, no offer, at most 200 characters. OXYGEN trims longer notes at send, because accounts without Premium refuse them and an account's tier is unknown.
- **Email copy:** `references/cold-copy.md`. In the inbox sizing (`oxygen-email-infra` skill) the cold order is 3 emails per contact.

## Steps

1. Put the leads in one table with `linkedin_url`, a verified `email` and the copy columns. One sender profile sends both channels: `oxygen senders profiles list --json`.
2. Cold order, `steps.json`. Journeys run one step at a time, so the message waits for email 3; the connection wait starts about a week after the invite, so `timeout_days` 7 withdraws it about 14 days after sending:
   ```json
   {"steps":[
    {"id":"e1","channel":"email","kind":"email_send","subject_template":"<subject>","body_template":"<email 1>"},
    {"id":"w1","kind":"wait","days":1,"working_days":true},
    {"id":"invite","kind":"invite","note_template":"{{invite_hook}}"},
    {"id":"w2","kind":"wait","days":2,"working_days":true},
    {"id":"e2","channel":"email","kind":"email_send","body_template":"<email 2>"},
    {"id":"w3","kind":"wait","days":4,"working_days":true},
    {"id":"e3","channel":"email","kind":"email_send","body_template":"<email 3>"},
    {"id":"accept","kind":"wait_for_connection","timeout_days":7,"on_timeout":"stop","withdraw_on_timeout":true},
    {"id":"w4","kind":"wait","days":1},
    {"id":"dm","kind":"message","template":"{{linkedin_message}}"}]}
   ```
3. Warm order, `steps-warm.json`. Connected people get the message, then the email 3 working days later; the rest get the email when the invite times out:
   ```json
   {"steps":[
    {"id":"invite","kind":"invite","note_template":"{{invite_hook}}"},
    {"id":"accept","kind":"wait_for_connection","timeout_days":14,"on_timeout":"continue","withdraw_on_timeout":true},
    {"id":"conn","kind":"branch","condition":"already_connected","then_id":"dm","else_id":"e1"},
    {"id":"dm","kind":"message","template":"{{linkedin_message}}"},
    {"id":"w1","kind":"wait","days":3,"working_days":true},
    {"id":"e1","channel":"email","kind":"email_send","subject_template":"<subject>","body_template":"<email>"}]}
   ```
4. `oxygen sequences create --name "<name>" --slug <slug> --steps-file ./steps.json --channels email,linkedin --table <table> --sender-profiles <id> --json`. The warm order is a second Sequence created the same way from `steps-warm.json`.
5. Launch through the ladder in `SKILL.md`.
6. Warm captures enroll themselves with `oxygen linkedin intent autoenroll --account <ref> --sequence <slug> --json`: a standing grant whose approval the `oxygen-signals` skill describes.

## Kill and scale

Read `oxygen sequences stats <slug> --json` for invites sent and accepted and LinkedIn replies.

- **Acceptance under 25% or LinkedIn reply under 10%:** change the audience, not the copy.
