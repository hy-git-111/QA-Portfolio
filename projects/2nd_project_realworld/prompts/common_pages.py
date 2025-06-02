COMMON_PAGE_CONTEXT = """
📎 프로젝트 정보 (공통):
- 프론트엔드: https://github.com/gothinkster/react-redux-realworld-example-app
- 백엔드: https://github.com/gothinkster/node-express-realworld-example-app
- 테스트 대상 웹사이트의 기본 접속 주소(Base URL)는 http://localhost:4100 입니다.
- 코드 이외의 모든 설명 문장은 반드시 주석(#)으로 작성해주세요.

🧩 페이지 객체 구조 안내:
- 모든 페이지 객체는 qa-realworld-automation/pages/ 디렉토리에 저장됩니다.
- 각 클래스는 반드시 BasePage를 상속받아야 하며, 공통 메서드(_click, _send_keys 등)를 활용합니다.
- 요소 로케이터는 qa-realworld-automation/locators/ 디렉토리에 분리 저장되며,
  페이지 객체 파일에서는 반드시 다음과 같이 import해서 사용해야 합니다:

    from locators.<파일명> import <클래스명> as Loc
    예: from locators.login_page_locators import LoginPageLocators as Loc

🧪 테스트 코드와 연결:
- 생성된 페이지 객체는 tests/ 디렉토리의 테스트 코드에서 import하여 사용됩니다.
- 따라서 클래스와 메서드는 반드시 모듈화되어 있어야 하며, 재사용 가능해야 합니다.

📐 개발 규칙 (공통 적용):
- Page Object Model(POM) 구조 기반으로 작성해야 합니다.
- 단일 책임 원칙(SRP)을 따라야 하며, 각 메서드는 명확한 동작을 수행해야 합니다.
- WebDriverWait을 활용한 **명시적 대기(Explicit Wait)**를 기본으로 사용해야 합니다.
- 예외 처리 및 오류 메시지 출력을 포함해야 하며, 테스트 안정성을 고려해야 합니다.
- 변수명과 함수명은 **camelCase** 로 작성해야 합니다.
- 모든 메서드는 간단한 설명 주석과 함께 작성되어야 합니다.
"""
