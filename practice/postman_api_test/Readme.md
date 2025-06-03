# Postman & Newman - 사용자 등록 API 테스트
: 엘리스트랙 강의용 웹사이트를 대상으로 API 명세와 Test Case를 작성하고 사용자 등록 API 테스트를 진행한다.

## 테스트 계획  
* 테스트 목적
  - Restful API에 대한 학습 내용을 바탕으로 API 명세서를 작성한다.
  - API 명세서를 바탕으로 정상/예외 흐름에 대한 테스트 케이스를 설계한다.
  - Postman의 Runner와 Newman을 사용하여 API 테스트 자동화를 실습한다.
  - 실패/성공 결과를 확인하며 분석 방법 익힌다.

* 사용 도구
  * API 테스트 : Postman
  * 문서 작성 : Google Spreadsheet

* 대상 URL : http://localhost:5000/api/v1/users/register
  
## 테스트 설계 및 구현
* 테스트 데이터 : [data.json](https://github.com/hy-git-111/Quality-Assurance/blob/main/postman_api_test/data.json)
* [API 명세](https://github.com/hy-git-111/Quality-Assurance/blob/main/postman_api_test/API%20%EB%AA%85%EC%84%B8.pdf)
* [Test Case](https://github.com/hy-git-111/Quality-Assurance/blob/main/postman_api_test/Test%20Case.pdf)
* Postman 테스트 파일
  * Collection 파일: [Collection.json](https://github.com/hy-git-111/Quality-Assurance/blob/main/postman_api_test/collection.json)
  * 환경설정 파일 : [environment.json](https://github.com/hy-git-111/Quality-Assurance/blob/main/postman_api_test/environment.json)

## 테스트 결과 확인 및 분석
* Test Result 요약
   
   |전체 TC|Pass|Fail|
   |:--:|:--:|:--:|
   |15|9|6|

* 주요 이슈 및 개선사항
  * 비밀번호 유효성 검증 부족
    - 자리수 제한, 보안 규칙이 설정되지 않아 낮은 보안 수준의 비밀번호로도 가입이 가능함
    - 관련 Test Case : TC-009, TC-010, TC-011, TC-012
  
  * 이름에 대한 유효성 검증 부족
    - 이름에 숫자, 특수문자가 포함되어도 가입이 가능함
    - 사용자 입력 오류 방지를 위해 검증 로직 추가 필요
    - 관련 Test Case : TC-012, TC-013
  
  * 중복 사용자 처리 시 서버 오류 발생
    - 기존에 가입된 사용자명으로 가입 요청 시, 서버 전체가 종료되는 현상 발생
    - 예외처리를 통해 서버 안정성 확보 필요
    - 관련 Test Case : TC-015

* 전체 리포트 : [report.pdf](https://github.com/hy-git-111/Quality-Assurance/blob/main/postman_api_test/report.pdf)