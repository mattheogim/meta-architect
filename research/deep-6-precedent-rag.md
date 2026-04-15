# Deep Research #6: Precedent Researcher RAG 구현

## 질문
"이 문제를 누가 이미 풀었는가"를 실제로 검색하려면 어떤 RAG 파이프라인이 필요한가?

## 찾은 근거

### RAG 아키텍처 성숙도 (2024-2025)
- 2024: naive vector search → sophisticated hybrid retrieval로 전환
- **GraphRAG (Microsoft, 2024 오픈소스)**: entity-relationship 그래프 기반 검색. 테마 수준 쿼리 가능
- **RAG-Fusion**: 다중 reformulated query + reciprocal rank fusion → recall 향상
- **DRAGIN/FLARE**: 토큰 수준 동적 검색 트리거 (confidence 낮을 때만 검색)

### Precedent Researcher에 필요한 지식 소스
| 소스 | 유형 | 접근 방법 |
|------|------|----------|
| GitHub 레포 | 코드 + README | GitHub API + embedding |
| 기술 블로그 | 설계 결정 | 웹 크롤링 + embedding |
| 아키텍처 패턴 DB | 구조화된 지식 | 자체 구축 또는 기존 DB |
| 논문 | 학술적 근거 | Semantic Scholar API |
| Stack Overflow | 실전 경험 | SO API + embedding |

### v2의 RAG 가드레일과 대조
- v2: "URL 3개 이상 필수, 없으면 evidence_level: anecdotal"
- 이건 좋은 원칙이지만 RAG 구현 세부사항이 없음

### 실현 가능성 판단
- **즉시 가능**: Semantic Scholar API + GitHub API로 기본 검색
- **중기**: 아키텍처 패턴 knowledge base 구축 (기존 패턴 문서 임베딩)
- **장기**: GraphRAG로 프로젝트 간 관계/유사성 그래프

### v2 보강 제안
- Precedent Researcher를 **RAG 도구 + LLM 판단** 하이브리드로 구현
  - 검색 = RAG 파이프라인 (코드)
  - 유사성 판단 + 장단점 분석 = LLM
- evidence_level을 RAG 결과의 quality에 연동
  - 3+ 독립 소스 → empirical
  - 1~2 소스 → anecdotal  
  - 0 소스 → no_contribution (hallucination 방지)
