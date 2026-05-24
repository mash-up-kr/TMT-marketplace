# ttalkkak Jira Issue Creator

딸깍팀(Mash-Up 16기) Jira 이슈 생성 스킬. OPS · DDK 프로젝트에 이슈를 올바른 구조로 만들기 위한 가이드.

> MCP: `mcp__atlassian-ddalkkak__*` 툴 사용 (ttalkkak.atlassian.net)
> 참고 문서: [Jira 프로젝트 구조 가이드](https://ttalkkak.atlassian.net/wiki/spaces/ttalkkak/pages/18546704)

---

## 아키텍처

```
사용자 요청
    ↓
Step 1. 프로젝트 · 이슈 타입 결정
    ↓
Step 2. 컨텍스트 수집 (Jira/Confluence 참조 이슈 있으면)
    ↓
Step 3. 담당자 · Decision Level · Backup Assignee 확인 (AskUserQuestion)
    ↓
Step 4. 사용자 최종 확인
    ↓
Step 5. 이슈 생성 (mcp__atlassian-ddalkkak__jira_create_issue)
    ↓
Step 6. 링크 연결 (필요 시)
```

---

## Step 1. 프로젝트 · 이슈 타입 결정

### 프로젝트 선택 기준

| 프로젝트 | 역할 | 언제 |
|---|---|---|
| **OPS** | 운영·기획·의사결정 | "무엇을 만들지 결정"해야 할 때 |
| **DDK** | 실제 개발·구현 | "만들기로 결정된 것을 만들" 때 |

```
이슈가 개발 작업(코딩·디자인·테스트)인가?  → DDK
의사결정·운영·기획 사안인가?              → OPS
```

### 이슈 타입 (OPS)

| 타입 | 언제 | 예시 |
|---|---|---|
| **Idea** | 컨셉·아이디어 탐색, 진행 결정 전 | "그룹 맛집 지도 서비스" 후보 등록 |
| **Decision** | 옵션→결정 안건. 48h RFC 프로세스 | "투트랙 프로토타입 진행 결정" |
| **Task** | 운영성 단발 작업 (레포 생성, 채널 셋업 등) | "마켓플레이스 레포지토리 생성" |
| **Meeting** | 회의 결과·후속 액션 트래킹 | (회의록은 Confluence, Jira는 액션만) |
| **Onboarding** | 신규 합류·계정·툴 셋업 | 합류 시 사용 |

### 이슈 타입 (DDK)

| 타입 | 계층 | 언제 | 예시 |
|---|---|---|---|
| **Epic** | 최상위 | 큰 단위 묶음 (마일스톤·feature) | "5/23 인터뷰 검증용 프로토타입" |
| **Story** | Epic 하위 | 사용자 가치 단위 (INVEST) | "UT용 와이어프레임 제작" |
| **Task** | Epic 하위 | 산출물 명확한 기술 작업 | "목 데이터 수집 (선릉역 중심)" |
| **Subtask** | Story/Task 하위 | 더 쪼갠 개인 단위 | 큰 Task 내 세부 단계 |
| **Bug** | 독립 | 동작 오류 | 회귀·결함 |

---

## Step 2. 컨텍스트 수집

참조 이슈나 Confluence 문서를 언급했다면 먼저 조회:

```
# 이슈 조회
mcp__atlassian-ddalkkak__jira_get_issue(issue_key="OPS-14")

# 연관 이슈 검색 (JQL)
mcp__atlassian-ddalkkak__jira_search(jql="project = DDK AND parent = DDK-9")

# Confluence 페이지
mcp__atlassian-ddalkkak__confluence_get_page(page_id="8028173")
```

---

## Step 3. 인터뷰 (AskUserQuestion)

이슈 생성 전 **반드시** 다음 항목을 확인한다.

### 담당자 (Assignee)

⚠️ **반드시 Jira display name 사용**. account ID · 이메일은 silent no-op (설정된 것처럼 보이지만 실제 적용 X).

| 실명 | Jira display name | account ID (watcher용) | 팀 |
|---|---|---|---|
| 이준표 | `Dradnats` | `712020:cdb6b0e7-8a68-4e9d-9d79-511f92898ad6` | Spring 팀장 |
| 정혜인 | `hyein396` | `712020:c165ade4-ad82-416f-b24e-8d96ebd3e732` | Web 팀장 |
| 장민서 | `Minseo Jang` | `712020:eba24041-39c7-46a8-a960-7581cb007de3` | Spring |
| 임준형 | `임준형` | `712020:aaabb651-1817-46ef-96b5-e759b841fad5` | Spring |
| 장정우 | `장정우` | `712020:7a4a319d-e043-4edc-8378-e0e5353c8717` | Web |
| 이창우 | `changchangwoo119` | `712020:69ebe92d-f78e-4b83-9c45-639435e36b74` | Web |
| 이서원 | `이서원` | `712020:04061ce9-2704-419e-bbb9-b8f8d7512f8f` | Design |
| 하아얀 | `하아얀` | `712020:19ac4adb-ae00-41f7-810b-3bea326a0172` | Design |

```python
# ✅ 올바른 assignee
assignee="Dradnats"          # 이준표
assignee="changchangwoo119"  # 이창우

# ❌ 작동 안 함 (silent no-op)
assignee="712020:cdb..."     # account ID
assignee="wnsvy607@..."      # email
```

### Decision Level (`customfield_10147`) — DDK 필수

DDK 이슈는 **반드시** 설정. 미설정 시 create 실패 ("Decision Level is required").

| 레벨 | 범위 | 결정 장소 |
|---|---|---|
| **L1** | 서비스 컨셉, MVP 범위, 기술 스택 (방향성) | 전원 참여 정기 회의 |
| **L2** | 로그인 플로우, API 설계, 화면 구조 (기능 단위) | 담당자+관련자, Confluence 비동기 |
| **L3** | 버튼 위치, 에러 메시지, 색상 (세부 조정) | 담당자 간, Jira 코멘트 |

> OPS도 마찬가지로 필요. 기본값: **L3** (불분명하면 L2)

```python
additional_fields={"customfield_10147": {"value": "L2"}}
```

### Backup Assignee (`customfield_10181`) — 선택

- 담당자 48h 무응답 시 대신 진행
- account ID 객체 형식 사용:

```python
additional_fields={"customfield_10181": {"accountId": "712020:cdb6b0e7-..."}}
```

### Watcher 추가 (선택)

- `jira_add_watcher`로 별도 호출. **account ID 사용** (display name 아님)

```python
mcp__atlassian-ddalkkak__jira_add_watcher(
    issue_key="DDK-999",
    user_id="712020:cdb6b0e7-8a68-4e9d-9d79-511f92898ad6"  # 이준표
)
```

---

## Step 4. 사용자 최종 확인

이슈 생성 전 **반드시** 아래 포맷으로 확인받는다:

```
📋 이슈 생성 확인
─────────────────────
프로젝트:        DDK
이슈 타입:       Task
Summary:         [운영] 목 데이터 수집 (선릉역 중심)
담당자:          hyein396 (정혜인)
Decision Level:  L3
Backup Assignee: 없음
우선순위:        Medium

📝 Description:
(요약)

이대로 생성할까요?
```

수정 요청 시 반영 후 재확인. 승인 후에만 Step 5 진행.

---

## Step 5. 이슈 생성

### 기본 호출 형식

```python
mcp__atlassian-ddalkkak__jira_create_issue(
    project_key="DDK",
    summary="[운영] 목 데이터 수집 (선릉역 중심)",
    issue_type="Task",
    assignee="hyein396",          # display name
    description="...",            # Markdown
    additional_fields={
        "customfield_10147": {"value": "L3"},  # Decision Level (필수)
        "customfield_10181": {"accountId": "712020:..."}  # Backup (선택)
    }
)
```

### Summary 패턴

```
[태그] 본문 — 상위 참조
```

| 패턴 | 예시 |
|---|---|
| `[프로토타입]` | `[프로토타입] 그룹 맛집 지도 — 5/23 인터뷰 검증용` |
| `[운영]` | `[운영] 공통 마켓플레이스 레포지토리 생성` |
| `[기획]` | `[기획] 투트랙 프로토타입 진행 결정` |
| `[데이터]` | `[데이터] 목 데이터 스키마 v0.1 (DDK-18)` |

### Description 템플릿

```markdown
## 목적
이 이슈가 풀려는 문제 한 줄

## 작업 내용
- 무엇을
- 왜

## 핵심 액션 / 체크리스트
- [ ] 항목 1
- [ ] 항목 2

## 참고
- 상위 Epic / 관련 이슈 링크
- 회의록·Confluence 문서 링크
- 결정 근거 (OPS Decision 이슈 참조)
```

### Epic 하위 이슈 연결 (DDK)

Subtask는 `additional_fields.parent`로 상위 이슈 키 전달:

```python
additional_fields={"parent": "DDK-9"}  # ✅ 문자열
# ❌ additional_fields={"parent": {"key": "DDK-9"}}  # 객체 형식 에러
```

Story/Task를 Epic에 연결할 때도 parent 사용:

```python
additional_fields={"parent": "DDK-9"}
```

---

## Step 6. 링크 연결 (선택)

여러 이슈 생성 후 관계 연결:

```python
mcp__atlassian-ddalkkak__jira_create_issue_link(
    link_type="관련된 이슈",       # ⚠️ 반드시 한글
    inward_issue_key="DDK-100",
    outward_issue_key="OPS-24"
)
```

| 한글 (사용) | 의미 |
|---|---|
| **관련된 이슈** | 일반 연관 |
| **블로킹** | A가 B를 막음 |
| **의존된 이슈** | A가 B에 의존 |
| **중복된 이슈** | 동일 작업 |

---

## 자주 쓰는 케이스

### 단일 Task 생성 (가장 흔한 케이스)

1. 프로젝트 확인 (OPS or DDK)
2. 담당자·Decision Level 질문
3. 확인 후 생성

### Epic + 하위 Task 여러 개

1. Epic 먼저 생성 → 키 확인
2. 각 Task를 `additional_fields.parent = "DDK-<epic키>"` 로 생성
3. 전체 구조 요약 제공

### Decision 이슈 (OPS)

- Decision Level: L1 또는 L2
- Description에 **옵션 비교 + 결정 근거** 포함
- 생성 후 팀원 watcher 추가 권장 (48h RFC 프로세스 시작)

---

## 코멘트 작성 컨벤션

이슈 생성 후 첫 코멘트 또는 후속 코멘트:

- **결정·새 정보만** — 본문·직전 코멘트 중복 X
- 멘션은 필요한 사람에게만
- 막힌 부분은 "무엇이 막혔는지 + 누구의 액션 필요한지" 명시
- verbose 금지 — 한두 줄로 끝낼 수 있으면 그렇게

---

## 에러 핸들링

| 에러 | 원인 | 해결 |
|---|---|---|
| `Decision Level is required` | customfield_10147 미설정 | `{"customfield_10147": {"value": "L2"}}` 추가 |
| `Field 'assignee' cannot be set` | account ID / email 사용 | display name 으로 변경 |
| `issue type is required` | 이슈 타입명 오류 | 정확한 타입명 사용 (대소문자 포함) |
| MCP 연결 안 됨 | mcp__atlassian-ddalkkak 미연결 | MCP 재연결 안내 후 중단. 우회 시도 X |

---

## 참고 링크

- [Jira 프로젝트 구조 가이드 (Confluence)](https://ttalkkak.atlassian.net/wiki/spaces/ttalkkak/pages/18546704)
- [딸깍 팀 운영 가이드](https://ttalkkak.atlassian.net/wiki/spaces/ttalkkak/pages/15433729)
- [3. 의사결정 · 합의 룰](https://ttalkkak.atlassian.net/wiki/spaces/ttalkkak/pages/15663105)
- [Jira 이슈 보드 (OPS)](https://ttalkkak.atlassian.net/jira/software/projects/OPS/boards)
- [Jira 이슈 보드 (DDK)](https://ttalkkak.atlassian.net/jira/software/projects/DDK/boards)
