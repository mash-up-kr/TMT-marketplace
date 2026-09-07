# be-oncall-kit

딸깍팀(Mash-Up 16기) 온콜 봇 스킬 모음.

[TMT-oncall](https://github.com/mash-up-kr/TMT-oncall) 봇이 Discord에서 받은 질문에 답할 때 호출하는 스킬입니다. 봇은 스킬 **이름만** 알고 문구는 갖지 않기로 해서, 역할별 톤이 여기 있습니다.

## 스킬

| 스킬 | 언제 | 톤 |
|---|---|---|
| `answer-design` | 질문자의 Discord 역할이 **디자인** | 화면에서 무엇이 어떻게 보이는지. 코드 용어 없이 3~6문장 |
| `answer-web` | 역할이 **웹** | API 계약 — 엔드포인트·요청/응답 형태·상태 코드·에러 바디 |
| `answer-spring` | 역할이 **스프링** | 코드 위치·설정·스택. 근거를 `파일:줄`로 |

역할이 없거나 판정되지 않으면 봇이 `answer-design`으로 답합니다.

## 출력 계약

세 스킬 모두 JSON 객체 하나만 출력합니다.

```json
{ "answer": "...", "code_fix_needed": true, "fix_plan": ["...", "..."] }
```

`code_fix_needed`가 `true`면 봇이 `fix_plan`을 'PR 만들기' 버튼과 함께 보여주고, 누르면 그대로 수정 작업의 입력이 됩니다. 그래서 답변 본문이 코드 용어를 피하는 디자인 톤에서도 `fix_plan`만은 개발자가 읽을 말로 씁니다.

형식이 깨지면 봇은 답변 본문만 살리고 수정 버튼을 붙이지 않습니다 — 형식 하나 때문에 질문한 사람이 아무 답도 못 받는 것보다는 낫기 때문입니다.

## 사람이 직접 쓰기

봇 없이 로컬에서 단독으로 써도 됩니다. TMT-BE 워크스페이스에서:

```
/be-oncall-kit:answer-spring 리뷰 목록 조회가 데이터 늘고 나서 느려졌는데 왜죠
```

## 아직 없는 것

[SPEC](https://github.com/mash-up-kr/TMT-oncall/blob/main/docs/SPEC.md)이 정한 6종 중 답변 3종만 있습니다. `incident-triage` · `incident-analyze`는 붙을 `IncidentTriage`(TMT-330)가, `tmt-fix-pr`은 계약을 맞출 `PullRequestAgent`가 아직 정리되지 않아 후속으로 둡니다.
