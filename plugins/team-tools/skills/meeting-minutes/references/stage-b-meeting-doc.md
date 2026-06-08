# Stage B - 대본 → 회의 마크다운 (Transcript To Meeting Markdown)

Mode B에 사용하세요. `references/spec.md`를 먼저 읽으세요; 스키마, 라우팅, 게이트를 소유합니다. 인물/계정 표는 `references/people.md`에 있습니다.

## 단계 (Steps)

1. 대본 텍스트를 로드. 대본에 타임스탬프(`.srt`/`.vtt`/`.json`)가 있으면 결정/액션 근거로 사용.
2. 작성 전에 기존 Confluence 회의록 컨벤션을 학습:
   - `searchConfluenceUsingCql`로 `title ~ "회의록" OR title ~ "meeting" OR label = "meeting-minutes"` 같은 작은 쿼리 사용.
   - `getConfluencePage(contentFormat=markdown)`로 관련 상위 3-5개 페이지를 가져옴.
   - 제목 패턴, 반복 섹션, 액션 표 컬럼, 결정 표 형식, 멘션 스타일, 타임스탬프 스타일, 라벨을 추출.
   - 사용 가능한 페이지가 없으면 `spec.md`의 스키마 사용.
   - 컨벤션이 있으면 처음부터 그 더 풍부한 형태로 로컬 마크다운을 작성(예: 요약본 / 결정사항 / TBD / 액션아이템 / 논의 흐름 / 다음 회의). 팀 컨벤션이 최소 `spec.md` 스키마보다 우선. 이렇게 하면 로컬 파일과 게시될 페이지가 정렬되고 게시 시 문서 전체를 다시 쓰는 일을 피함. 로컬 마크다운을 최종 형태가 게시될 모습을 반영하는 중간 산출물로 취급.
   - 사용자가 "그냥 회의록만 써줘"라고 해도 이 컨벤션 확인을 수행 — 형식을 먼저 배우는 것이 나중에 다시 포맷하는 것보다 저렴함.
3. 회의 마크다운 작성:
   - 시작 인테이크의 `meeting_date`, `meeting_location`, `meeting_topic` 사용.
   - 정식 이름(spec.md 이름 정규화)과 `references/people.md`의 account-safe 담당자 사용.
   - 결정과 액션을 대본 근거에 기반하게 유지.
4. 액션 아이템을 B-G1 검토 표로 추출:

```markdown
| # | 작업 | 프로젝트 후보 | 담당자 | 기한 | 상태 | 출처 발화 |
|---|---|---|---|---|---|---|
```

5. B-G1 실행:
   - 분리 정책 확인: 액션당 티켓 하나, 주제 묶음, 담당자 묶음, 또는 사용자 지정.
   - 프로젝트 후보 확인: 유지, 행별 편집, 전부 DDK, 전부 OPS, 또는 미해결 행 보류.
   - 다중 담당자, 담당자 불명, 기한, DONE, 중복 위험 처리 확인.
6. `spec.md`의 필수 스키마로 최종 회의 마크다운 작성.
7. B-G2 전에 spec 체크리스트로 검증.
8. `~/Desktop/meetings/<meeting_date>/<safe-topic-or-basename>.md`에 저장.
9. B-G2 실행:
   - 요약이 아니라 전체 마크다운 본문을 표시.
   - 이름, 담당자, 프로젝트 후보, 표 형태, DONE 항목, 중복 위험 노트에 대한 검증 결과 표시.
   - Confluence/Jira에 게시할지, 수정할지, 저장만 할지, 중단할지 질문.

## 출력 계약 (Output Contract)

로컬 마크다운 경로와 B-G2 결정을 반환. 사용자가 Confluence/Jira 진행을 승인할 때만 Stage C로 계속.
