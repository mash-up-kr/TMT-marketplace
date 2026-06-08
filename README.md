# ttalkkak-marketplace

> 딸깍팀(Mash-Up 16기)의 **공용 스킬·에이전트·자동화 스크립트** 마켓플레이스

팀이 만든 재사용 가능한 도구를 한 곳에 모아 공유합니다. Claude Code skills, AI agent prompts, 자동화 스크립트, 공통 설정·템플릿 등.

## 🎯 목적

- **재사용**: 한 명이 만든 유용한 도구를 팀 전체가 활용
- **AI Native 협업**: 스펙·결정·자동화 산출물을 코드로 공유 (spec-first)
- **운영 자산화**: Jira 알림·문서 자동화·테스트 데이터 등 운영 도구 축적

## 📦 Claude Code 마켓플레이스로 설치

```bash
# 1. 마켓플레이스 등록 (manifest의 name = team-marketplace)
claude plugin marketplace add mash-up-kr/ttalkkak-marketplace

# 2. team-tools 플러그인 설치
claude plugin install team-tools@team-marketplace
```

설치 후 Claude Code에서 `/team-tools:jira-creator` 또는 자연어로 호출.

## 📂 구조

```
ttalkkak-marketplace/             # GitHub repo (URL은 유지)
├── .claude-plugin/
│   └── marketplace.json          # name: team-marketplace
├── plugins/
│   └── team-tools/               # 메인 플러그인 (팀 공용 스킬 묶음)
│       ├── .claude-plugin/
│       │   └── plugin.json       # name: team-tools
│       └── skills/
│           └── jira-creator/     # Jira 이슈 생성 (OPS·DDK)
│               ├── SKILL.md
│               ├── README.md
│               └── scripts/
│                   ├── jira_adf.py
│                   └── README.md
├── mcps/                         # MCP 서버 설정 템플릿 (참고용 문서)
│   └── configs/atlassian/
└── docs/                         # 추가 가이드 (TBD)
```

> 새 스킬 추가 시 `plugins/team-tools/skills/<name>/SKILL.md` 경로에. 자세히는 [CONTRIBUTING.md](./CONTRIBUTING.md).

## 🤝 기여 방법

1. 새 스킬·스크립트 추가 시 **브랜치** 만들고 PR 올리기 (main 직접 push 금지)
2. 디렉터리 안에 짧은 `README.md` 또는 `SKILL.md`로 사용법·맥락 명시
3. 시크릿·토큰은 **절대 커밋 금지** — 환경 변수나 별도 vault 사용
4. PR 설명에 "이게 왜 필요한지" 한 줄 + "어디서 쓰일지" 한 줄 포함

자세한 내용은 [CONTRIBUTING.md](./CONTRIBUTING.md) 참고.

## 🔢 버저닝 정책

마켓플레이스(`marketplace.json`)와 각 플러그인(`plugin.json`)의 버전은 **독립적**으로 관리합니다. 둘 다 [semver](https://semver.org/lang/ko/) 따름.

### 플러그인 버전 — `plugins/<name>/.claude-plugin/plugin.json`

사용자 측 캐시(`~/.claude/plugins/cache/...`) 무효화 기준. **버전 숫자를 올리지 않으면 `/plugin marketplace update` 해도 사용자 캐시가 갱신되지 않습니다.**

| Bump | 언제 | 예시 |
|---|---|---|
| **patch** (0.0.**X**) | 사용자가 보는 동작·인터페이스 동일 | SKILL.md 문구 수정, 버그픽스, 내부 리네임, 스크립트 리팩터링 |
| **minor** (0.**X**.0) | 새 기능 추가 (깨지지 않음) | 새 스킬·커맨드·MCP 템플릿 추가, 기존 스킬에 새 옵션 |
| **major** (**X**.0.0) | 깨지는 변경 | 스킬 이름·네임스페이스 변경, 필수 인자 추가/제거, MCP 서버 키 변경, 폴더 구조 재편 |

### 마켓플레이스 버전 — `.claude-plugin/marketplace.json`

카탈로그 자체의 메타. 플러그인 내부 변경과 **독립**. 카탈로그 라인업이 바뀔 때만 bump.

| Bump | 언제 | 예시 |
|---|---|---|
| **patch** | 메타 변경 | 설명·카테고리·태그·정렬 수정 |
| **minor** | 플러그인 추가/제거 | `team-tools` 외 새 플러그인 등록, 기존 플러그인 deprecate |
| **major** | 마켓플레이스 자체 깨지는 변경 | 마켓플레이스 이름 변경, 스키마 재편 |

> 예: `team-tools` 를 `v0.2.0 → v0.3.0` 으로 올려도 `marketplace.json` 버전은 그대로 둡니다.

### 0.x → 1.0.0 승격 기준

`0.x` 는 "공개 API 불안정" 신호 (semver 컨벤션). 다음을 모두 만족하면 1.0.0 으로 promote:

- 팀원 모두 한 번 이상 사용
- 깨지는 변경이 2주 이상 없음

### PR 워크플로우

1. 변경 내용에 맞춰 bump 타입 결정 (patch / minor / major)
2. 해당 `plugin.json` (또는 `marketplace.json`) 의 `version` 수정
3. PR 설명에 한 줄 추가 — 예: `v0.2.1 (patch): jira-creator SKILL.md 문구 정리`

### 캐시 강제 새로고침 (트러블슈팅)

버전을 정상 bump 했는데도 반영이 안 되는 것 같으면 (드물지만):

```bash
rm -rf ~/.claude/plugins/cache/team-marketplace
```

그다음 Claude Code 에서 `/plugin marketplace update`.

## 👥 팀

- **Spring**: 이준표(팀장), 장민서, 임준형
- **Web**: 정혜인(팀장), 장정우, 이창우
- **Design**: 이서원, 하아얀

## 🔗 관련 레포

- [ttalkkak-web](https://github.com/mash-up-kr/ttalkkak-web) — 딸깍 웹 클라이언트
- [ttalkkak-notify](https://github.com/mash-up-kr/ttalkkak-notify) — Jira/Confluence → Discord 알림 봇

## 📋 운영 채널

- **이슈 트래커**: [Jira ttalkkak.atlassian.net](https://ttalkkak.atlassian.net) (관련 OPS-37)
- **문서**: [Confluence ttalkkak space](https://ttalkkak.atlassian.net/wiki/spaces/ttalkkak)
- **실시간**: Discord 트랙 채널

## 📄 License

[MIT](./LICENSE)
