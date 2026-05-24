# atlassian-ddalkkak MCP

딸깍팀 Atlassian (`ttalkkak.atlassian.net`)의 Jira·Confluence를 Claude Code에서 사용하는 MCP 서버.

[sooperset/mcp-atlassian](https://github.com/sooperset/mcp-atlassian) 컨테이너 이미지를 podman으로 실행.

## 🛠️ 제공 도구 (요약)

- **Jira**: 이슈 조회/생성/수정, 코멘트, 검색(JQL), changelog, 전환(상태 변경), watcher 등
- **Confluence**: 페이지 조회/생성/수정/삭제, 코멘트, 라벨, 첨부, 검색(CQL) 등

## 📋 사전 준비

1. **podman 설치** (또는 docker — 명령어를 `docker run`으로 바꾸면 됨)
   ```bash
   brew install podman
   podman machine init && podman machine start
   ```

2. **Atlassian API 토큰 발급**
   - https://id.atlassian.com/manage-profile/security/api-tokens
   - "Create API token" → 라벨 입력 → 생성 → 토큰 값 복사 (창 닫으면 다시 못 봄)

3. **MCP 이미지 미리 pull** (선택, 첫 실행 시 자동 pull)
   ```bash
   podman pull ghcr.io/sooperset/mcp-atlassian:latest
   ```

## ⚙️ 설치

### 옵션 A) 프로젝트 단위 (권장)

본인 프로젝트 루트에 `.mcp.json` 생성:

```bash
cp .mcp.json.template /your/project/.mcp.json
```

또는 본 디렉터리의 `.mcp.json.template`을 복사한 뒤 아래를 본인 값으로 교체:

| placeholder | 값 |
|---|---|
| `<YOUR_EMAIL>` | Atlassian 계정 이메일 (예: `you@example.com`) |
| `<YOUR_ATLASSIAN_API_TOKEN>` | 위에서 발급한 API 토큰 |

⚠️ **`.mcp.json`은 토큰을 담으므로 절대 커밋하지 마세요.** 프로젝트 `.gitignore`에 `.mcp.json` 추가 필수.

### 옵션 B) 전역 설정

`~/.claude.json`의 `mcpServers`에 직접 추가:

```bash
jq '.mcpServers."atlassian-ddalkkak" = $cfg' \
  --slurpfile cfg <(cat .mcp.json.template | jq '.mcpServers."atlassian-ddalkkak"') \
  ~/.claude.json > ~/.claude.json.tmp && mv ~/.claude.json.tmp ~/.claude.json
```

(또는 `~/.claude.json`을 에디터로 열어서 수동 추가)

## ✅ 검증

Claude Code 재시작 후:

```
mcp__atlassian-ddalkkak__jira_get_all_projects 호출해줘
```

→ DDK / OPS / JIR 등 ttalkkak 프로젝트 목록이 나오면 성공.

## 🐛 트러블슈팅

| 증상 | 원인·해결 |
|---|---|
| `Connection closed` | podman machine 미실행 → `podman machine start` |
| `401 Unauthorized` | 토큰 만료/오타. https://id.atlassian.com/... 에서 새로 발급 |
| `image not found` | 이미지 pull 안 됨. 수동 `podman pull ghcr.io/sooperset/mcp-atlassian:latest` |
| `command not found: podman` | brew install 필요. docker만 있으면 `command` 필드를 `docker`로 변경 |

## 🔒 보안

- 토큰은 본인 권한 그대로 (read/write 가능)
- `.mcp.json` 절대 git 커밋 X (`.gitignore` 추가)
- 작업 끝나면 https://id.atlassian.com/manage-profile/security/api-tokens 에서 revoke 가능
- 회사·외부 채널에 토큰 공유 금지

## 🔗 출처·참고

- 원본 MCP server: https://github.com/sooperset/mcp-atlassian
- 도구 상세: 위 레포 README의 Tool list 참고
