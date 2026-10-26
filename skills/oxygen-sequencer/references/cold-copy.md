# Cold email copy

Copy rules shared by the email plays in `plays/`. Spintax and A/B rounds belong to the whole-market play only.

## First email

At most 75 words; aim for under 50. In the largest cold email dataset on file, first emails under 50 words earned the most replies and 100–149 words the fewest.

Four lines:

```text
Hi {{first_name|there}},
{{icebreaker}}
<pitch: one sentence, the same for every lead in the segment>
{{idea}} <CTA>
```

- `{{icebreaker}}` is one AI column that stops at the first source that fits: a post of theirs from the last 14 days, then a case study or a named client, then what the company does. The prompt sees only the row's columns, so the row needs a recent-posts column first.
- `{{idea}}` is one AI column: one concrete thing your product would do for this company, specific enough to say yes to.
- The pitch line is the same for every lead of a Sequence; only its A/B round changes it.

## Follow-ups

At most 40 words each, with no `subject_template`.

## Call to action

Ask for a reply that gets them something concrete and free, for example "Let me know if I should send over <a personalised plan>." or "Want me to map the first 3 <plays> for {{company_name}}? Just reply yes." Never ask for a meeting or send a calendar link in the first email.

## Signal leads

Write the pain the signal implies and never name the signal: "saw you visited our site", "congrats on the funding" and "saw your comment on X's post" are out. A per-lead signal line, generated from the signal's evidence columns, replaces `{{icebreaker}}`.
