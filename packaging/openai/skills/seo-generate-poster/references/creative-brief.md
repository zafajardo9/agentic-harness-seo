# Creative brief: extraction sheet and approval card

Use these templates between choosing a profile and creating anything in Canva.
The extraction sheet records what the user supplied. The final brief is
the exact poster specification the user approves. Fill both in the user's
language and keep them short enough to review on a phone.

## Source labels

Tag every extracted item with where it came from so the user can see what
is grounded and what is a suggestion.

| Label | Meaning |
|---|---|
| `user` | Stated by the user in this chat |
| `source` | Taken from a document, page, image, or post the user supplied; name it |
| `profile` | Inherited from the selected creative profile |
| `suggested` | Proposed by you; needs the user's agreement |

Only `user`, `source`, and `profile` items may appear in the approved brief
as fact. A `suggested` item becomes approved when the user accepts the brief
that contains it. Never upgrade a guess to `source`.

## Extraction sheet

Read the whole brief and every supplied material before filling this in.
Quote figures, dates, names, prices, and citations exactly as supplied.
Leave a row out when nothing supports it rather than inventing content.

```markdown
### What I took from your brief

**Goal:** <what the post must achieve> (`user`)
**Audience:** <who it is for> (`user` / `profile`)
**Key message:** <the one idea a reader should remember> (`user` / `suggested`)

**Facts and data**
- <exact figure, date, name, price, or rule> (`source`: <file, page, or URL>)
- <...>

**Tone:** <three or four adjectives and a sample sentence in that voice> (`profile` + `user` cues)
**Language:** <English, Filipino, Taglish, other> (`user` / `profile`)
**Ideas and angles you mentioned:** <layouts, metaphors, references, past posts>
**Must include:** <logo, handle, disclaimer, citation, hashtag>
**Must avoid:** <claims, words, imagery, competitor names>
**Call to action:** <approved wording, or "none approved yet">

**Gaps:** <missing facts that affect accuracy, such as an event date>
**Conflicts:** <brief vs. profile, or source vs. user, with both values>
```

Raise every gap and conflict in the questions that follow. Resolve a
conflict by asking. Do not pick a side silently.

## Layout and format ideas

Show the ideas after the extraction sheet. Draw each wireframe in a fenced
text block, top to bottom in reading order, using the real extracted copy or
a short label for it. Keep each wireframe to about ten lines.

````markdown
### Layout and format ideas

**Idea A: <name>** (recommended) · <format>, <width × height>
```text
+---------------------------+
| [logo]                    |
| HEADLINE: "<headline>"    |
| [photo: <subject>] | fact |
| 1. <step>  2. <step>      |
| [CTA pill: "<CTA>"]       |
+---------------------------+
```
Why: <fits the content amount, goal, and channel>

**Idea B: <name>** · Carousel, <n> slides, <width × height>
Slide 1 <hook> · Slides 2-<n-1> <one point each> · Slide <n> <CTA and contact>
Why: <...>

**Idea C: <name>** · <format>
<wireframe>
Why: <...>

Pick A, B, or C, combine parts (for example "A's layout with B's carousel"),
or ask for different ideas.
````

Make the ideas genuinely different: change the format, the focal point, or
the structure (list, grid, photo-led, stat-led, question-led), not just
colors. Use layouts from the profile first and label any new layout
`suggested`. Put every extracted fact the user wants on the poster into each
wireframe, or say where it goes instead, such as in the caption or a later
slide.

## Final brief for approval

Present this after the creative settings are answered. It is the single
source of truth for the Canva request. Write the copy verbatim, exactly as it
should appear on the poster.

```markdown
### Final poster brief: <short title> · v<n>

**Profile:** <profile name> · **Channel and size:** <channel>, <width × height>
**Layout:** <chosen idea, focal point, reading order>, followed by its
wireframe (one per slide for a carousel)
**Palette:** <role: hex> for each color used
**Typography:** Heading <font>, body <font> (<fallback if substituted>)
**Imagery:** <photo / illustration / icons / supplied asset / text only>, <subject>

**Poster copy**
- Headline: "<exact text>"
- Supporting copy: "<exact text>"
- Details: "<date, place, price, citation, exactly as approved>"
- Call to action: "<exact text>" or none
- Footer: "<handle, contact, or lockup>"

**Tone:** <adjectives>
**Must avoid:** <list>
**Facts used:** <each fact with its source label>
**Open items:** none (or list what still blocks approval)

**Canva request:** <the prompt text that will be sent, in full>

Reply **Approve** to create the Canva draft, or tell me what to change.
```

## Approval rules

- Create nothing in Canva until the user approves the latest version of the
  final brief. Approval of an earlier version or of the creative settings
  alone does not count.
- Clear approvals include "Approve", "Approved", "Looks good, go", or
  "Generate it". A question, a partial reaction, or silence is not approval.
- When the user changes anything, apply it, increment the version, and
  show the updated brief with the changed lines marked **(changed)**. Ask for
  approval again.
- If the Canva request must change after approval (for example, the exact
  size is unsupported), stop, explain the change, and ask for approval again.
- Send the Canva request exactly as approved. Do not add copy, claims,
  contact details, or calls to action that are absent from the brief.

## After generation

- Check the returned draft against the approved brief where the connector
  exposes its content or preview: headline, copy, details, and call to
  action. Report any text Canva changed, dropped, or added, and offer a
  revision that restores the approved wording.
- Offer to save new preferences from this brief, such as a new call to
  action or layout, to the profile through `setup`. Save nothing to the
  profile without the user's agreement.
