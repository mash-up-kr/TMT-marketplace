# MCPs

딸깍팀이 사용하는 **MCP (Model Context Protocol) 서버** 모음.

## 📂 구조

```
mcps/
├── servers/        # 팀이 직접 만든 MCP 서버 코드 (있을 경우)
└── configs/        # 외부 MCP 서버 등록용 설정 템플릿 + 셋업 가이드
    └── <name>/
        ├── .mcp.json.template   # 토큰 placeholder 포함된 설정
        └── README.md            # 셋업·검증·트러블슈팅
```

## 📋 등록된 MCP

| 이름 | 위치 | 용도 |
|---|---|---|
| **atlassian-ddalkkak** | [configs/atlassian-ddalkkak](./configs/atlassian-ddalkkak/) | 딸깍 Jira·Confluence 조작 |

## 🤝 새 MCP 추가하는 법

1. `configs/<name>/` 디렉터리 생성
2. `.mcp.json.template` — 토큰·시크릿은 **placeholder**로만 (`<YOUR_TOKEN>` 형식)
3. `README.md` — 사전 준비, 설치 방법, 검증, 트러블슈팅, 보안 주의
4. 본 `mcps/README.md`의 등록 표에 한 줄 추가
5. PR 생성

## ⚠️ 보안 원칙

- **토큰·시크릿·webhook URL 절대 커밋 X**
- 본인 환경의 실제 `.mcp.json`은 프로젝트 `.gitignore`에 포함
- 작업 끝난 토큰은 즉시 revoke
