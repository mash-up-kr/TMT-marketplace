# be-oncall-kit

딸깍팀(Mash-Up 16기) 온콜 봇 스킬 모음.

[TMT-oncall](https://github.com/mash-up-kr/TMT-oncall) 봇이 호출하는 스킬입니다. 봇은 스킬 **이름만** 알고 문구는 갖지 않기로 해서, 톤과 규칙이 여기 있습니다.

## 에러 스킬

| 스킬 | 언제 | 모델 |
|---|---|---|
| `incident-triage` | Sentry가 새 에러를 올림 | Haiku. **소스를 읽지 않고** 조치 필요 여부만 1차 판정 |
| `incident-analyze` | 판정을 통과한 건 | Sonnet. 소스를 읽고 원인 + 수정 계획 |

`incident-triage`가 `false`로 판정하면 채널에 아예 올라가지 않습니다. 형식이 깨지면 봇은 `true`로 봅니다 — 놓치는 쪽이 시끄러운 쪽보다 나쁘기 때문입니다.

## 답변 스킬

| 스킬 | 언제 | 톤 |
|---|---|---|
| `answer-design` | 질문자의 Discord 역할이 **디자인** | 화면에서 무엇이 어떻게 보이는지. 코드 용어 없이 3~6문장 |
| `answer-web` | 역할이 **웹** | API 계약 — 엔드포인트·요청/응답 형태·상태 코드·에러 바디 |
| `answer-spring` | 역할이 **스프링** | 코드 위치·설정·스택. 근거를 `파일:줄`로 |

역할이 없거나 판정되지 않으면 봇이 `answer-design`으로 답합니다.

## 에러 스킬

| 스킬 | 언제 | 모델 |
|---|---|---|
| `incident-triage` | Sentry가 새 에러를 올림 | Haiku. **소스를 읽지 않고** 조치 필요 여부만 1차 판정 |
| `incident-analyze` | 판정을 통과한 건 | Sonnet. 소스를 읽고 원인 + 수정 계획 |

`incident-triage`가 `false`로 판정하면 채널에 아예 올라가지 않습니다. 형식이 깨지면 봇은 `true`로 봅니다 — 놓치는 쪽이 시끄러운 쪽보다 나쁘기 때문입니다.

## 에러 스킬의 출력 계약

`incident-triage`:

```json
{ "action_needed": true, "reason": "...", "severity": "high|medium|low" }
```

`incident-analyze` — `Analysis` 레코드가 그대로 계약입니다. `fix_plan`은 'PR 만들기'를 누르면 `tmt-fix-pr`의 입력이 되고, `code_fix_possible`이 `false`면 버튼이 붙지 않습니다.

```json
{ "cause": "...", "fix_plan": ["..."], "impact": "...",
  "related_deploy": "...", "stack_excerpt": "...", "code_fix_possible": true }
```

## 답변 스킬의 출력 계약

세 스킬 모두 JSON 객체 하나만 출력합니다.

```json
{ "answer": "...", "code_fix_needed": true, "fix_plan": ["...", "..."] }
```

`code_fix_needed`가 `true`면 봇이 `fix_plan`을 'PR 만들기' 버튼과 함께 보여주고, 누르면 그대로 수정 작업의 입력이 됩니다. 그래서 답변 본문이 코드 용어를 피하는 디자인 톤에서도 `fix_plan`만은 개발자가 읽을 말로 씁니다.

형식이 깨지면 봇은 답변 본문만 살리고 수정 버튼을 붙이지 않습니다 — 형식 하나 때문에 질문한 사람이 아무 답도 못 받는 것보다는 낫기 때문입니다.

## 수정 스킬

| 스킬 | 언제 |
|---|---|
| `tmt-fix-pr` | 사람이 'PR 만들기' 버튼을 누른 뒤. 승인된 수정 계획대로 TMT-BE 작업 트리를 고칩니다 |

브랜치·커밋·푸시·PR은 봇(`PullRequestAgent`)이 직접 하므로 이 스킬은 **파일만** 고칩니다. 변경 사항이 하나도 없으면 봇이 실패로 처리합니다.

## 사람이 직접 쓰기

봇 없이 로컬에서 단독으로 써도 됩니다. TMT-BE 워크스페이스에서:

```
/be-oncall-kit:answer-spring 리뷰 목록 조회가 데이터 늘고 나서 느려졌는데 왜죠
```

## 경로

```
에러:  Sentry → incident-triage → incident-analyze → 리포트 → [PR 만들기] → tmt-fix-pr
질문:  Discord → 역할 판정 → answer-design | answer-web | answer-spring
```
