#!/usr/bin/env python3
"""
Jira ADF helper — Markdown 본문을 ADF(Atlassian Document Format)로 변환해서
Jira 이슈 description을 PUT 한다. markdown `- [ ]` 가 인터랙티브 체크박스로 렌더링됨.

사용 (CLI):
  # stdin 으로 markdown
  cat description.md | python jira_adf.py DDK-33
  # 또는 파일 지정
  python jira_adf.py DDK-33 -f description.md
  # 미리보기 (PUT 안 함)
  python jira_adf.py DDK-33 -f description.md --dry-run

인증 (env):
  ATLASSIAN_EMAIL              필수
  ATLASSIAN_API_TOKEN          필수
  JIRA_BASE_URL                선택 (default: https://ttalkkak.atlassian.net)

사용 (모듈):
  from jira_adf import parse_markdown, update_jira_description
  doc = parse_markdown(md_text)
  update_jira_description("DDK-33", doc)

지원하는 markdown 서브셋:
  - 헤딩: # ## ### #### ##### ######
  - 문단 (멀티라인)
  - 불릿: - 또는 *
  - 체크박스: - [ ] / - [x]  → ADF taskList (인터랙티브)
  - 인용: > 줄
  - 인라인 링크: [텍스트](URL)
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request


# ---------------------------------------------------------------------------
# ADF builders
# ---------------------------------------------------------------------------

def text(s: str, link: str | None = None) -> dict:
    n = {"type": "text", "text": s}
    if link:
        n["marks"] = [{"type": "link", "attrs": {"href": link}}]
    return n


def paragraph(content: list) -> dict:
    return {"type": "paragraph", "content": content}


def heading(level: int, content: list | str) -> dict:
    if isinstance(content, str):
        content = [text(content)]
    return {"type": "heading", "attrs": {"level": min(level, 6)}, "content": content}


def bullet_list(items: list[list]) -> dict:
    return {
        "type": "bulletList",
        "content": [
            {"type": "listItem", "content": [paragraph(item)]}
            for item in items
        ],
    }


def task_list(items: list[str], done_indices: set[int] | None = None) -> dict:
    done = set(done_indices or [])
    return {
        "type": "taskList",
        "attrs": {"localId": "tl-1"},
        "content": [
            {
                "type": "taskItem",
                "attrs": {
                    "localId": str(i + 1),
                    "state": "DONE" if i in done else "TODO",
                },
                "content": [text(t)],
            }
            for i, t in enumerate(items)
        ],
    }


def blockquote(inline: list) -> dict:
    return {"type": "blockquote", "content": [paragraph(inline)]}


# ---------------------------------------------------------------------------
# Markdown → ADF parser (focused subset)
# ---------------------------------------------------------------------------

_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$")
_TASK_RE = re.compile(r"^[-*]\s+\[([ xX])\]\s+(.+)$")
_BULLET_RE = re.compile(r"^[-*]\s+(.+)$")
_QUOTE_RE = re.compile(r"^>\s?(.*)$")


def _parse_inline(line: str) -> list:
    """Inline links만 처리. 나머지는 text."""
    nodes: list = []
    pos = 0
    for m in _LINK_RE.finditer(line):
        if m.start() > pos:
            nodes.append(text(line[pos:m.start()]))
        nodes.append(text(m.group(1), m.group(2)))
        pos = m.end()
    if pos < len(line):
        nodes.append(text(line[pos:]))
    return nodes or [text(line)]


def parse_markdown(md: str) -> dict:
    """단순 markdown → ADF doc 변환."""
    lines = md.split("\n")
    content: list = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i].rstrip()

        if not line.strip():
            i += 1
            continue

        # 헤딩
        m = _HEADING_RE.match(line)
        if m:
            content.append(heading(len(m.group(1)), _parse_inline(m.group(2))))
            i += 1
            continue

        # 인용 (연속된 > 라인 묶기)
        if _QUOTE_RE.match(line):
            quote_text: list[str] = []
            while i < n and _QUOTE_RE.match(lines[i]):
                quote_text.append(_QUOTE_RE.match(lines[i]).group(1))
                i += 1
            content.append(blockquote(_parse_inline(" ".join(quote_text).strip())))
            continue

        # 체크박스 리스트 (- [ ] 연속 묶기)
        if _TASK_RE.match(line):
            items: list[str] = []
            done: set[int] = set()
            while i < n:
                tm = _TASK_RE.match(lines[i].rstrip())
                if not tm:
                    break
                if tm.group(1).lower() == "x":
                    done.add(len(items))
                items.append(tm.group(2))
                i += 1
            content.append(task_list(items, done))
            continue

        # 일반 불릿
        if _BULLET_RE.match(line):
            items_inline: list[list] = []
            while i < n:
                bm = _BULLET_RE.match(lines[i].rstrip())
                if not bm:
                    break
                rest = bm.group(1)
                # 체크박스로 시작하면 빠져나가서 위 블록이 처리
                if re.match(r"^\[[ xX]\]\s+", rest):
                    break
                items_inline.append(_parse_inline(rest))
                i += 1
            content.append(bullet_list(items_inline))
            continue

        # 문단 (빈 줄·블록 시작 전까지 합치기)
        para_lines: list[str] = []
        while i < n:
            cur = lines[i].rstrip()
            if not cur.strip():
                break
            if _HEADING_RE.match(cur) or _BULLET_RE.match(cur) or _QUOTE_RE.match(cur):
                break
            para_lines.append(cur)
            i += 1
        if para_lines:
            content.append(paragraph(_parse_inline(" ".join(para_lines))))

    return {"type": "doc", "version": 1, "content": content}


# ---------------------------------------------------------------------------
# Jira API
# ---------------------------------------------------------------------------

def update_jira_description(
    issue_key: str,
    doc: dict,
    *,
    email: str | None = None,
    token: str | None = None,
    base_url: str | None = None,
) -> tuple[int, str]:
    email = email or os.environ.get("ATLASSIAN_EMAIL")
    token = token or os.environ.get("ATLASSIAN_API_TOKEN")
    base_url = base_url or os.environ.get("JIRA_BASE_URL", "https://ttalkkak.atlassian.net")
    if not email or not token:
        raise SystemExit(
            "ATLASSIAN_EMAIL / ATLASSIAN_API_TOKEN 환경 변수가 필요합니다."
        )

    auth = base64.b64encode(f"{email}:{token}".encode()).decode()
    req = urllib.request.Request(
        f"{base_url}/rest/api/3/issue/{issue_key}",
        data=json.dumps({"fields": {"description": doc}}).encode("utf-8"),
        method="PUT",
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, (r.read().decode() or "")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(
        description="Markdown → ADF 변환 후 Jira 이슈 description 업데이트.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("issue_key", help="Jira 이슈 키 (예: DDK-33)")
    p.add_argument("-f", "--file", help="Markdown 파일 경로. 미지정 시 stdin")
    p.add_argument("--dry-run", action="store_true", help="PUT 안 함. ADF JSON만 출력")
    args = p.parse_args()

    md = open(args.file, encoding="utf-8").read() if args.file else sys.stdin.read()
    doc = parse_markdown(md)

    if args.dry_run:
        print(json.dumps(doc, ensure_ascii=False, indent=2))
        return

    status, body = update_jira_description(args.issue_key, doc)
    print(f"HTTP {status}: {body or '(empty body — success)'}")
    if status >= 400:
        sys.exit(1)


if __name__ == "__main__":
    main()
