# Contributing to ttalkkak-marketplace

## 워크플로우

1. **이슈 또는 Jira 티켓** 먼저 (작은 기여는 생략 가능)
2. **브랜치** 생성: `<유형>/<짧은-설명>` (예: `skill/notion-sync`, `script/jira-cleanup`)
3. **PR 올리기**: main 직접 push 금지, 최소 1명 리뷰
4. **머지 후 브랜치 삭제**

## PR 설명 템플릿

```markdown
## Why
이 기여가 왜 필요한가 (한두 줄)

## What
무엇을 추가/수정했나

## How to use
사용 예시 한두 줄 (가능한 경우)

## Related
- Jira: <티켓 키>
- Confluence: <페이지 링크>
```

## 디렉터리 컨벤션

| 위치 | 무엇을 |
|---|---|
| `skills/<name>/` | Claude Code skill 1개 = 디렉터리 1개. `SKILL.md` 필수 |
| `agents/<name>/` | AI agent / sub-agent 프롬프트. `AGENT.md` 권장 |
| `scripts/<lang>/<name>` | 자동화 스크립트. 언어별로 폴더 |
| `templates/` | Jira·Confluence·회의록·PR 등 템플릿 |
| `mock-data/<project>/` | 시연·테스트용 데이터셋 |
| `docs/` | 가이드·결정 기록 |

## 보안 / 비밀

- 시크릿(API 토큰, webhook URL, 인증 정보)을 **절대 커밋하지 마세요**
- `.env`, `*.local.*`, `secrets/` 는 이미 `.gitignore`에 포함
- 실수로 커밋한 경우: 즉시 토큰 revoke + `git filter-repo`로 히스토리 제거

## 코드 스타일

특별한 강제 없음. 다음만 권장:
- 파이썬: `black` 포매팅
- JS/TS: `prettier` 포매팅
- 셸 스크립트: `shellcheck` 통과
- 모든 코드: **주석은 WHY만, WHAT은 식별자로 표현**

## 새 스킬 추가 체크리스트

1. `plugins/<plugin>/skills/<name>/SKILL.md` 작성 (name·description frontmatter 필수)
2. 별도 등록 불필요 — 플러그인이 `skills/`를 번들로 인식하므로 Claude(`plugin.json`)·Codex(`.codex-plugin/plugin.json`) 양쪽에 자동 포함됩니다.

## 문서

새 스킬/스크립트는 사용 예시를 README에 한두 줄이라도 추가.

## 질문

Discord 트랙 채널에 ping. Jira/Confluence에 비동기로 남겨도 OK.
