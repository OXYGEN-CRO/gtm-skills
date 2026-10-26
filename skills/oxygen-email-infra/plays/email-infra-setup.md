# Set up cold email infrastructure

## The Play

Cold email sent from your main company domain can push all of your company's email into spam, so it goes out from a separate look-alike domain (for example getacme.com) with two inboxes in your name that warm up for 14 days first. OXYGEN quotes the domain and inboxes for free, buys them only after you approve the exact price, sets up SPF, DKIM and DMARC (the records that prove the mail is really yours) and starts the warm-up by itself. Expect 700-1,250 credits a year for the domain (`domains check` prices it) and 500 credits ($5) a month per inbox (`billing estimate --managed-mailboxes 2` prices them), so the first month is about 1,700-2,250 credits. Cold email never goes out from your own work inbox, even a little of it: that inbox stays for replies.

## Before You Start

- **What exists.** `oxygen domains list --json` and `oxygen mailboxes list` (free; without `--json` it prints the inbox count and every inbox that needs action first). If two or more inboxes on a separate sending domain (never the company's own) already show 14+ days of warm-up, tell the founder "You're ready to send" and go to outbound-pilot-50.
- **Credits.** `oxygen billing balance --json` (free): `spendable_credits`, which comes after the long `available_plans` list, covers the first month, about 1,700-2,250 credits for a domain and two inboxes (100 credits are about $1). The plan's monthly credits and `available_credits` are not what you can spend. If short: "The first month is about N credits and you have M; add credits at https://oxygen-agent.com/billing." Buying inboxes also needs a paid plan ($49 a month and up), whatever the credits: on Free the buy returns `upgrade_required`, so tell the founder to subscribe and link its `upgrade_url`, never a credit top-up.
- **Who the inboxes send as.** `oxygen senders profiles list --json` (free): one person with a real first and last name. If there is none, ask the founder: "Which full name should these inboxes send as?" The name and photo are stamped permanently, so never invent one. Until you have the name, price the inboxes without it: `oxygen billing estimate --managed-mailboxes 2 --json` (free, prices in force) gives their monthly credits, and step 1 gives the domain's yearly price. The exact quote in step 3 still needs the name, even for role addresses such as hello@ (without `--sender` it answers `invalid_request`): stop there and ask.
- **The domain owner's contact**, only when buying, on the first order: real name, phone, street, city, state, postal code and country.

## Steps

1. Price 3-5 look-alike domains in one call (free). Build them from the company's domain, for example get<brand>.com, try<brand>.com, <brand>hq.com, <brand>mail.co; never the company's own domain.
   ```bash
   oxygen domains check getacme.com tryacme.com acmehq.com acmemail.co --json
   ```
   Keep the ones with `registrable: true`; `registration_credits` is the price per year (in the audit a .com cost 1,250 and a .co 700).
   Tell the founder: "Cold email will go out from a separate domain like getacme.com so your main domain stays safe; it costs N credits a year."
2. Pick the sender (free). Reuse an id from `senders profiles list`, or create the person from the founder's answer. A photo is optional and cannot be added after the order; use only a file the founder gives you.
   ```bash
   oxygen senders profiles create --name "Ada Lovelace" --first-name Ada --last-name Lovelace --json
   oxygen senders profiles set-photo <sender_profile_id> --file ./photo.png --json
   ```
   Tell the founder: "The inboxes will send as Ada Lovelace, from ada@ and ada.lovelace@ on the new domain."
3. Get the exact quote (free: `--preview` buys and connects nothing, and needs no owner contact).
   ```bash
   oxygen managed-inboxes subscribe getacme.com --provider google --sender <sender_profile_id> --locals ada,ada.lovelace --preview --json
   ```
   Read back `quote_id`, `one_off_credits` (the domain, once), `total_monthly_credits` and `total_monthly_usd` (every month, warm-up included), `projected_monthly_shortfall` (above 0: the plan's monthly credits will not cover all running costs), `warmup_activation.mailboxes` and `senders[]`; say out loud any `avatar_durable: false` (that inbox ships without a photo).
   Tell the founder: "Two inboxes on getacme.com: N credits now, then M credits ($X) every month; warm-up starts by itself and nothing is sent."
> APPROVAL GATE — infra-purchase: show the domain (a separate one, not the company's own), the two addresses, the name and photo stamped on them for good, the one-off credits, the monthly credits that recur until cancelled, and that this approval also starts automatic warm-up for exactly those addresses for at least 14 days. Nothing is sent to anyone.
4. Place the order (charges the quote). `registrant.json` holds the owner's real contact; the registrar refuses placeholder data.
   ```bash
   echo '{"first_name":"Ada","last_name":"Lovelace","phone_cc":"1","phone":"<phone>","address_line_one":"<street>","city":"<city>","state":"<state>","postal_code":"<zip>","country":"US"}' > registrant.json
   oxygen managed-inboxes subscribe getacme.com --provider google --sender <sender_profile_id> --locals ada,ada.lovelace --billing ./registrant.json --approved --quote <quote_id> --json
   ```
   Tell the founder: "Ordered. The inboxes usually appear the same day and can send in 14 days."
5. Check it worked (free). The order turns active and warm-up shows `warming`; `oauth-health` lists only inboxes that cannot send yet, and a new address there with `consent_state: client_id_not_approved` is still being authorized by OXYGEN (usually minutes, nobody signs in). After 14 days, send with outbound-pilot-50.
   ```bash
   oxygen managed-inboxes get getacme.com --json
   oxygen mailboxes warmup status --json
   oxygen mailboxes oauth-health --json
   ```
   Tell the founder: "Your inboxes are warming up; from <date in 14 days> they can send your first campaign."

## If It Goes Wrong

- `domain_search_unavailable` from `domains search` → skip the search and check your own candidates with `domains check` (up to 20 in one call).
- `domain_not_available` on the quote → that domain is taken or banned; quote the next one from step 1.
- `sender_profile_incomplete` → the sender lacks a last name: `oxygen senders profiles update <id> --first-name <first> --last-name <last> --json`, after asking the founder.
- Your agent's safety layer refuses the quote → with `--preview` it buys and charges nothing; show the founder the command and ask them to allow it.
- `insufficient_credits` (402) on the order → top up at https://oxygen-agent.com/billing, then approve the same `quote_id`; `upgrade_required` → a paid plan first.
- `inbox_pricing_unsigned` (409) → that inbox type cannot be priced right now; nothing was ordered; try later or `--provider microsoft`.
- `warmup_activation` is null in the quote → warm-up is not included; stop and tell the founder before buying, because the new inboxes must not send cold email until they have warmed for 14 days.
- `executable: false` in the quote or `inboxkit_wallet_insufficient` (503) → OXYGEN's supplier is short and nothing was ordered; an order still `pending` after a day (its credits stay reserved) → contact OXYGEN support.
- A new address shows `consent_state: client_id_refused` in `oauth-health` → automatic authorization will not finish; follow that row's remedy, a one-time browser sign-in for that inbox.
