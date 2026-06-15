# Stage C - 회의 마크다운 → Confluence 및 Jira (Meeting Markdown To Confluence And Jira)

Mode B/C에 사용하세요. `references/spec.md`를 먼저 읽으세요; 계정 매핑, DDK/OPS 라우팅, Jira 필드, 쓰기 게이트를 소유합니다.

## 단계 (Steps)

1. 회의 마크다운 확보:
   - Mode B: 승인된 Stage B 마크다운 사용.
   - Mode C: 제공된 Confluence 페이지를 `mcp__atlassian__confluence_get_page(page_id=<id>)`로 가져옴(sooperset는 기본 markdown 변환).
2. Mode B가 게시를 요구하면:
   - `mcp__atlassian__confluence_create_page(space_key=<KEY>, title=, parent_id=<부모 페이지 ID>, content_format="markdown", content=)` 사용.
   - 제목: `<meeting_date> <meeting_topic> 회의록`.
   - 본문: frontmatter를 제거한 승인된 마크다운.
   - `space_key`/parent가 불명이면 사용자에게 물음. space/parent를 임의로 만들지 말 것.
3. spec가 요구하는 액션 표를 파싱.
4. 담당자 정규화:
   - `references/people.md`의 **accountId**를 assignee로 사용(전환 전과 동일). sooperset `assignee`는 accountId를 받습니다.
   - watcher도 같은 표의 accountId를 사용(아래 9번 `jira_add_watcher`).
   - 표에 없는 담당자는 임의 조회·추측 금지 — C-G1에서 사용자에게 확인하고, 해결 전까지 생성 후보에서 제외.
5. 쓰기 전에 중복 위험 검색:
   - 최근 DDK/OPS 이슈를 assignee로 `mcp__atlassian__jira_search`.
   - 노트가 "본인 담당분", "직접 운영", "이미 진행", 또는 DONE을 언급하면 가능성 있는 reporter/추적 이슈도 검색.
6. C-G1용 Jira 계획 표 작성:

```markdown
| # | 작업 | project_key | assignee accountId | watcher accountId | due | duplicate/link plan | parent/link plan | create? |
|---|---|---|---|---|---|---|---|---|
```

7. C-G1 실행:
   - 모든 행에 대해 생성/링크/스킵 확인.
   - DDK/OPS 라우팅 확인.
   - assignee accountId와 watcher accountId 확인.
   - DDK Epic 또는 OPS parent/링크 전략 확인.
8. C-G1 통과 후 Jira 이슈 생성:
   - `mcp__atlassian__jira_create_issue`를 `project_key`, `issue_type: "작업"`, `assignee: <accountId>`, `description: <markdown>`, `additional_fields: {"customfield_10147": {"value": "L3"}}`와 함께 사용.
   - 동일 프로젝트 parent는 `additional_fields.parent: "<상위 키>"`(문자열)로 지정.
   - DDK Epic과 관련된 OPS는 OPS 이슈를 먼저 생성한 뒤 `mcp__atlassian__jira_create_issue_link(link_type="관련된 이슈", inward_issue_key=, outward_issue_key=)` 사용.
9. watcher는 `mcp__atlassian__jira_add_watcher(issue_key=, user_identifier=<accountId>)`로 추가. 소스/맥락 코멘트가 필요하면 `mcp__atlassian__jira_add_comment(issue_key=, body=<markdown>)`로 추가.
10. C-G1에서 명시적으로 승인된 경우에만 소스/추적 이슈 업데이트.

## 출력 계약 (Output Contract)

보고:

- 생성되거나 사용된 Confluence 페이지 URL.
- 신규 Jira 이슈.
- 기존 링크된 이슈.
- 스킵된 DONE/중복/미해결 항목.
- 후속 확인, 특히 watcher 등록과 미해결 담당자.
