# jira-creator

딸깍팀 Jira 이슈 생성 스킬 (OPS · DDK 프로젝트).

## 사용법

Claude Code 대화에서:

```
이슈 만들어줘: DDK에 목 데이터 수집 Task, 담당자 정혜인
```

또는 자세하게:

```
OPS에 Decision 이슈 만들어줘.
- 제목: 외부 노출 여부 결정
- 배경: 그룹 평가 결과를 익명으로 외부 공개할지 결정 필요
- Decision Level: L2
```

## 설치

`SKILL.md`를 Claude Code의 skills 경로에 배치하거나, 대화에서 직접 내용을 참조합니다.

## 주의사항

- MCP `mcp__atlassian-ddalkkak` 연결 필수
- DDK 이슈는 Decision Level 필수 (미설정 시 생성 실패)
- Assignee는 반드시 **display name** 사용 (account ID · email 사용 시 silent no-op)

## 관련 문서

- [Jira 프로젝트 구조 가이드](https://ttalkkak.atlassian.net/wiki/spaces/ttalkkak/pages/18546704)
