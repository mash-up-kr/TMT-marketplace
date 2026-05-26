---
name: jira-creator
description: 딸깍팀(Mash-Up 16기) Jira 이슈 생성 워크플로우. OPS(운영·기획·의사결정) 또는 DDK(개발) 프로젝트에 이슈 작성 시 사용. "딸깍 이슈 만들어줘", "OPS Decision 등록", "DDK Task 만들어줘", "ttalkkak Jira 이슈 생성" 같은 요청에 트리거. 타입별 템플릿(Epic/Story/Task/Subtask/Bug/Decision/Idea), Decision Level 필수 처리, 팀원 매핑, Jira vs Confluence 정보 배분 가이드 포함.
---

# ttalkkak Jira Issue Creator

딸깍팀(Mash-Up 16기) Jira 이슈 생성 스킬. OPS · DDK 프로젝트에 이슈를 올바른 구조로 만들기 위한 가이드.

> MCP: `mcp__atlassian__*` 툴 사용 (ttalkkak.atlassian.net)
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
Step 2.5. Confluence 분리 판단 ⭐ (본문 길어질 것 같으면 페이지 먼저 만들기)
    ↓
Step 3. 담당자 · Decision Level · Backup Assignee 확인 (AskUserQuestion)
    ↓
Step 4. 사용자 최종 확인
    ↓
Step 5. 이슈 생성 (mcp__atlassian__jira_create_issue)
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
mcp__atlassian__jira_get_issue(issue_key="OPS-14")

# 연관 이슈 검색 (JQL)
mcp__atlassian__jira_search(jql="project = DDK AND parent = DDK-9")

# Confluence 페이지
mcp__atlassian__confluence_get_page(page_id="8028173")
```

---

## Step 2.5. Confluence 분리 판단 ⭐

> **원칙**: Jira 티켓 = 핵심 트래킹, Confluence = 상세 문서. 본문이 길어질 것 같으면 Confluence 페이지를 먼저 만들고 Jira엔 링크만 남긴다. ([가이드](https://ttalkkak.atlassian.net/wiki/spaces/ttalkkak/pages/18546704#5-jira-vs-confluence-정보-배분))

### 다음 중 **하나라도** 해당하면 Confluence 페이지를 먼저 만든다

- 본문이 **15줄 이상** 으로 늘어날 것 같음
- **옵션 2개 이상** 비교가 필요함
- 외부 자료·표·다이어그램이 들어감
- "이 결정은 왜?" 가 길어짐 (Decision 이슈)
- 데이터 스키마 / 스펙 / API 설계

### Confluence 페이지 작성 (필요 시)

```python
mcp__atlassian__confluence_create_page(
    space_key="ttalkkak",
    title="[태그] 제목 — 한 줄 요약",
    parent_id="<적절한 부모 페이지 ID>",
    content_format="markdown",
    content="""
# [태그] 제목

> 관련 Jira: <링크>  · 작성 YYYY-MM-DD

## 배경
왜 이게 필요한지

## 옵션 / 분석 / 데이터
긴 본문은 여기에

## 결정 / 다음 액션
한두 줄 결론 → 이게 Jira 본문으로 들어감

## 변경 이력
| 일자 | 변경 | 작성자 |
"""
)
```

→ 응답에서 page URL을 받아서 Jira Description의 "참고" 섹션에 링크.

### Jira만으로 충분한 케이스

- 단순 운영성 작업 (레포 생성, 채널 셋업)
- 작은 체크리스트만 있으면 끝나는 작업
- 버그 수정·재현 단계

이런 경우는 Step 2.5 건너뛰고 바로 Step 3.

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
mcp__atlassian__jira_add_watcher(
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
mcp__atlassian__jira_create_issue(
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

### Description 템플릿 — 타입별

> 📋 **상세 템플릿·예시는 [Jira 이슈 타입별 템플릿 · 예시](https://ttalkkak.atlassian.net/wiki/spaces/ttalkkak/pages/18546754)** 참고.
>
> **핵심 원칙**: Jira 본문은 짧지만 충분히. 옵션 비교·표·긴 배경은 Confluence로 분리.
>
> ⚠️ **체크리스트는 두 가지 방법**:
> - **인터랙티브 체크박스가 필요하면 → [Step 5.5 ADF taskList 패턴](#step-55-인터랙티브-체크박스-adf-tasklist) 사용** (MCP 후 REST API로 description 재설정)
> - **간단한 시각만 충분하면 → `- ⬜` 사용** (markdown 그대로, 진행 시 `⬜` → `✅` 수동 변경)
>
> 템플릿에서는 `⬜` 표기로 작성. 인터랙티브 필요 시 Step 5.5로 변환.

#### Epic 🏔 (DDK)

```markdown
## 🎯 목표
이 Epic이 달성하려는 결과 (2~4줄)

## ✅ Definition of Done
- 명확한 산출물 1
- 검증 방법

## 👥 멤버 · 역할
| 멤버 | 역할 |

## 📐 스코프
포함 / 제외 (의식적으로 제외한 것)

## 🔗 관련
- 상위 OPS Decision / 상세 컨셉 / 회의록
```

#### Story 📖 (DDK)

```markdown
## 사용자 가치
**As a** [사용자]  **I want** [기능]  **So that** [가치]

## 승인 기준
- ⬜ 시나리오 1: [상황]에서 [동작]하면 [결과]
- ⬜ 시나리오 2:
- ⬜ 시나리오 3:

## 🔗 관련
- 상위 Epic / 디자인 / 의존
```

#### Task ✅ (DDK · OPS)

```markdown
## 🎯 목적
한 줄

## 📋 작업 내용
3~5줄

## ✅ 체크리스트
- ⬜ 실행 가능 단위 1
- ⬜ 실행 가능 단위 2

## 🔗 관련
- 상위 Epic / 상세 문서(Confluence) / 결정 근거
```

#### Subtask 🔹

```markdown
## 작업
한 줄

## 체크리스트
- ⬜ 단일 산출물 1

## 🔗 부모: [DDK-XX](...)
```

#### Bug 🐞

```markdown
## 🌐 환경
디바이스/브라우저 · 빌드 · 재현 빈도

## 🔁 재현 단계
1. 2. 3.

## 🎯 기대 vs ⚠️ 실제

## 📊 영향도
사용자 영향 · 우회 방법

## 🔗 관련 Story / 로그·스크린샷
```

#### Decision ⚖️ (OPS)

```markdown
## 🎯 안건
한 줄

## 🧭 배경
3~5줄

## 🗳 옵션
| | A | B |
|---|---|---|
| 장점 | | |
| 단점 | | |

## ✋ 추천 + 근거 / ✅ 결정 / 📋 후속 액션

## 🔗 상세 분석(Confluence) / RFC 마감 / Decision Level
```

#### Idea 💡 (OPS)

```markdown
## 💡 컨셉 (한 줄)
## 🎯 페인포인트
## 🔧 솔루션 골격 (3~5줄)
## ✅ 검증 필요 / 리스크
## 🚪 다음 게이트 (Decision 이슈 · 회의)
## 🔗 상세 컨셉 문서
```

### 본문 길이 자가 체크

이슈 생성 직전 본문을 다시 보고:

- ✅ 타입별 권장 섹션만, 옵션 비교/표/긴 배경 없음 → 그대로 생성
- ⚠️ 옵션 비교·긴 분석 들어감 → Step 2.5로 돌아가서 Confluence로 분리, 본문엔 결론만

---

## Step 5.5. 인터랙티브 체크박스 (ADF taskList)

> MCP `jira_create_issue` 의 `description` 파라미터는 markdown만 받음. markdown `- [ ]` 는 Jira에서 인터랙티브 체크박스로 렌더링되지 않음 ([Atlassian MCP Issue #25](https://github.com/atlassian/atlassian-mcp-server/issues/25)). 진짜 클릭 가능한 체크박스가 필요하면 **이슈 생성 후 `scripts/jira_adf.py` 로 description 재설정**.

### 언제 사용

- 이슈 본문에 4개 이상의 체크리스트 항목이 있고
- 담당자가 진행 상황을 클릭으로 토글하길 원할 때

체크리스트가 짧거나 (1~3개) 시각만 충분하면 `- ⬜` 그대로 두면 됨.

### 사용법

**1단계** — MCP로 이슈 먼저 생성 (description은 `- [ ]` 포함된 markdown 그대로):

```python
issue = mcp__atlassian__jira_create_issue(
    project_key="DDK",
    summary="...",
    issue_type="Task",
    assignee="...",
    description="""
## 🎯 목적
한 줄

## ✅ 체크리스트
- [ ] 항목 1
- [ ] 항목 2
- [ ] 항목 3
""",
    additional_fields={"customfield_10147": {"value": "L3"}}
)
issue_key = issue["key"]   # 예: "DDK-33"
```

**2단계** — `scripts/jira_adf.py` 로 ADF description 재설정 (Bash):

```bash
# scripts 디렉터리는 SKILL.md와 같은 경로
SCRIPT_DIR="$(dirname "$(realpath "${BASH_SOURCE[0]:-$0}")")/scripts"

# 환경 변수 (claude.local.md 토큰 참고)
export ATLASSIAN_EMAIL='wnsvy607@naver.com'
export ATLASSIAN_API_TOKEN='ATATT...'

# 같은 markdown을 stdin 으로 전달 → 인터랙티브 체크박스로 변환
cat <<'MD' | python3 "$SCRIPT_DIR/jira_adf.py" "$issue_key"
## 🎯 목적
한 줄

## ✅ 체크리스트
- [ ] 항목 1
- [ ] 항목 2
- [ ] 항목 3
MD
```

### 스크립트 기능

`scripts/jira_adf.py` 가 자동 처리:

- `## 제목` → ADF heading
- `- 항목` → ADF bulletList
- **`- [ ]` / `- [x]` → ADF taskList (인터랙티브 체크박스!)**
- `> 인용` → ADF blockquote
- `[텍스트](URL)` → 인라인 링크
- `--dry-run` → PUT 없이 ADF JSON 미리보기

자세한 사용법은 [scripts/README.md](./scripts/README.md) 참고.

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
mcp__atlassian__jira_create_issue_link(
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
| MCP 연결 안 됨 | mcp__atlassian 미연결 | MCP 재연결 안내 후 중단. 우회 시도 X |

---

## 참고 링크

- [Jira 프로젝트 구조 가이드 (Confluence)](https://ttalkkak.atlassian.net/wiki/spaces/ttalkkak/pages/18546704)
- [딸깍 팀 운영 가이드](https://ttalkkak.atlassian.net/wiki/spaces/ttalkkak/pages/15433729)
- [3. 의사결정 · 합의 룰](https://ttalkkak.atlassian.net/wiki/spaces/ttalkkak/pages/15663105)
- [Jira 이슈 보드 (OPS)](https://ttalkkak.atlassian.net/jira/software/projects/OPS/boards)
- [Jira 이슈 보드 (DDK)](https://ttalkkak.atlassian.net/jira/software/projects/DDK/boards)
