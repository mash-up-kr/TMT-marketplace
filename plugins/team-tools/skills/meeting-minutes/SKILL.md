---
name: meeting-minutes
description: Convert meeting transcripts or existing Confluence meeting notes into corrected minutes and Jira action tickets for ttalkkak.atlassian.net. Use when the user asks to draft/publish meeting notes, split action items into DDK/OPS Jira tickets, map Korean team member names to Atlassian accounts, detect duplicate Jira work, add watcher mentions, or process an existing Confluence action-item table. Do not use for audio transcription/STT (transcribe externally first, then pass the transcript), single manual Jira tickets, or Linear/GitHub issue workflows.
---

# meeting-minutes

Run the meeting pipeline with one canonical source of truth:

1. Read `references/spec.md` first.
2. Detect input mode.
3. Ask the startup intake questions from the spec.
4. Load only the stage reference needed for the detected mode.
5. Stop at each confirmation gate before creating or updating external Jira/Confluence state.

## Input Modes

| Mode | Input | Load |
|---|---|---|
| B | Transcript `.txt`, pasted transcript text, or `transcripts_*/` directory | `references/stage-b-meeting-doc.md` -> `references/stage-c-jira.md` |
| C | Confluence page ID, tiny link, or URL | `references/stage-c-jira.md` |

Audio recordings are out of scope for this skill. If the input is an audio/video file, do not transcribe it here — ask the user to transcribe it externally (any STT tool, or export a VTT/transcript) and re-run with the resulting transcript as Mode B.

Supported options: `--epic DDK-9`, `--team-lead <name>`, `--space <KEY or spaceId>`.

## Non-Negotiables

These are reminders of what to watch for. The binding detail lives once in `references/spec.md` and `references/people.md` — do not rely on a paraphrase here over the canonical text, and do not restate rule specifics in this file (it causes drift).

- `references/spec.md` is canonical. If a stage file conflicts with it, follow the spec.
- Meeting notes are the only source of truth for owners, due dates, decisions, and action text — never invent facts.
- Never write to Jira/Confluence before the matching confirmation gate passes (spec.md → Confirmation Gates).
- The create/skip rules (`프로젝트 미정`, unknown owner, missing accountId, DONE, duplicates), the account-field and mention rules, and the OPS-vs-DDK-Epic cross-project rule are each defined once in spec.md / people.md — apply them from there.

## Stage Outputs

- Stage B: local meeting markdown under `~/Desktop/meetings/<YYYY-MM-DD>/`.
- Stage C: Confluence page URL plus created/linked/skipped Jira issue summary.

## Resources

- `references/spec.md` - canonical intake fields, gates, schemas, DDK/OPS routing, name normalization, validation rules, and Atlassian constraints.
- `references/people.md` - canonical people/account table (names, accountIds, displayNames, aliases) and account rules. Edit this when the team changes.
- `references/stage-b-meeting-doc.md` - transcript to meeting markdown.
- `references/stage-c-jira.md` - meeting markdown to Confluence/Jira.
