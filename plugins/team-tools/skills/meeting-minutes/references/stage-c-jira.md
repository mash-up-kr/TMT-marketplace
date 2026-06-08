# Stage C - Meeting Markdown To Confluence And Jira

Use this for Mode B/C. Read `references/spec.md` first; it owns account mapping, DDK/OPS routing, Jira fields, and write gates.

## Steps

1. Acquire meeting markdown:
   - Mode B: use the approved Stage B markdown.
   - Mode C: fetch the provided Confluence page with `getConfluencePage(contentFormat=markdown)`.
2. If Mode B requires publishing:
   - Use `createConfluencePage`.
   - Title: `<meeting_date> <meeting_topic> 회의록`.
   - Body: approved markdown with frontmatter removed.
   - If `spaceId`/parent is unknown, ask the user. Do not invent a space ID.
3. Parse the action table required by the spec.
4. Normalize owners:
   - Prefer accountIds from `references/people.md`.
   - Use `lookupJiraAccountId(searchString=<name-or-alias>)` only for unknown owners.
   - Exclude unresolved owners from create candidates until C-G1 resolves them.
5. Search duplicate risk before writes:
   - `searchJiraIssuesUsingJql` for recent DDK/OPS issues by assignee.
   - Also search likely reporter/tracking issues when notes mention "본인 담당분", "직접 운영", "이미 진행", or DONE.
6. Build a Jira plan table for C-G1:

```markdown
| # | 작업 | projectKey | assignee | accountId | due | duplicate/link plan | parent/link plan | create? |
|---|---|---|---|---|---|---|---|---|
```

7. Run C-G1:
   - Confirm create/link/skip for every row.
   - Confirm DDK/OPS routing.
   - Confirm assignee accountIds and watcher accountIds.
   - Confirm DDK Epic or OPS parent/link strategy.
8. After C-G1 passes, create Jira issues:
   - Use `createJiraIssue` with `projectKey`, `issueTypeName: "작업"`, `assignee_account_id`, `contentFormat: "markdown"`, and `additional_fields.customfield_10147: {"value": "L3"}`.
   - Use same-project `parent` only.
   - For OPS related to a DDK Epic, create the OPS issue first, then use `createIssueLink(type="Relates")`.
9. Add watcher/source comments with `addCommentToJiraIssue(contentFormat="adf")` and ADF mention ids.
10. Update source/tracking issue only if explicitly approved in C-G1.

## Output Contract

Report:

- Confluence page URL when created or used.
- New Jira issues.
- Existing linked issues.
- Skipped DONE/duplicate/unresolved items.
- Follow-up checks, especially watcher registration and unresolved owners.
