# ttalkkak-marketplace

> 딸깍팀(Mash-Up 16기)의 **공용 스킬·에이전트·자동화 스크립트** 마켓플레이스

팀이 만든 재사용 가능한 도구를 한 곳에 모아 공유합니다. Claude Code skills, AI agent prompts, 자동화 스크립트, 공통 설정·템플릿 등.

## 🎯 목적

- **재사용**: 한 명이 만든 유용한 도구를 팀 전체가 활용
- **AI Native 협업**: 스펙·결정·자동화 산출물을 코드로 공유 (spec-first)
- **운영 자산화**: Jira 알림·문서 자동화·테스트 데이터 등 운영 도구 축적

## 📂 구조 (제안)

```
ttalkkak-marketplace/
├── skills/              # Claude Code skills (디렉터리당 1개 skill)
│   └── <skill-name>/
│       ├── SKILL.md
│       └── ...
├── agents/              # AI agent prompts / sub-agent 정의
├── scripts/             # 자동화 스크립트 (Python, Bash 등)
├── templates/           # 회의록·Jira·Confluence 등 템플릿
├── mock-data/           # 데모·시연용 데이터셋
└── docs/                # 사용법·기여 가이드
```

> 세부 구조는 첫 컨트리뷰션을 진행하면서 조정해주세요. 디렉터리는 **필요할 때 만들기**.

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
