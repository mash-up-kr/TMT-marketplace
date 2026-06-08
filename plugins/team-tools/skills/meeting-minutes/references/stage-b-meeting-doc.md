# Stage B - Transcript To Meeting Markdown

Use this for Mode B. Read `references/spec.md` first; it owns the schema, routing, and gates. The people/account table lives in `references/people.md`.

## Steps

1. Load the transcript text. If the transcript includes timestamps (e.g. `.srt`/`.vtt`/`.json`), use them for decision/action evidence.
2. Learn existing Confluence meeting-note conventions before drafting:
   - Use `searchConfluenceUsingCql` with a small query such as `title ~ "회의록" OR title ~ "meeting" OR label = "meeting-minutes"`.
   - Fetch the top 3-5 relevant pages with `getConfluencePage(contentFormat=markdown)`.
   - Extract title pattern, recurring sections, action table columns, decision table format, mention style, timestamp style, and labels.
   - If no pages are available, use the schema in `spec.md`.
   - When conventions exist, draft the local markdown in that richer shape from the start (e.g., 요약본 / 결정사항 / TBD / 액션아이템 / 논의 흐름 / 다음 회의). The team convention wins over the minimal `spec.md` schema. This keeps the local file and the published page aligned and avoids re-writing the whole doc at publish time. Treat the local markdown as an intermediate artifact whose final shape mirrors what will be published.
   - Do this convention check even when the user says "just write the minutes" — learning the format first is cheaper than reformatting later.
3. Draft meeting markdown:
   - Use `meeting_date`, `meeting_location`, and `meeting_topic` from startup intake.
   - Use canonical names (spec.md name normalization) and account-safe owners from `references/people.md`.
   - Keep decisions and actions grounded in transcript evidence.
4. Extract action items into the B-G1 review table:

```markdown
| # | 작업 | 프로젝트 후보 | 담당자 | 기한 | 상태 | 출처 발화 |
|---|---|---|---|---|---|---|
```

5. Run B-G1:
   - Confirm split policy: one ticket per action, topic bundle, owner bundle, or user-specified.
   - Confirm project candidates: keep, row-by-row edit, all DDK, all OPS, or defer unresolved rows.
   - Confirm multi-owner, unknown-owner, due-date, DONE, and duplicate-risk handling.
6. Build final meeting markdown using the required schema from `spec.md`.
7. Validate before B-G2 using the spec checklist.
8. Save to `~/Desktop/meetings/<meeting_date>/<safe-topic-or-basename>.md`.
9. Run B-G2:
   - Show the full markdown body, not a summary.
   - Show validation results for names, owners, project candidates, table shape, DONE items, and duplicate-risk notes.
   - Ask whether to publish to Confluence/Jira, revise, save only, or stop.

## Output Contract

Return the local markdown path and the B-G2 decision. Continue to Stage C only when the user approves Confluence/Jira progression.
