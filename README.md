# The LinkedIn agent skill

Eleven Claude skills for writing and planning LinkedIn content. Free, MIT,
no signup, no API key, nothing to connect.

One of them writes your posts off 21 hook formulas. One comments on other
people's posts. One handles the replies under yours. One scores your profile
out of 100 and rewrites what lost points. One plans the week: what to post,
when, and who to engage with.

And one is the voice editor. `/li-human` helps simplify jargon, cut repetition,
and follow your own writing and punctuation preferences. You get revised copy
and a short explanation of the edits, with your meaning and attribution intact.

**Nothing gets posted until you say yes.** These skills write. You post.

## Install in Claude Code

These instructions install commands in **Claude Code**, in the environment
where it runs. Pasting the repo URL into a regular Claude chat does not install
files into your computer's `~/.claude/skills/` or register `/li-post` there.
A chat sandbox is separate from your local Claude Code installation.

Paste this into a Claude Code session with filesystem and network access:

```
https://github.com/Jakeschincariol/linkedin-agent-skill

Install the skills into ~/.claude/skills/ in this Claude Code environment.
Report any access or download errors; do not claim success without checking
that li-post/SKILL.md and li-post/hooks.json were installed.
```

Or run these commands in your terminal (Git required):

```bash
git clone https://github.com/Jakeschincariol/linkedin-agent-skill.git
mkdir -p ~/.claude/skills
cp -r linkedin-agent-skill/skills/li-* ~/.claude/skills/
```

Open a fresh Claude Code session in that environment. Type `/li-post` and
check that it appears in the command menu, then invoke it with your own idea.
A request for your writing samples is normal on first use. The optional
`/li-human` helper script needs Python 3. See [Claude Code skills documentation](https://code.claude.com/docs/en/skills).

Or run these commands inside Claude Code to install as a plugin:

```
/plugin marketplace add Jakeschincariol/linkedin-agent-skill
/plugin install linkedin-agent
```

Plugin skills use a namespace: invoke `/linkedin-agent:li-post` after installation.
Project-local instead of global: copy the same folders into your repo's
`.claude/skills/` and open Claude Code in that project.

### Using a regular Claude chat

For a one-off drafting workflow, open the files on GitHub yourself and paste
or upload `skills/li-post/SKILL.md`, `skills/li-post/hooks.json`, and your writing
samples. Ask Claude to follow those instructions using the supplied files.
This does not register a slash command or install the full workflow. Local
voice/log files and Python tools are unavailable unless that chat environment
explicitly provides them. `/li-human` can edit directly without Python; its
optional local helper adds wording suggestions. Do not claim the helper ran
or invent its report. If GitHub fetching is blocked, supply the files directly
instead of retrying the install prompt.

### Set your voice in Claude Code

Then spend ten minutes on `templates/voice.md`. Copy it to
`~/.claude/linkedin/voice.md` and fill it in, or paste three of your own posts
into Claude and say "write my voice.md from these". Every skill reads that
file. Skip it and everything comes out sounding like everyone else.

## The eleven

| command | what it does |
| --- | --- |
| `/li-post` | One idea into a post. Three hook options from [21 formulas](skills/li-post/hooks.json), one full draft, edited for your voice before you see it. |
| `/li-comment` | Comments on other people's posts. Nine types, picked by what the post actually is. Never "Great post!". |
| `/li-reply` | The thread under your own post. Sorts every comment into lead / substance / peer / support / noise, then writes in that order. |
| `/li-profile` | Scores your profile against a [12-part rubric](skills/li-profile/rubric.json) out of 100, then rewrites in fix-first order. |
| `/li-plan` | The week. What to post, when to post it, and the 10 people to engage with. Writes `~/.claude/linkedin/plan.md`. |
| `/li-human` | Voice and clarity editing, with an optional local wording review. See below. |
| `/li-carousel` | Document posts. Slide-by-slide copy, the cover that earns the swipe, and the PDF to upload. |
| `/li-repurpose` | One video, newsletter or transcript into a week of posts that each stand alone. |
| `/li-dm` | The 200-character invite note, the first message, and the two follow-ups. Two. |
| `/li-inbox` | Triages the inbox into lead / recruiter / peer / ask / spam, and tells you which tell gave the sequence away. |
| `/li-audit` | Post-mortem on what you have already published. Ranks by engagement rate and reach multiple, not impressions. |

## The voice editor

`/li-human` keeps its existing command name. It edits for clarity, concision,
and your voice using your preferences and writing examples. It preserves
facts, quotations, links, attribution, and AI-use disclosures. It does not
assess authorship, optimize detector results, or remove watermarks/provenance.

The optional Python helper runs locally with no dependencies or uploads:

```bash
# Run from skills/li-human, using your own draft path.
python3 humanize.py "draft.txt" --report
python3 humanize.py "draft.txt" --json
python3 humanize.py "draft.txt" --plain-typography -o "preview.txt" --report
```

By default, the helper returns your draft unchanged and suggests simpler words
or structures to review. The editor decides which suggestions fit the context.
Technical terms, distinctive phrasing, and useful three-item lists can stay.
The editable lexicon is [`slop.json`](skills/li-human/slop.json).

`--plain-typography` optionally converts long dashes, curly quotes, and ellipses
to plain punctuation. Review the preview for grammar, especially sentence
boundaries. URLs and email addresses are preserved. Unicode format characters,
non-breaking spaces, language-specific characters, and emoji are preserved too.
An output path must be a new file so the original and earlier previews survive.

A typical editorial note is: "Shortened the opening, replaced one vague phrase,
and followed your punctuation preference. Facts and attribution retained."
There is no numerical score or pass/fail verdict. The skill finishes when the
copy communicates the intended point in your voice.

### Updating from v1

This is v2.0.0 because the helper's behavior and report format have changed.
`/li-human` and `humanize.py` keep their names. `detect.py` has been removed.
The helper's JSON remains `{text, report}`, with `typographic`, `wording`, and
`structures` lists in the report. Wording suggestions are no longer applied
automatically; plain punctuation requires `--plain-typography`. Exit status 0
means the review completed, including when suggestions remain.

For manual installs, replace the entire installed `li-human` directory with
this version and update the other skill files. Copying files over an existing
directory leaves deleted files such as the old `detect.py` behind. Preserve
any custom lexicon outside the installed skill first, then migrate only its
wording and structure suggestions. Do not carry over the old skill instructions
or character-removal rules. Plugin users should update/reinstall the plugin
and verify the installed `li-human` directory no longer includes `detect.py`.

## The fine print, which is the honest part

**These skills do not post to LinkedIn, and they should not.** There is no
official API for posting to a personal profile without an approved partner
app, and automating the site with a browser or a third-party tool violates
[LinkedIn's User Agreement](https://www.linkedin.com/legal/user-agreement) and
gets accounts restricted. So every skill here ends the same way: a copy-ready
block, and you paste it. That is not a limitation bolted on afterwards, it is
the design. It is also why the approval gate is real rather than a setting.

**Nothing here fabricates.** No invented metrics, clients or outcomes go under
your name. If a draft needs a number you have not given, it comes back with
`{{your number}}` in it and a flag, every time.

## Files

```
skills/li-post/hooks.json        21 hook formulas: template, example, what it is for, how it gets ruined
skills/li-human/slop.json        optional wording and structure suggestions
skills/li-human/humanize.py      local editorial review and optional plain punctuation
skills/li-profile/rubric.json    the 100-point profile score
templates/voice.md               your voice profile. Fill this in first.
```

## Credit

Made by Jake Schincariol, [opusjake.ai](https://opusjake.ai).
The full write-up is at [opusjake.ai/r/linkedin-agent](https://opusjake.ai/r/linkedin-agent).

## License

MIT. Take it, change it, ship it.