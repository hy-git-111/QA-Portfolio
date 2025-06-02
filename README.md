# Portfolio
## 1. About me
안녕하세요.  
반복되는 문제를 그냥 넘기지 않고, 직접 해결 방법을 고민하고 실험해보는 QA 엔지니어 김혜영입니다.

수동 테스트에서 출발했지만, 환경 이슈 개선을 위해 자체 모니터링 도구를 제작해본 경험이 있습니다.  
이후 자동화 테스트와 LLM API 연동까지 직접 시도하며 테스트 효율화를 설계해보았습니다.

자동화의 한계를 느낀 뒤에는 테스트 설계력의 중요성을 깨닫고,  
현재는 DB 흐름 기반의 테스트 시나리오 작성에도 도전하고 있습니다.  
실습과 학습을 반복하며 테스트의 효율성과 본질을 함께 고민하는 QA로 성장하고 싶습니다.

## 2. Projects
이 포트폴리오에는 **직접 작성한 산출물만 발췌**하여 정리하였습니다.  
2차 프로젝트의 테스트 시나리오를 제외한 모든 문서와 결과물은 직접 작성한 내용입니다.

### 오늘 뭐 먹지 - AI 메뉴 추천 웹앱 QA

- 페이지 기반으로 전체 UI 요소를 검증하는 자동화 테스트 스크립트 구현
- 자동화 테스트 실행 결과를 바탕으로 결함 리포트 작성
- [Testcase(Google Sheets)](https://docs.google.com/spreadsheets/d/1DCZmkrZaEWpEKfRqDpZnWgieNcIwcts5/edit?usp=sharing&ouid=115467792666132717582&rtpof=true&sd=true)
- [Bug Report(Notion)](https://drive.google.com/file/d/13TjDo_DxJT8a_TxWPNqUVPUiZXkiNs8e/view?usp=sharing)
- [pytest 테스트 리포트(html)](https://hy-git-111.github.io/eliceproject_qa04/report.html)

### RealWorld - 소셜 블로깅 플랫폼(Medium) 클론 프로젝트 QA
- 사용자 시나리오 기반으로 LLM API를 활용한 UI 자동화 테스트 설계
- 테스트 계획서 및 자동화 결과 리포트 작성
- [QA 자동화 테스트 계획서(Notion)](https://drive.google.com/file/d/1kE_iUneOCMFHX7b2q0eVMhd3CDTXQx2p/view?usp=sharing)
- [Testcase(Google Sheets)](https://docs.google.com/spreadsheets/d/19Wv5aZH9RQehH4muqcWtqFv3-nEprcfz/edit?usp=sharing&ouid=115467792666132717582&rtpof=true&sd=true)
- [QA 자동화 테스트 결과 보고서(Notion)](https://drive.google.com/file/d/1t7IJKnjejLBoxRBeFmR4MvdqmM3zbKPK/view?usp=sharing)

## 3. Soft skills
아래 Soft Skills는 실제 프로젝트 경험을 기반으로 도출하였습니다.

| 소프트스킬 | 설명 |
|------------|------------|
| 기능 간 영향도 예측 및 사전 리스크 감지 역량 | 테스트 전 다양한 실행 조건을 고려해 문제 가능성을 선제적으로 점검 |
| 사용자 관점 문제 탐색 및 통합 기능 검증 역량 | 테스트케이스 외 실제 사용 환경을 기반으로 오류 케이스 탐색 |
| 테스트 커버리지 누락 방지를 위한 커뮤니케이션 역량 | 기획 누락 사항을 직접 질문하고 검증 범위를 확장 |
| 피드백 수용 및 성장 지향 마인드셋 | 종료 후 피드백을 먼저 요청하고, 수용과 개선 태도를 긍정적으로 평가받음 |
| 구조적 문제 정리 및 유연한 협업 태도 | 기능 흐름을 시각적으로 정리하고, 팀 의견을 수용해 효율적인 방향 전환을 주도 |

## 4. Hard Skills
부트캠프 프로젝트, 개인 실습, 그리고 이전 직장 경험을 통해 익힌 주요 도구들을 실제 적용 사례 중심으로 정리했습니다.

### UI 자동화
* **Python**  
  - 이전 직장에서 웹 뷰 버전 모니터링 프로그램을 직접 설계 및 구현해, 팀 내 수동 배포 환경에서 활용 
  - 부트캠프 1차 프로젝트에서 pytest 기반의 POM 구조로 UI 테스트 스크립트를 작성하고 리포트 생성
  - 부트캠프 2차 프로젝트에서 LLM API를 연동해 테스트 스크립트 자동화 로직 구현

* **Selenium**
  - 웹 요소 조작을 통해 키보드 및 마우스 이벤트를 자동화
  - pytest UI 테스트 케이스에 적용하여 사용자 시나리오 기반의 자동화 테스트를 수행

### API 테스트
* **Postman**  
- 사용자 등록 API에 대해 명세 작성부터 정상/예외 흐름 테스트를 설계하고, Runner 및 Newman으로 자동 테스트를 수행하여 결과 분석까지 실습함

### 성능 테스트
* **JMeter**
  - 단순 GET 요청 및 로그인 인증 흐름 기반의 부하 테스트 시나리오를 구성하여 성능 지표를 확인함

### CI/CD 
* **Jenkins**
  - 2차 프로젝트에서 Docker 기반의 VM 환경에서 자동 배포 파이프라인을 구성
  - GitLab push, Merge Request 이벤트 기반 CI자동화를 구현

* **Docker**  
  - Jenkins 기반의 CI 환경을 구성할 때 이미지 빌드, 컨테이너 실행 환경으로 활용

### 협업 도구
* **Redmine**
  - 이전 직장에서 결함 추적 및 이슈 관리 도구로 사용
  - 테스트 결과 기반의 이슈 등록, 상태 모니터링에 활용

* **Google Spreadsheets**
  - 테스트케이스 작성, 결함 분포 시각화, 테스트 결과 정리에 활용
  - 이전 직장 프로젝트에서는 협업 문서로도 적극 사용

* **GitLab**
  - 부트캠프 프로젝트에서 소스코드 관리 및 팀원 간 협업 브랜치 관리에 사용

* **Notion**
  - 부트캠프에서 팀 페이지 관리, 데일리스크럼 회의록 작성 등에 사용

## 5. Certificates
- [ISTQB CTFL](https://drive.google.com/file/d/1TUH-lI0yzwLWOF3_T5naMxJhWt6M9Xtc/view?usp=sharing)
- [CSTS FL](https://drive.google.com/file/d/1uPIkwsb3CBxOEuaWuEx14SV7ABwGSSzL/view?usp=sharing)
- [컴퓨터 활용능력 1급](https://drive.google.com/file/d/1fm8Ct6fiYLULAjc5B2YoLqQwUwsl5yJc/view?usp=sharing)
- [정보처리기사](https://drive.google.com/file/d/1TRFpdke59K4g55FrWWIYhmtHvoOaOf4W/view?usp=sharing)

## 6. Courses
- [[엘리스그룹] QA 자동화 엔지니어 트랙](https://drive.google.com/file/d/1LYKO_Us8y-DjY4MWUNyhyufNe_2wluV7/view?usp=sharing)  
: Pytest UI 자동화, API 테스트 실습, Jenkins CI 구성, 팀 프로젝트 2회 참여(1차 프로젝트: [리더스파크상](https://drive.google.com/file/d/1bk7AZKatn85r_OnWhqtkH5KhhgUhP7IB/view?usp=sharing) 수상)

- [[코멘토] QA 테스트 자동화 구축하고 QA 실무 역량 퀀텀 점프하기](https://drive.google.com/file/d/1kvv4Wf_TiwjPPixOXcvv9kgVHuldAabH/view?usp=sharing)  
: Python Selenium을 활용한 UI 테스트 자동화 실습 과정

## 7. Learning & Practice
부트캠프의 커리큘럼은 끝났지만, 테스트의 본질과 설계력을 고민하는 학습은 계속되고 있습니다.  
지식 기반의 QA로 성장하기 위해 작은 실습과 정리를 이어가고 있습니다.  
프로젝트와 학습 내용은 앞으로도 유연하게 확장될 예정입니다.

### Learning
| 구분 | 설명 | 링크 |
|------|------|------|
| python | SDLC, 유닛 테스트, Python 기반 UI 자동화 관련 개념 정리 | [learning/python](./learning/python) |
| qa | QA 이론, JMeter, DevTools 등 주요 QA 도구 중심 정리 | [learning/qa](./learning/qa) |
| web | 웹의 동작 원리 | [learning/web](./learning/web) |
| javascript | JavaScript 기초 문법 및 UI 자동화 응용 | [learning/javascript](./learning/javascript) |
> 'LearningNotes'저장소에 서브모듈로 연결되어 있습니다.

### Practice
- [Postman & Newman 사용자 등록 API 테스트](./practice/postman_api_test)
- [JMeter 부하 테스트 실습](./practice/jmeter_load_tests)