# meeting-minutes

회의 **전사(대본)·Confluence 회의록**을 받아 → **교정된 회의록**과 **Jira 액션 티켓**으로 만들어주는 스킬입니다. (`ttalkkak.atlassian.net` 전용)

---

## 한 줄 요약

> "회의 대본 던지면 → 회의록 정리해서 Confluence에 올리고 → 할 일은 DDK/OPS Jira 티켓으로 끊어준다."

---

## 언제 쓰나

- 회의 대본/전사를 깔끔한 회의록으로 정리하고 싶을 때
- 회의록의 액션 아이템을 Jira(DDK/OPS) 티켓으로 쪼개고 싶을 때
- 기존 Confluence 회의록의 액션 표를 Jira로 옮기고 싶을 때

**안 쓰는 경우:** 오디오 받아쓰기(STT) — 외부 도구로 먼저 전사한 뒤 대본을 넣으세요. 그 외 Jira 티켓 1개 수동 생성, Linear/GitHub 이슈 작업.

---

## 입력 2가지 모드

| 모드 | 넣는 것 | 하는 일 |
|---|---|---|
| **B** | 전사 텍스트(`.txt`)·붙여넣은 대본·전사 폴더 | 회의록 → Jira |
| **C** | Confluence 페이지 ID/링크/URL | (이미 있는 회의록) → Jira |

> **오디오/영상은 범위 밖입니다.** 녹음 파일이 있으면 외부 STT 도구로 먼저 전사(또는 VTT/자막 추출)한 뒤, 그 대본을 **모드 B**로 넣으세요.

옵션: `--epic DDK-9`, `--team-lead <이름>`, `--space <키>`

---

## 동작 흐름

```
[전사]       → B. 회의록 작성 → C. Confluence/Jira
[Confluence] →                  C. Jira
```

중간에 **3개의 확인 게이트**에서 멈추고 사람에게 물어봅니다. 외부(Confluence/Jira)에 쓰기 전에 항상 확인받습니다.

| 게이트 | 시점 | 확인 내용 |
|---|---|---|
| **B-G1** | 액션 추출 후 | 티켓 분리 방식·DDK/OPS 라우팅·담당자/기한 |
| **B-G2** | Confluence/Jira 직전 | 회의록 전문 승인 |
| **C-G1** | Jira 쓰기 직전 | 생성/링크/스킵 계획·담당자 accountId·중복·Epic 처리 |

---

## 산출물

- **B단계:** 로컬 회의록 `~/Documents/meetings/<날짜>/<주제>.md`
- **C단계:** Confluence 페이지 URL + 생성/링크/스킵된 Jira 이슈 요약

---

## 안전장치 (핵심 규칙)

- 회의 내용을 **유일한 진실원**으로 삼고, 없는 사실은 지어내지 않음.
- **확인 게이트 통과 전엔 Jira/Confluence에 절대 쓰지 않음.**
- 다음은 자동 생성하지 않고 사용자에게 먼저 확인: `프로젝트 미정`, 담당자 불명, accountId 없음, DONE 항목, 중복 의심, 모호한 이름(예: 두 사람과 겹치는 별칭).
- OPS 이슈를 DDK Epic 하위(parent)로 넣지 않음 → OPS에 만들고 필요 시 `Relates`로 링크.

---

## 파일 구조

```
meeting-minutes/
├── SKILL.md                      # 진입점(모드 감지·라우팅)
├── README.md                     # 이 문서
├── agents/
│   └── openai.yaml               # Codex/OpenAI 앱 등록 메타(표시명·트리거·MCP 의존)
└── references/
    ├── spec.md                   # 정책 단일 진실원(게이트·스키마·라우팅·검증)
    ├── people.md                 # 팀원/계정 표(이름·accountId·별칭) ← 팀 바뀌면 여기 수정
    ├── stage-b-meeting-doc.md    # 전사 → 회의록
    └── stage-c-jira.md           # 회의록 → Confluence/Jira
```

> 책임 분리: **오케스트레이션(SKILL)** · **정책(spec)** · **변동 데이터(people)** · **절차(stage)** — 각 진실원이 하나씩.

---

## 팀 설정 (커스터마이즈)

- **팀원/계정**: `references/people.md` 표만 고치면 됨 (이름·displayName·accountId·별칭).
- **프로젝트 라우팅**: 제품·UX·구현·QA → **DDK** / 운영·일정·문서·커뮤니케이션 → **OPS** (`references/spec.md`).
- **회의록 포맷**: 기존 Confluence 회의록 컨벤션을 자동 학습해 맞춤(없으면 `spec.md` 기본 스키마).

---

## 요구사항

- **B/C단계**: Atlassian(Confluence/Jira) MCP 연결, `ttalkkak.atlassian.net` 접근 권한.
- **오디오 입력**: 별도 외부 STT로 전사 후 대본을 모드 B로 사용 (이 스킬은 전사 도구를 포함하지 않음).

---

## 사용 예

```
/meeting-minutes <전사 텍스트 붙여넣기>
/meeting-minutes ~/Downloads/회의-대본.txt
/meeting-minutes https://ttalkkak.atlassian.net/wiki/.../12345
```
