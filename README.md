# TMT-marketplace

> 딸깍팀(Mash-Up 16기)의 **공용 스킬·에이전트·자동화 스크립트** 마켓플레이스

팀이 만든 재사용 가능한 도구를 한 곳에 모아 공유합니다. Claude Code skills, AI agent prompts, 자동화 스크립트, 공통 설정·템플릿 등.

## 🎯 목적

- **재사용**: 한 명이 만든 유용한 도구를 팀 전체가 활용
- **AI Native 협업**: 스펙·결정·자동화 산출물을 코드로 공유 (spec-first)
- **운영 자산화**: Jira 알림·문서 자동화·테스트 데이터 등 운영 도구 축적

## 📦 Claude Code 마켓플레이스로 설치

```bash
# 1. 마켓플레이스 등록 (manifest의 name = team-marketplace)
claude plugin marketplace add mash-up-kr/TMT-marketplace

# 2. team-tools 플러그인 설치
claude plugin install team-tools@team-marketplace
```

설치 후 Claude Code에서 `/team-tools:jira-creator` 또는 자연어로 호출.

## 🤖 Codex에서 설치

Codex도 동일한 플러그인·마켓플레이스 개념을 지원합니다(`.codex-plugin/plugin.json` + `.agents/plugins/marketplace.json`). 그래서 Claude와 **대칭으로** 설치합니다:

```bash
# 1. 마켓플레이스 등록 (owner/repo 슬러그 — 원격에서 바로)
codex plugin marketplace add mash-up-kr/TMT-marketplace

# 2. team-tools 플러그인 설치
codex plugin add team-tools@team-marketplace
```

설치하면 `skills/` 아래 스킬이 **번들 통째로** 딸려옵니다. 설치 후 **Codex 재시작**하면 인식합니다. 업데이트는 `codex plugin marketplace upgrade`.

> 일부 스킬은 MCP(예: atlassian)에 의존하므로, Codex `config.toml`에 동일 MCP가 설정돼 있어야 런타임에 정상 동작합니다.

## 📂 구조

```
TMT-marketplace/             # GitHub repo (= 마켓플레이스 루트)
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
