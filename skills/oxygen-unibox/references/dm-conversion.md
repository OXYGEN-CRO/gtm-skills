# LinkedIn DM conversion: first message, replies and the second message

Write in the workspace voice: `oxygen context canonical get --type voice --json`. When `present` is false, say so before drafting instead of inventing a voice.

## First message (Sequence copy)

- A greeting, then one question. 100–250 characters. No pitch, no link, no product mention, no call ask.
- Never mention that they viewed the profile.
- A commenter: name their actual comment, then ask about the problem it touches. A reaction alone gives no personal hook; do not invent one.
- A researched contact: one dated current fact about their company, then a question that names their ICP or a tool the offer replaces. The tool goes into the question, with no commentary line before it.
- Someone who asked for a resource: deliver it first and never make qualification a condition. OXYGEN has no native bulk delivery to post commenters yet; tell the user rather than scripting raw sends.

## Who needs an answer

`oxygen inbox list --channel linkedin --unanswered --json` lists candidates. Reread each with `oxygen inbox get <conversation> --json` and drop it when the latest message is outbound or the order is unclear. Buyers first, oldest first; a buyer gets an answer the same day.

## Route the reply

| Thread | Reply |
| --- | --- |
| Qualified buyer: passes the rubric and names a concrete need | One line showing you understood their answer, then a concrete low-effort offer and the calendar link, asked as a question |
| Unknown or weaker fit | Answer, then the offer's lowest-effort next step |
| Agency, freelancer or partner who will not buy | One friendly closing line |
| Pitching the user; a thanks, "done" or "will check it out" | No reply |
| Resource request | The link, then one question about their work |

Unknown is not qualified: a large employer or senior title alone earns no call link. Someone ready to buy gets the direct next step, not a call the offer doesn't need.

## Draft rules

- Usually under 240 characters in 1–4 short paragraphs; links on their own line; no sign-off; no em dashes; one next step at most.
- Rewrite from the thread: the inbox's suggested reply is a generic follow-up question that never offers anything.
- Their last message over 3 days old: own the delay in a few words, worded differently across a batch.
- Show each draft in a code block beside the thread link and route.
- Reread the thread before presenting and before sending; a new message voids the draft. Recommended default (Auto-approve can skip it; say so): send only the exact text the user approved, through SKILL.md, Triage loop step 5.
- An edited or rejected draft becomes a proposed general rule for the workspace voice (`oxygen-knowledge` skill), never names or message text.

## Anti-patterns in replies

The default call or demo closer ("walk you through it", "a quick demo this week", "dive deeper", "hop on a quick call", "book a time whenever you're ready"); "how we help teams like yours scale"; an estimate that needs a call; offers of more content; status, booking link and product trial in one social reply; product layers listed for a signup; numbered steps with no question; numbers the user never stated; breezy closers; the same stock closing question or apology on every draft; feature lines where a question about their setup would move a buyer; a summary of a linked page; any answer to a message that needs none. A booking link is right when they asked for a call or one is already being arranged.
