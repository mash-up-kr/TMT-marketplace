# meeting-minutes 정식 스펙 (Canonical Spec)

이 파일은 스킬의 단일 진실원입니다. Stage 파일은 절차를 기술할 수 있지만, 이 스펙이 이름·계정·게이트·스키마·라우팅·안전 규칙을 소유합니다.

## 목차

- 정식 흐름(Canonical flow)
- 시작 인테이크(Startup intake)
- 확인 게이트(Confirmation gates)
- 인물 및 Atlassian 계정
- 이름 정규화
- 회의 마크다운 스키마
- DDK / OPS 라우팅
- Jira 생성 계약
- 검증 체크리스트
- 툴 제약

## 정식 흐름 (Canonical Flow)

1. 입력을 대본 또는 Confluence 회의 페이지로 분류. (오디오 녹음은 범위 밖 — SKILL.md 참고; 사용자가 먼저 외부에서 전사해야 함.)
2. 어떤 stage 작업보다 먼저 시작 인테이크 수집.
3. 로드된 대본에서 이름 정규화.
4. 가능하면 기존 Confluence 컨벤션을 사용해 회의 마크다운 생성.
5. 액션 아이템 분리와 라우팅 확인.
6. 전체 회의 마크다운 확인.
7. 필요에 따라 Confluence 페이지 가져오기/생성.
8. 액션 아이템 파싱, accountId 매핑, 중복 검색, Jira 계획 제시.
9. 최종 확인 후에만 Jira 이슈 생성/링크/스킵.

## 시작 인테이크 (Startup Intake)

입력 분류 직후, Stage B/C 이전에 이 세 가지 질문을 하세요.

| Key | 질문 | 기본값 |
|---|---|---|
| `meeting_date` | 오늘 또는 이 회의 날짜가 몇일인가요? | 대본/페이지에 날짜 단서(언급된 날짜, "다음 주", 예정된 항목)가 있으면 그에 부합하는 날짜를 제안; 없으면 현재 시스템 날짜. 붙여넣은 대본은 과거 회의인 경우가 많으니 무턱대고 오늘로 가정하지 말 것. |
| `meeting_location` | 어디서 회의했나요? 예: Google Meet, Discord, 오프라인, Zoom | 입력에서 후보를 제안으로만 추론 |
| `meeting_topic` | 회의 주제명은 무엇인가요? | 파일명/페이지 제목에서 후보를 제안으로만 추론 |

계속하기 전에 요약:

```text
사전 정보 확인:
- 날짜: <meeting_date>
- 장소: <meeting_location>
- 주제: <meeting_topic>
```

이 값들을 회의 마크다운 frontmatter, 회의 제목, Confluence 제목, Jira 설명, 최종 요약에 사용하세요.

## 확인 게이트 (Confirmation Gates)

가능한 최선의 확인 수단을 사용하세요. Codex App에서는 구조화된 입력이 없으면 간결한 평문 질문을 하세요.

| Gate | 시점 | 필요한 사용자 결정 |
|---|---|---|
| Intake | stage 실행 전 | 날짜, 장소, 주제 |
| Name Review | 대본 로드 후 이름이 불확실할 때 | 이름 교정 및 추가 별칭 |
| B-G1 | 액션 추출 후 | 분리 정책, 프로젝트 라우팅, 담당자/기한 불확실성 |
| B-G2 | Confluence/Jira 전 | 전체 마크다운 승인; 요약만으로는 승인 불가 |
| C-G1 | Jira 쓰기 전 | 생성/링크/스킵 계획, project_key, assignee displayName, watcher accountId, Epic/링크 처리 |

C-G1을 통과하기 전에는 `mcp__atlassian__jira_create_issue`, `mcp__atlassian__jira_update_issue`, `mcp__atlassian__jira_transition_issue`, `mcp__atlassian__jira_create_issue_link`, `mcp__atlassian__jira_add_comment`, `mcp__atlassian__jira_add_watcher`를 절대 호출하지 마세요.

## 인물 및 Atlassian 계정 (People And Atlassian Accounts)

정식 인물/계정 표와 계정 규칙은 `references/people.md`에 있습니다(휘발성 조직 데이터로, 팀원/accountId 변경이 정책을 건드리지 않도록 분리). 담당자, accountId, displayName, 별칭을 해석해야 할 때마다 그 파일을 읽으세요. 이 스펙의 아래 규칙들(게이트, 라우팅, Jira 계약, 검증)은 그 표를 복사하지 않고 역할로 참조합니다.

## 이름 정규화 (Name Normalization)

대본 로드 후 B-G2 전에 이름을 정규화하세요:

1. 감지된 이름을 나열.
2. 명백한 별칭/STT 오류를 정식 이름으로 매핑.
3. `raw -> canonical` 교정을 표시.
4. 신뢰도 낮은 이름은 `확인 필요`로 남김.
5. 확인된 교정을 대본 텍스트, 회의 마크다운, Jira 계획에 일관되게 적용.

이름이 비슷하다는 이유만으로 새로운 사람을 알려진 팀원으로 정규화하지 마세요.

### 모호한 토큰 (Ambiguous tokens)

일부 짧은 이름 토큰은 두 명 이상과 매칭될 수 있습니다(예: 공유된 이름 일부). 감지된 토큰이 둘 이상의 정식 인물에 매핑될 수 있으면 자동 할당하지 마세요. 한 매핑이 더 그럴듯해 보여도 `확인 필요`로 표시하고 사용자에게 물으세요. 여기서의 조용한 구분(silent disambiguation)은 잘못된 Jira assignee를 만들고, 되돌리는 비용이 큽니다.

### 참석자 vs 언급 (Attendee vs mention)

frontmatter `attendees` 목록은 이름이 등장한 모든 사람이 아니라 실제로 회의에 있었던 사람을 반영해야 합니다.

- 대본에서 발언하는 사람은 참석자입니다.
- 3인칭으로만 언급되는 사람(예: "혜인이가 정리해준 것")은 언급이며 반드시 참석자는 아닙니다.
- 명시적인 "오늘 없고 / 불참 / 못 왔다"는 불참자를 표시합니다.
- 참석 여부가 불분명하면 추측하지 말고 그 사람을 `확인 필요`로 표시하고 Name Review 또는 B-G1 게이트에서 확인하세요. 대본만으로 참석을 추론하기 어려우니 묻는 것을 선호하세요.

## 회의 마크다운 스키마 (Meeting Markdown Schema)

필수 frontmatter:

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

필수 액션 표:

```markdown
## 🎯 액션 아이템

| # | 작업 | 프로젝트 후보 | 담당자 | 기한 | 상태 |
|---|---|---|---|---|---|
| 1 | ... | DDK/OPS/프로젝트 미정 | 이름 또는 (미정) | YYYY-MM-DD 또는 미정 | TODO/DONE/진행중 |
```

소스 인용/타임스탬프는 B-G1 검토 표에 유지하되, 기존 Confluence 컨벤션이 요구하지 않는 한 최종 회의 마크다운에서는 소스 전용 컬럼을 제거하세요.

## DDK / OPS 라우팅 (DDK / OPS Routing)

| 후보 | 용도 |
|---|---|
| `DDK` | 제품 기능, UX/UI, 구현, QA/검증, 디자인/프로토타입, 데이터/기술 결정, 제품 산출물을 바꾸는 작업 |
| `OPS` | 운영, 일정 관리, 회의 준비, 문서 정리, 커뮤니케이션, 조율, 프로세스 관리, 운영으로 추적되는 작업 |
| `프로젝트 미정` | 모호한 작업; 사용자가 DDK 또는 OPS를 선택하기 전에는 Jira 생성 금지 |

라우팅은 C-G1 전까지는 최종 결정이 아니라 후보입니다.

### 스킵 후보 (드러내되, 조용히 생성하지 말 것)

회의의 모든 줄이 Jira 티켓은 아닙니다. 다음은 자동으로 티켓을 만들지 말고 B-G1에서 스킵/처리 후보로 표시해 사용자가 결정하게 하세요:

- 단일 담당자가 없는 모호한 숙제(예: 모두에게 배정된 "각자 고민해오기") — 제안: 담당자가 지정된 추적 티켓 하나, 인별 티켓, 또는 노트만.
- 비제품/소셜 항목(예: 팀 회식/MT 준비) — OPS로 라우팅하기 전에 Jira에 넣을지 자체를 확인.
- 약속된 액션이 없는 순수 논의 또는 TBD — Jira가 아니라 회의 문서에 유지.

목표는 일관성입니다: 사용자는 매 실행마다 같은 종류의 질문을 받아야 하며, 즉흥적 판단에 맡겨져선 안 됩니다.

## Jira 생성 계약 (Jira Creation Contract)

모든 Jira 후보에 대해 쓰기 전에 계획 행을 만드세요:

`mcp__atlassian__jira_create_issue(project_key=, summary=, issue_type=, assignee=, description=, additional_fields={...})` 형태로 호출합니다(sooperset):

| 필드 | 규칙 |
|---|---|
| `project_key` | 확인 후에만 `DDK` 또는 `OPS` |
| `issue_type` | `작업` |
| `summary` | 원래 액션 텍스트 사용; 간결하게 유지 |
| `assignee` | **displayName** 사용(accountId/email은 silent no-op). 사용자가 미할당을 명시적으로 승인하지 않는 한 필수 |
| `description` | markdown. 액션, 결정 근거, 회의 링크, 회의 장소/주제, 관련 Epic/소스 포함 |
| `additional_fields.parent` | 동일 프로젝트 parent 키 문자열만 (예: `"DDK-9"`) |
| `additional_fields.duedate` | ISO 날짜 또는 불명 시 생략 |
| `additional_fields.customfield_10147` | 필수: 액션 아이템에는 `{"value": "L3"}` (Decision Level) |

> `customfield_10147`은 `ttalkkak.atlassian.net` 전용 필드 ID입니다(이 스킬은 해당 워크스페이스 전용). 다른 워크스페이스로 확장한다면 이 ID를 이 표에서 직접 고치지 말고 별도 사이트 설정(예: `references/site-config.yaml`)으로 분리해 본문 수정 없이 재사용하세요.

교차 프로젝트 규칙:

- DDK Epic 하위의 DDK 이슈: 확인되면 `additional_fields.parent` 사용.
- DDK Epic과 관련된 OPS 이슈: OPS에 OPS 이슈를 생성한 뒤 `mcp__atlassian__jira_create_issue_link(link_type="관련된 이슈", ...)`로 연결.

중복 규칙:

- 생성 전에 assignee로 최근 DDK/OPS 이슈를 검색.
- "본인 담당분 별도 과제", "이미 진행 중", "DONE", 유사한 노트는 중복 위험으로 취급.
- C-G1에서 중복을 제시하고 중복 생성보다 스킵/링크를 기본값으로.

Watcher 규칙:

- 기본값은 watcher 없음. 회의가 계속 알려야 할 비-assignee(예: 리뷰어, 페어 담당자, 알림을 요청한 리드)를 지명한 경우에만 추가.
- C-G1에서 accountId와 함께 watcher 목록을 명시적으로 제안; watcher를 조용히 추가하지 말 것.
- watcher는 `mcp__atlassian__jira_add_watcher(issue_key=, user_id=<accountId>)`로 추가(displayName 아님). watcher가 필요 없으면 최종 요약에 그렇다고 명시해 누락이 잊히지 않고 보이게.

## 검증 체크리스트 (Validation Checklist)

B-G2 전:

- 이름이 정식이거나 명시적으로 `확인 필요`로 표시됨.
- 액션 담당자가 소스 인용과 충돌하지 않음.
- 액션 표에 필수 컬럼과 유효한 값이 있음.
- `프로젝트 미정` 행이 강조됨.
- DONE 항목이 신규 티켓 후보로 집계되지 않음.

C-G1 전:

- 모든 생성 후보에 `project_key`, assignee displayName 또는 승인된 미할당 상태, 기한 처리, 중복 처리, parent/링크 전략이 있음.
- OPS 후보에 DDK parent가 배정되지 않음.
- `프로젝트 미정`에 Jira 쓰기가 계획되지 않음.
- watcher는 `jira_add_watcher`로 accountId를 사용함.

## 툴 제약 (Tool Constraints)

이 스킬은 같은 레포의 `jira-creator`와 동일하게 **sooperset `mcp-atlassian` 서버**(`mcp__atlassian__*` 접두사 + snake_case 툴명)를 전제로 합니다. 아래 이름 그대로 호출하세요:

- Confluence: `mcp__atlassian__confluence_search`, `mcp__atlassian__confluence_get_page`, `mcp__atlassian__confluence_create_page`, `mcp__atlassian__confluence_update_page`, `mcp__atlassian__confluence_add_comment`
- Jira: `mcp__atlassian__jira_search`, `mcp__atlassian__jira_get_issue`, `mcp__atlassian__jira_create_issue`, `mcp__atlassian__jira_update_issue`, `mcp__atlassian__jira_add_comment`, `mcp__atlassian__jira_add_watcher`, `mcp__atlassian__jira_create_issue_link`, `mcp__atlassian__jira_transition_issue`, `mcp__atlassian__jira_get_transitions`

> 인증/의존성: sooperset 서버는 **Atlassian API 토큰**으로 동작합니다(env: `JIRA_URL`/`CONFLUENCE_URL`=`https://ttalkkak.atlassian.net`, `ATLASSIAN_EMAIL`, `ATLASSIAN_API_TOKEN`). 토큰은 발급자 권한으로 동작하므로 별도 신규 Jira 권한은 필요 없습니다. `jira-creator`와 같은 서버·토큰을 공유합니다.
>
> 주의: 공식 Atlassian Remote MCP(OAuth)는 **camelCase**(`createJiraIssue` 등)라 이름이 다릅니다. 두 서버는 보통 한 환경에 동시에 안 깔리니, 실제 연결된 서버가 sooperset인지 먼저 확인하세요(`mcp__atlassian__atlassianUserInfo`가 있으면 공식 서버, 없으면 sooperset).

제공된 페이지나 알려진 옵션에서 space ID를 찾을 수 없으면, 임의로 만들지 말고 사용자에게 Confluence space/parent를 물으세요.
