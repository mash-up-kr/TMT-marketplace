---
name: meeting-minutes
description: 회의 대본이나 기존 Confluence 회의록을 교정된 회의록과 ttalkkak.atlassian.net용 Jira 액션 티켓으로 변환합니다. 회의록 작성/게시, 액션 아이템을 DDK/OPS Jira 티켓으로 분리, 한국어 팀원 이름을 Atlassian 계정에 매핑, 중복 Jira 작업 탐지, watcher 멘션 추가, 기존 Confluence 액션 아이템 표 처리를 요청할 때 사용하세요. 오디오 전사/STT(먼저 외부에서 전사한 뒤 대본을 전달), 단건 수동 Jira 티켓, Linear/GitHub 이슈 워크플로에는 사용하지 마세요.
---

# meeting-minutes

하나의 정식 진실원(canonical source of truth)으로 회의 파이프라인을 실행합니다:

1. `references/spec.md`를 먼저 읽으세요.
2. 입력 모드를 감지하세요.
3. spec의 시작 인테이크 질문을 물어보세요.
4. 감지된 모드에 필요한 stage 레퍼런스만 로드하세요.
5. 외부 Jira/Confluence 상태를 생성·수정하기 전에 각 확인 게이트에서 멈추세요.

## 입력 모드

| 모드 | 입력 | 로드 |
|---|---|---|
| B | 대본 `.txt`, 붙여넣은 대본 텍스트, 또는 `transcripts_*/` 디렉터리 | `references/stage-b-meeting-doc.md` -> `references/stage-c-jira.md` |
| C | Confluence 페이지 ID, tiny 링크, 또는 URL | `references/stage-c-jira.md` |

오디오 녹음은 이 스킬의 범위 밖입니다. 입력이 오디오/비디오 파일이면 여기서 전사하지 마세요 — 사용자에게 외부에서 전사(아무 STT 도구나, 또는 VTT/대본 내보내기)한 뒤 그 대본을 Mode B로 다시 실행하도록 요청하세요.

지원 옵션: `--epic DDK-9`, `--team-lead <name>`, `--space <KEY or spaceId>`.

## 절대 규칙 (Non-Negotiables)

이것들은 무엇을 주의해야 하는지에 대한 리마인더입니다. 구속력 있는 세부 내용은 `references/spec.md`와 `references/people.md`에 한 번만 존재합니다 — 이 파일의 요약을 정식 텍스트보다 우선하지 말고, 규칙 세부사항을 이 파일에 다시 적지 마세요(드리프트를 유발함).

- `references/spec.md`가 정식입니다. stage 파일이 spec과 충돌하면 spec을 따르세요.
- 회의록은 담당자, 기한, 결정사항, 액션 텍스트의 유일한 진실원입니다 — 사실을 절대 지어내지 마세요.
- 해당하는 확인 게이트를 통과하기 전에 Jira/Confluence에 절대 쓰지 마세요 (spec.md → Confirmation Gates).
- 생성/스킵 규칙(`프로젝트 미정`, 담당자 불명, accountId 없음, DONE, 중복), account-field 및 멘션 규칙, OPS-대-DDK-Epic 교차 프로젝트 규칙은 각각 spec.md / people.md에 한 번씩 정의되어 있습니다 — 그곳에서 적용하세요.

## 단계 산출물

- Stage B: `~/Desktop/meetings/<YYYY-MM-DD>/` 아래의 로컬 회의 마크다운.
- Stage C: Confluence 페이지 URL과 생성/링크/스킵된 Jira 이슈 요약.

## 리소스

- `references/spec.md` - 정식 인테이크 필드, 게이트, 스키마, DDK/OPS 라우팅, 이름 정규화, 검증 규칙, Atlassian 제약.
- `references/people.md` - 정식 인물/계정 표(이름, accountId, displayName, 별칭)와 계정 규칙. 팀이 바뀌면 여기를 수정하세요.
- `references/stage-b-meeting-doc.md` - 대본 → 회의 마크다운.
- `references/stage-c-jira.md` - 회의 마크다운 → Confluence/Jira.
