# ✨ Team03
- 팀명: 삼공주와 찬위무사
- 좌우명: “호위는 기본, 프로젝트도 완벽히 지켜낸다.”

## 👥 팀원
- 김다예
- 김혜영
- 신은영
- 윤찬유

## 📌 프로젝트 개요
본 프로젝트는 [RealWorld](https://github.com/gothinkster/realworld) 애플리케이션을 대상으로 API 테스트 자동화를 수행한 실습 프로젝트입니다.  
RealWorld는 다양한 프론트엔드 및 백엔드 기술 스택으로 동일한 기능을 구현한 [Medium.com](https://medium.com) 클론 예제입니다.  
단순한 Todo 앱 데모를 넘어서, 실제 서비스 수준의 기능을 갖춘 웹 애플리케이션을 테스트하는 데 목적이 있습니다.

- 백엔드: [`node-express-realworld-example-app`](https://github.com/gothinkster/node-express-realworld-example-app)  
- 프론트엔드: [`react-redux-realworld-example-app`](https://github.com/gothinkster/react-redux-realworld-example-app)  
- 테스트 환경: Postman, Newman, Python, PostgreSQL


## 🧱 아키텍처 구조

RealWorld는 **프론트엔드와 백엔드가 분리된 구조**이며, RESTful API를 통해 데이터를 주고받는 구조입니다.

- **프론트엔드:** React + Redux 기반 SPA  
- **백엔드:** Node.js + Express 기반 REST API 서버  
- **인증 방식:** JWT (JSON Web Token) 기반 인증  
- **API 포맷:** OpenAPI(Swagger) 또는 Postman 컬렉션 제공  


## ⚙️ 주요 기능
### 1. 사용자 인증
- 회원가입 (Sign up)
- 로그인 (Sign in) – JWT 기반 인증
- 로그아웃 (Settings 페이지 내)

### 2. 사용자 관리
- 사용자 정보 조회 (프로필 페이지)
- 사용자 정보 수정 (프로필 사진, 이름, 소개, 이메일, 비밀번호 변경)

### 3. 게시글(Articles)
- 게시글 목록 조회 (글로벌 피드 / 팔로우 피드 / 태그 필터링 / 페이지네이션)
- 게시글 작성 (제목, 설명, 본문(Markdown), 태그)
- 게시글 조회
- 게시글 수정 및 삭제 (자신의 게시글만 가능)

### 4. 댓글(Comments)
- 게시글 댓글 작성
- 댓글 목록 조회
- 댓글 삭제 (자신의 댓글만 가능)

### 5. 태그(Tags)
- 인기 태그 조회 (홈 화면)
- 게시글 작성 시 태그 입력
- 태그로 게시글 필터링

### 6. 소셜 기능
- 다른 사용자 팔로우 / 언팔로우
- 게시글 즐겨찾기(Favorite) / 즐겨찾기 해제
- 사용자별 게시글 목록 조회 (작성글 / 즐겨찾기한 글)


## 📁 디렉토리 구조
```
TEAM03/
├── ai_generate/              # AI 연동 모듈 (Claude)
├── google_sheets/            # 구글 시트 → 테스트케이스 변환
├── html_crawler/             # HTML 요소 크롤링 (로케이터)
├── html_data/                # HTML 샘플 페이지 저장
├── json_data/                # testcase.json 저장 위치
├── locators/                 # 자동 생성된 로케이터 파일 저장
├── logs/                     # Claude 응답 로그 저장
├── prompts/                  # POM구조에 맞게 프롬프트 상세 작성 
├── qa-realworld-automation/  # 테스트 자동화 메인 코드 (POM + pytest)
├── ai_run/                   # 실행 스크립트 모음 (AI 실행 자동화)
├── sql/                      # 테스트 데이터 생성 모음
└── postmain/                 # API 테스트 모음
```
