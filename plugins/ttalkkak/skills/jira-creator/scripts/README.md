# scripts

jira-creator 스킬의 보조 스크립트 모음.

## `jira_adf.py`

Markdown → ADF(Atlassian Document Format) 변환 + Jira 이슈 description 업데이트.

### 왜 필요?

Jira Cloud는 markdown `- [ ]` 를 인터랙티브 체크박스로 렌더링하지 않음 ([Atlassian MCP 이슈 #25](https://github.com/atlassian/atlassian-mcp-server/issues/25)). 진짜 클릭 가능한 체크박스가 필요하면 ADF `taskList` 노드로 직접 보내야 함.

이 스크립트가 그 변환을 자동 처리.

### 사용

```bash
# 환경 변수 셋업
export ATLASSIAN_EMAIL='wnsvy607@naver.com'
export ATLASSIAN_API_TOKEN='ATATT...'   # claude.local.md 참고

# stdin 으로 markdown
cat <<'EOF' | python3 jira_adf.py DDK-33
## 🎯 목적
한 줄 설명

## ✅ 체크리스트
- [ ] 항목 1
- [ ] 항목 2
- [x] 이미 완료된 항목
EOF

# 파일에서
python3 jira_adf.py DDK-33 -f description.md

# 미리보기 (PUT 안 함)
python3 jira_adf.py DDK-33 -f description.md --dry-run
```

### 지원 markdown 서브셋

- `#` ~ `######` 헤딩
- 문단 (멀티라인)
- `- 항목` 불릿
- `- [ ]` / `- [x]` 체크박스 → ADF `taskList` (인터랙티브)
- `> 줄` 인용
- `[텍스트](URL)` 인라인 링크

### 모듈로 사용

```python
import sys
sys.path.insert(0, '<scripts 경로>')
from jira_adf import parse_markdown, update_jira_description

doc = parse_markdown("## ✅ 체크리스트\n- [ ] 항목 1\n- [ ] 항목 2")
status, body = update_jira_description("DDK-33", doc)
```

### 의존성

Python 3.8+ (표준 라이브러리만 사용 — `urllib`, `argparse`, `re`, `json`).
