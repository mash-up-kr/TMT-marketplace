# meeting-minutes Canonical Spec

This file is the single source of truth for the skill. Stage files may describe procedure, but this spec owns names, accounts, gates, schemas, routing, and safety rules.

## Table of Contents

- Canonical flow
- Startup intake
- Confirmation gates
- People and Atlassian accounts
- Name normalization
- Meeting markdown schema
- DDK / OPS routing
- Jira creation contract
- Validation checklist
- Tool constraints

## Canonical Flow

1. Classify input as transcript or Confluence meeting page. (Audio recordings are out of scope — see SKILL.md; the user must transcribe externally first.)
2. Collect startup intake before any stage work.
3. Normalize names from the loaded transcript.
4. Produce meeting markdown using existing Confluence conventions when available.
5. Confirm action-item split and routing.
6. Confirm the full meeting markdown.
7. Fetch/create Confluence page as needed.
8. Parse action items, map accountIds, search duplicates, and present a Jira plan.
9. Create/link/skip Jira issues only after final confirmation.

## Startup Intake

Ask these three questions immediately after input classification and before Stage B/C.

| Key | Question | Default |
|---|---|---|
| `meeting_date` | 오늘 또는 이 회의 날짜가 몇일인가요? | If the transcript/page has date clues (mentioned dates, "next week", scheduled items), propose a date consistent with them; otherwise current system date. Pasted transcripts are often of past meetings, so do not assume today blindly. |
| `meeting_location` | 어디서 회의했나요? 예: Google Meet, Discord, 오프라인, Zoom | Infer a candidate from input only as a suggestion |
| `meeting_topic` | 회의 주제명은 무엇인가요? | Infer a candidate from filename/page title only as a suggestion |

Summarize before continuing:

```text
사전 정보 확인:
- 날짜: <meeting_date>
- 장소: <meeting_location>
- 주제: <meeting_topic>
```

Use these values in meeting markdown frontmatter, meeting title, Confluence title, Jira descriptions, and final summaries.

## Confirmation Gates

Use the best available confirmation surface. In Codex App, ask concise plain-text questions if structured input is unavailable.

| Gate | When | Required User Decision |
|---|---|---|
| Intake | Before stage execution | Date, location, topic |
| Name Review | After transcript load when names are uncertain | Name corrections and extra aliases |
| B-G1 | After action extraction | Split policy, project routing, owner/due-date uncertainty |
| B-G2 | Before Confluence/Jira | Full markdown approval; no summary-only approval |
| C-G1 | Before Jira writes | Create/link/skip plan, projectKey, assignee accountIds, watchers, Epic/link handling |

Never call `createJiraIssue`, `editJiraIssue`, `transitionJiraIssue`, `createIssueLink`, or `addCommentToJiraIssue` before C-G1 passes.

## People And Atlassian Accounts

The canonical people/account table and account rules live in `references/people.md` (volatile org data, kept separate so a teammate/accountId change does not touch policy). Read it whenever you need to resolve an owner, accountId, displayName, or alias. The rules below in this spec (gates, routing, Jira contract, validation) reference that table by role, not by copying it.

## Name Normalization

Normalize names after transcript load and before B-G2:

1. List detected names.
2. Map obvious aliases/STT errors to canonical names.
3. Show `raw -> canonical` corrections.
4. Leave low-confidence names as `확인 필요`.
5. Apply confirmed corrections consistently to the transcript text, meeting markdown, and Jira plan.

Do not normalize a new person into a known team member solely because the name is similar.

### Ambiguous tokens

Some short name tokens can match more than one member (for example, a shared given-name fragment). When a detected token could map to two or more canonical people, do not auto-assign it. Mark it `확인 필요` and ask the user, even if one mapping seems more likely. Silent disambiguation here causes wrong Jira assignees, which is expensive to undo.

### Attendee vs mention

The frontmatter `attendees` list must reflect who was actually in the meeting, not everyone whose name appears.

- A person who speaks in the transcript is an attendee.
- A person who is only referred to in the third person (e.g., "혜인이가 정리해준 것") is a mention, not necessarily an attendee.
- An explicit "오늘 없고 / 불참 / 못 왔다" marks an absentee.
- When attendance is unclear, mark the person `확인 필요` and confirm at the Name Review or B-G1 gate rather than guessing. Attendance is hard to infer from a transcript alone, so prefer asking.

## Meeting Markdown Schema

Required frontmatter:

```yaml
---
title: <meeting_date> <meeting_topic> 회의록
date: <meeting_date>
location: <meeting_location>
topic: <meeting_topic>
transcript: <path-or-empty>
attendees: [<canonical names>]
---
```

Required action table:

```markdown
## 🎯 액션 아이템

| # | 작업 | 프로젝트 후보 | 담당자 | 기한 | 상태 |
|---|---|---|---|---|---|
| 1 | ... | DDK/OPS/프로젝트 미정 | 이름 또는 (미정) | YYYY-MM-DD 또는 미정 | TODO/DONE/진행중 |
```

Keep source quotes/timestamps in the B-G1 review table, but remove source-only columns from final meeting markdown unless the existing Confluence convention requires them.

## DDK / OPS Routing

| Candidate | Use For |
|---|---|
| `DDK` | Product features, UX/UI, implementation, QA/verification, design/prototype, data/technical decisions, work that changes the product artifact |
| `OPS` | Operations, scheduling, meeting prep, documentation cleanup, communication, coordination, process management, work tracked as operations |
| `프로젝트 미정` | Ambiguous work; do not create Jira until user chooses DDK or OPS |

Routing is a candidate, not a final decision, until C-G1.

### Skip candidates (surface, do not silently create)

Not every line in a meeting is a Jira ticket. Flag these as skip/handle candidates at B-G1 and let the user decide, rather than minting tickets automatically:

- Vague homework with no single owner (e.g., "각자 고민해오기" assigned to everyone) — offer: one tracking ticket with a named owner, per-person tickets, or notes-only.
- Non-product/social items (e.g., team outing/MT logistics) — confirm whether they belong in Jira at all before routing to OPS.
- Pure discussion or TBD with no committed action — keep in the meeting doc, not Jira.

The goal is consistency: the user should be asked the same kinds of questions every run, not left to your ad-hoc judgment.

## Jira Creation Contract

For every Jira candidate, build a plan row before writes:

| Field | Rule |
|---|---|
| `projectKey` | `DDK` or `OPS` only after confirmation |
| `issueTypeName` | `작업` |
| `summary` | Use original action text; keep it concise |
| `assignee_account_id` | Required unless user explicitly approves unassigned |
| `parent` | Same-project parent only |
| `duedate` | ISO date or omit when unknown |
| `customfield_10147` | Required: `{"value": "L3"}` for action items |
| `description` | Include action, decision basis, meeting link, meeting location/topic, related Epic/source |

Cross-project rule:

- DDK issue under DDK Epic: use `parent` when confirmed.
- OPS issue related to DDK Epic: create OPS issue in OPS, then `createIssueLink` with `Relates`.

Duplicate rule:

- Search recent DDK/OPS issues by assignee before creating.
- Treat "본인 담당분 별도 과제", "이미 진행 중", "DONE", and similar notes as duplicate risk.
- Present duplicates in C-G1 and default to skip/link rather than duplicate creation.

Watcher rule:

- The default is no watchers. Add them only when the meeting names a non-assignee who must be kept in the loop (e.g., a reviewer, a pair owner, a lead who asked to be notified).
- Propose the watcher list explicitly at C-G1 with accountIds; never add watchers silently.
- Add watcher mentions via `addCommentToJiraIssue(contentFormat="adf")` using ADF mention `attrs.id=<accountId>`. If no watcher is warranted, say so in the final summary so the omission is visible, not forgotten.

## Validation Checklist

Before B-G2:

- Names are canonical or explicitly marked `확인 필요`.
- No action owner conflicts with source quote.
- Action table has required columns and valid values.
- `프로젝트 미정` rows are highlighted.
- DONE items are not counted as new ticket candidates.

Before C-G1:

- Every create candidate has `projectKey`, assignee accountId or approved unassigned state, due-date handling, duplicate handling, and parent/link strategy.
- OPS candidates are not assigned a DDK parent.
- Jira writes are not planned for `프로젝트 미정`.
- Watcher mentions use accountIds.

## Tool Constraints

Use the available Atlassian MCP tools by their actual names in this environment:

- Confluence: `searchConfluenceUsingCql`, `getConfluencePage`, `createConfluencePage`, `updateConfluencePage`, `createConfluenceFooterComment`
- Jira: `lookupJiraAccountId`, `searchJiraIssuesUsingJql`, `getJiraIssue`, `createJiraIssue`, `editJiraIssue`, `addCommentToJiraIssue`, `createIssueLink`, `transitionJiraIssue`, `getTransitionsForJiraIssue`

If a space ID cannot be discovered from a provided page or known option, ask the user for the Confluence space/parent instead of inventing one.
