# 인물 및 Atlassian 계정 (People And Atlassian Accounts)

팀의 휘발성 조직 데이터입니다. 팀원, accountId, displayName, 또는 별칭이 바뀌면 (`spec.md`가 아니라) 이 파일을 수정하세요. `spec.md`는 이 표를 사용하는 정책을 소유하고, 이 파일은 데이터를 소유합니다.

| 이름 | Atlassian displayName | Jira accountId | 별칭 / 흔한 STT 오류 |
|---|---|---|---|
| 이창우 | changchangwoo119 | `712020:69ebe92d-f78e-4b83-9c45-639435e36b74` | 창후, 창호, 창우 형, 창호영 |
| 이준표 | Dradnats | `712020:cdb6b0e7-8a68-4e9d-9d79-511f92898ad6` | 준표, 준포, dradnats |
| 이서원 | 이서원 | `712020:04061ce9-2704-419e-bbb9-b8f8d7512f8f` | 서원, 서원님 |
| 하아얀 | 하아얀 | `712020:19ac4adb-ae00-41f7-810b-3bea326a0172` | 아연, 아얀, 하얀, 하아얀 언니 |
| 장정우 | 장정우 | `712020:7a4a319d-e043-4edc-8378-e0e5353c8717` | 정우, 장정후 |
| 임준형 | 임준형 | `712020:aaabb651-1817-46ef-96b5-e759b841fad5` | 준형, 임준영 |
| 정혜인 | hyein396 | `712020:c165ade4-ad82-416f-b24e-8d96ebd3e732` | 혜인, 해인, hyein396 |
| 장민서 | Minseo Jang | `712020:eba24041-39c7-46a8-a960-7581cb007de3` | 민서, minseo, minseo jang |

## 계정 규칙 (Account rules)

> 서버: 이 스킬은 sooperset `mcp-atlassian`을 전제로 합니다(`jira-creator`와 동일). assignee·watcher 모두 accountId를 씁니다(공식 MCP 전환 전과 동일한 식별자).

- 새 조회보다 표의 값을 선호(불필요한 lookup 회피).
- **Jira assignee에는 `accountId`를 넣기** (`jira_create_issue(assignee=<accountId>)`). sooperset assignee는 accountId/displayName/email을 모두 받지만, 전환 전과 동일하게 accountId 사용.
- **Watcher에는 `accountId`를 사용** (`jira_add_watcher(user_identifier=<accountId>)`, Cloud 기준).
- 담당자가 표에 없거나 매칭이 모호하면 Jira 생성 전에 사용자에게 묻기(임의 조회·추측 금지).
- 둘 이상의 행과 매칭될 수 있는 별칭(공유된 이름 일부)은 자동 할당 금지 — `spec.md` 이름 정규화 → 모호한 토큰 참고.
