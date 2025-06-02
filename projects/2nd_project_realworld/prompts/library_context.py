# prompts/library_context.py

COMMON_LIBRARY_CONTEXT = """
📦 프로젝트 전체 구조 안내 (테스트 자동화 프레임워크)

이 프레임워크는 Page Object Model(POM)을 기반으로 구성된 Selenium + Pytest 자동화 테스트 프로젝트입니다.
모든 구성 요소는 명확히 역할이 분리되어 있으며, 서로 연결된 구조로 동작합니다.

📁 디렉토리 구조:
qa-realworld-automation/
├── pages/             # 각 페이지의 Page Object 클래스
│   └── base_page.py   # 모든 페이지가 상속하는 공통 클래스
├── utils/             # 유틸리티 함수/클래스 (예: 로깅, 헬퍼)
│   └── logger.py      # 로그 설정 파일
├── locators/          # 페이지별 요소 로케이터 (UPPER_SNAKE_CASE)
├── config/            # 공통 설정: config.py, conftest.py
├── tests/             # pytest 기반 테스트 코드 (각 Page 클래스 import)
├── reports/           # 테스트 실행 리포트 (HTML 등)
├── data/              # 테스트 데이터 파일 (JSON, CSV 등)

📌 공통 규칙:
- 모든 Page는 base_page.BasePage를 상속받아야 합니다.
- Page는 해당 로케이터를 다음과 같이 import 해서 사용해야 합니다:

    from locators.<파일명> import <클래스명> as Loc
    예: from locators.login_locators import LoginPageLocators as Loc

- 로케이터는 반드시 외부 파일(locators/*.py)에 정의하며, Page 클래스 내부에 직접 작성하지 않습니다.
- 모든 locator 변수는 UPPER_SNAKE_CASE 표기법을 사용합니다 (예: USERNAME_INPUT)
- 함수 및 변수명은 camelCase, 클래스명은 PascalCase 표기법을 사용합니다.

🧪 테스트 구조:
- 모든 테스트는 `qa-realworld-automation/tests/` 디렉토리 내에서 작성되며 pytest 기반입니다.
- 테스트 파일은 test_*.py 형식으로 이름을 설정하고, Page 객체를 import 하여 기능 검증을 수행합니다.
- pytest.ini, config.py, conftest.py는 테스트 실행, 설정 주입, HTML 리포트 생성을 자동화합니다.
- 테스트 실패 시 스크린샷을 reports/screenshots/ 에 자동 저장합니다.

🧠 Claude 또는 AI가 이 구조를 기준으로 코드를 생성하거나 평가해야 할 때에는:
- 이 문서를 사전 입력(prompt)으로 포함시켜야 합니다.
- 개별 프롬프트마다 이 구조를 따른다는 가정 하에 동작해야 합니다.

✅ 이 구조는 완전히 모듈화되어 있으며, 각 구성 요소는 명확하게 연결되어 동작하도록 설계되었습니다.
"""
