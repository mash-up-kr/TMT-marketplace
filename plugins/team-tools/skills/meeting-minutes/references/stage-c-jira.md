# Stage C - 회의 마크다운 → Confluence 및 Jira (Meeting Markdown To Confluence And Jira)

Mode B/C에 사용하세요. `references/spec.md`를 먼저 읽으세요; 계정 매핑, DDK/OPS 라우팅, Jira 필드, 쓰기 게이트를 소유합니다.

## 단계 (Steps)

1. 회의 마크다운 확보:
   - Mode B: 승인된 Stage B 마크다운 사용.
   - Mode C: 제공된 Confluence 페이지를 `getConfluencePage(contentFormat=markdown)`로 가져옴.
2. Mode B가 게시를 요구하면:
   - `createConfluencePage` 사용.
   - 제목: `<meeting_date> <meeting_topic> 회의록`.
   - 본문: frontmatter를 제거한 승인된 마크다운.
   - `spaceId`/parent가 불명이면 사용자에게 물음. space ID를 임의로 만들지 말 것.
3. spec가 요구하는 액션 표를 파싱.
4. 담당자 정규화:
   - `references/people.md`의 accountId 선호.
   - 불명 담당자에만 `lookupJiraAccountId(searchString=<name-or-alias>)` 사용.
   - C-G1이 해결하기 전까지 미해결 담당자를 생성 후보에서 제외.
5. 쓰기 전에 중복 위험 검색:
   - 최근 DDK/OPS 이슈를 assignee로 `searchJiraIssuesUsingJql`.
   - 노트가 "본인 담당분", "직접 운영", "이미 진행", 또는 DONE을 언급하면 가능성 있는 reporter/추적 이슈도 검색.
6. C-G1용 Jira 계획 표 작성:

```markdown
| # | 작업 | projectKey | assignee | accountId | due | duplicate/link plan | parent/link plan | create? |
|---|---|---|---|---|---|---|---|---|
```

7. C-G1 실행:
   - 모든 행에 대해 생성/링크/스킵 확인.
   - DDK/OPS 라우팅 확인.
   - assignee accountId와 watcher accountId 확인.
   - DDK Epic 또는 OPS parent/링크 전략 확인.
8. C-G1 통과 후 Jira 이슈 생성:
   - `createJiraIssue`를 `projectKey`, `issueTypeName: "작업"`, `assignee_account_id`, `contentFormat: "markdown"`, `additional_fields.customfield_10147: {"value": "L3"}`와 함께 사용.
   - 동일 프로젝트 `parent`만 사용.
   - DDK Epic과 관련된 OPS는 OPS 이슈를 먼저 생성한 뒤 `createIssueLink(type="Relates")` 사용.
9. watcher/소스 코멘트를 `addCommentToJiraIssue(contentFormat="adf")`와 ADF 멘션 id로 추가.
10. C-G1에서 명시적으로 승인된 경우에만 소스/추적 이슈 업데이트.

## 출력 계약 (Output Contract)

보고:

- 생성되거나 사용된 Confluence 페이지 URL.
- 신규 Jira 이슈.
- 기존 링크된 이슈.
- 스킵된 DONE/중복/미해결 항목.
- 후속 확인, 특히 watcher 등록과 미해결 담당자.
