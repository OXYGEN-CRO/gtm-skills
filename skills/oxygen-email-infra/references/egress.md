# Mailbox egress IPs

Every native Gmail or Microsoft send, reply read and token refresh leaves from an OXYGEN-managed static egress IP: the shared one, or the workspace's dedicated one. Inboxes connected through Zapmail (Zapbox) send through Zapmail and use neither.

- Read the posture with `oxygen egress status --json` and `oxygen egress ips --json`, and quote the address they report. A configured address shows policy, not observed traffic.
- A dedicated IP is preview first: `oxygen egress dedicated request --json` shows the recurring price and terms, and `--approved` orders it. `--country <ISO code>` asks for a region where the mailbox owners plausibly sign in; promise only a country the preview confirmed. Every current inbox moves to the dedicated IP and future inboxes join it automatically.
- `oxygen egress dedicated cancel` previews; `--approve` cancels at the end of the period already paid, with no refund or early cutoff, and the workspace returns to the shared IP.
- `egress status` reports blocked transport states (missing entitlement, inventory, handoff, liveness). Sending stays paused while one is blocked, which keeps the isolation the workspace paid for; contact support and leave the mailbox assignments as they are.

A dedicated IP gives account safety and tenant isolation: a stable, unshared sign-in source that another workspace's history cannot touch, and one address a customer's IT can allowlist in Microsoft Conditional Access or Google context-aware access. It is not a deliverability or placement lever: Gmail API and Microsoft Graph mail leaves through Google's and Microsoft's own relays, and recipients never see the egress IP. The exception is a Microsoft mailbox on SMTP transport, where Exchange Online may record the submitting IP in the headers.
