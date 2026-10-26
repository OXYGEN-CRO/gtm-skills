# Import mailboxes and authorize them

Import registers exact Google Workspace or Microsoft 365 inboxes from any provider into the sending pool. It never scans a domain or enumerates a Google or Microsoft directory. Native sending then needs fresh authorization for each imported address: individual OAuth for Google and ordinary Microsoft accounts, or one Microsoft tenant authorization for an exact set of addresses.

## Choose the file

- Identity-only export: addresses plus Google or Microsoft platform data. No credential crosses the network. Use it for Microsoft, or whenever the export has no compatible Google app password.
- Credential export: the same fields plus a Google `app_password` per row. Only Google rows may carry one; it belongs to that exact mailbox, created from that account after 2-Step Verification is on (a super-admin credential never belongs in the file). Microsoft passwords are stripped or rejected.

Common vendor column names (Email Address, Provider, App Password, Mailbox ID, Entra Tenant ID, First Name, Surname, From Name) map automatically; `oxygen mailboxes import --help` lists the contract. A file is limited to 500 rows and 5 MB.

## Import

```bash
oxygen mailboxes import --file ./mailboxes.csv --vendor <source> --validate-only --json
oxygen mailboxes import --file ./mailboxes.csv --vendor <source> --sender <sender-profile-id> --json
oxygen mailboxes import --from credentials --vendor <source> --file ./mailboxes.csv --json
```

- `--validate-only` parses the whole file locally with no network call or write and returns counts plus the OAuth review plan. Any error rejects the whole file before the first write.
- Import costs 0 credits and is idempotent by address: rerunning the same file creates no duplicates.
- A mailbox the workspace does not hold yet needs a paid plan: on Free the import returns `402 upgrade_required`; relay `upgrade_url`, never a top-up. Re-importing or re-authorizing mailboxes it already holds stays open.
- Web: Accounts, Email, Add inboxes, Import a file. The browser validates locally and shows the review plan before Import.

Credentials stay out of chat and MCP. A secret-bearing import runs only through the signed-in web app or the local CLI; MCP, Copilot and Agent identities import identity-only rows. Only the canonical identity fields and one Google `app_password` cross the network: OAuth grants, MFA seeds, delegation secrets and conflicting password columns fail locally. The app password is encrypted on receipt, never returned, and expires after seven days unused; re-import locally if approval waits longer.

## Who each inbox sends as

Each imported inbox attaches to a sender profile, first match wins:

1. the row's own `sender_profile_id`;
2. `--sender <id>` for every row;
3. the row's first and last name (or display name), joining an active profile of that name;
4. otherwise a new profile named from the address (`alex.rivera@` becomes "Alex Rivera"), counted under `sender_profiles.created` and renamed with `senders profiles update <id> --name "..."`.

An inbox without its own From name takes the sender's name. Profiles in depth: [managed inboxes](managed-inboxes.md).

## Authorize native sending

```bash
oxygen mailboxes compatibility --json
oxygen mailboxes connect-oauth --vendor oxygen --provider google --mailboxes <address> --json
```

The preview names the exact accounts; `--approved` starts the run, and each owner opens their own consent link. Google and individual Microsoft runs cover up to 10 addresses each, because every address signs in separately.

For a dedicated Microsoft sending tenant, one administrator approves up to 500 exact addresses:

```bash
oxygen mailboxes connect-oauth --vendor oxygen --provider microsoft --authorization-mode tenant --mailboxes <a>,<b> --json
```

Then repeat with `--approved` and open the returned link as a Global Administrator or Privileged Role Administrator of that tenant; the grant requests the Microsoft Graph application permissions `Mail.Send` and `Mail.Read`, which Application Administrator and Cloud Application Administrator cannot consent to. OXYGEN probes only the submitted addresses, and a failed one stays Needs connection. For an ordinary company or personal Microsoft mailbox use `--authorization-mode individual`; `auto` picks tenant mode for several Microsoft addresses and individual for one. Tenant mode is agent-only: the app's **Add inboxes** connects every Google and Microsoft mailbox with one owner sign-in each and offers no tenant option.

A source app password, source OAuth grant or tenant id never counts as native-send authorization; incomplete rows stay Needs connection. Warm-up is a separate approval ([warm-up](warmup.md)).

## Zapmail inboxes (your own Zapmail account)

Zapmail bills your account for its inboxes; import and Custom OAuth cost 0 OXYGEN credits.

- Import per provider, because Zapmail lists each separately: `oxygen mailboxes import --from zapmail --provider google --json` and `--provider microsoft` (Microsoft rows get their Entra tenant id).
- Custom OAuth authorizes OXYGEN's app across your Zapmail Workspaces: `oxygen mailboxes connect-oauth --provider google --json` previews the pool, `--approved` starts it, `--status <export_id>` polls.
- Zapmail allows 3 Custom OAuth re-exports per mailbox per 7 days. OXYGEN retries eligible inboxes itself: in `mailboxes oauth-health`, `automatic_repair: queued` or `cooldown` means wait for `next_attempt_at`; `null` means follow the row's explicit remedy.
- Warm-up: Zapmail's Google inboxes enroll straight into `mailboxes warmup enable` (the credential is fetched at enrollment and never stored); its Microsoft inboxes first need one `mailboxes warmup microsoft` authorization per mailbox. Zapmail's credential list returns at most 500 entries, and unmatched addresses come back as per-mailbox reasons.

## Stop conditions

- `mailbox_credential_unavailable` or `not_connectable`: follow the exact row's remedy. A connected Google inbox without a transferable source credential can use separate `mailboxes warmup google` owner consent; protocol-only OXYGEN deliverability still needs a compatible credential import. See [warm-up](warmup.md).
- `plan_stale`: the scope, price, workspace, ramp or credential revision changed. Preview again.
- `mailbox_credential_rotation_requires_reconnect`: a provider write for this mailbox is still in flight. Run `oxygen mailboxes warmup status` to let it settle, then re-import. An enrolled mailbox rotates freely otherwise, and `mailboxes warmup reconnect` pushes the new credential.
- A provider authentication failure (`auth_invalid_credentials`, such as SMTP `535-5.7.8 Username and Password not accepted`): create a fresh Google app password, re-import it locally, then run `oxygen mailboxes warmup reconnect`. Enrollment alone keeps the dead credential, so the inbox would bill and send nothing; the warm-up history restarts, the renewal date stays. Keep the subscription: `warmup disable` cancels it and re-enabling bills a new cycle.
- A Microsoft mailbox is `consent_required`: read the row's `blocked_reason`
  before choosing a remedy, because two different states share this verdict.
  `smtp_not_consented` means the mailbox is already authorized and is missing the
  separate mail-submission permission — tenant authorization CANNOT supply that
  (application access covers Microsoft Graph only, and these are exactly the
  tenants that refuse Graph-submitted mail), so re-run the per-mailbox grant with
  `--authorization-mode individual` and complete every consent screen the browser
  link opens. Any other reason is a missing first authorization: use tenant
  authorization for a dedicated sending tenant, or individual OAuth for an
  ordinary mailbox. Never retry a password for either.

Removing or reconnecting an imported mailbox: [wind-down](wind-down.md).

## Google Workspace administrator access

Mailbox consent and Workspace administrator consent are separate. For Gmail delivery audit events, usage, domain/account/group administration and Postmaster data:

```sh
oxygen mailboxes google-workspace connect --json
oxygen mailboxes google-workspace connect --approved --json
oxygen mailboxes google-workspace status --json
oxygen mailboxes google-workspace status --connection <id> --live --json
oxygen mailboxes google-workspace disconnect <id> --approved --json
```

The first command previews exact permissions without storing anything. The approved start returns a Google consent URL; a Google Workspace administrator must complete it. OXYGEN workspace administrator access is also required. A saved grant is not proof that Google permits every API: `--live` checks read access and exposes scope versus privilege/edition failures. It sends no email, changes no Google settings and enrolls no paid services.

Existing grants need fresh consent for added scopes. Administrator authorization does not grant all users' mailbox access. Google DKIM key generation/signing activation still requires Google Admin Console; DNS publication uses the connected DNS provider. Warm-up and OXYGEN deliverability retain their supported credential/enrollment paths.
