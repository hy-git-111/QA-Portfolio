# prompts/common.py

# 📎 공통 프로젝트 정보 (모든 프롬프트 앞에 포함)
COMMON_CONTEXT = """
📎 프로젝트 정보 (공통):
- 프론트엔드: https://github.com/gothinkster/react-redux-realworld-example-app
- 백엔드: https://github.com/gothinkster/node-express-realworld-example-app
- 테스트 대상 웹사이트의 기본 접속 주소(Base URL)는 http://localhost:4100 입니다.
- 코드 이외의 모든 글은 주석 처리 해주세요.

🧩 이 프로젝트의 테스트 자동화 설정 파일들은 서로 연결되어 동작합니다:
- `config.py`는 공통 설정을 정의하며, `conftest.py`와 테스트 코드에서 import 됩니다.
- `conftest.py`는 driver, base_url fixture를 정의하며, config 설정과 pytest.ini 옵션을 활용합니다.
- `requirements.txt`는 위의 모든 설정 파일에서 사용하는 라이브러리 의존성을 관리합니다.
- `pytest.ini`는 테스트 실행 방식, 리포트 출력, 마커 설정 등을 통합 제어합니다.
"""

# ✅ config.py 생성용 프롬프트
CONFIG_PROMPT = f"""{COMMON_CONTEXT}

---

당신은 테스트 자동화 환경을 구성하는 전문가입니다.

다음 기준에 따라 실무에서 사용할 수 있는 `config.py` 파일을 생성해주세요:

- BASE_URL, TIMEOUT, HEADLESS, BROWSER_TYPE 등의 설정을 포함합니다.
- 명시적 대기(Explicit Wait) 시간인 WAIT_SECONDS와 재시도 횟수인 RETRY_COUNT 같은 설정도 함께 포함해주세요.
- 운영체제에 따라 자동으로 ChromeDriver 경로를 설정할 수 있어야 합니다 (Windows, macOS, Linux 환경 모두 지원).
- 설정은 config/ 디렉토리에 위치하며, 다른 테스트 코드에서 import해서 공통으로 사용할 수 있어야 합니다.
- 다양한 테스트 환경(로컬, 개발, 스테이징 등)에서 재사용 가능해야 합니다.
- Python 3.11 기준이며, POM + Pytest + Selenium 기반 구조입니다.

📌 추가 조건:
- 코드는 Page Object Model(POM) 기반 구조로 작성되어야 합니다.
- 각 파일은 반드시 모듈화되어야 하며, 재사용 가능해야 합니다.
- 각 파일은 명확한 역할을 가지며, 단일 책임 원칙(SRP)을 따라야 합니다.
- 모든 코드 스텝에는 주석을 작성해주세요.
- 변수명과 함수명 등은 카멜 표기법(camelCase)을 사용해주세요.
"""

# ✅ conftest.py 생성용 프롬프트
CONFTEST_PROMPT = f"""{COMMON_CONTEXT}

---

당신은 Pytest 기반 테스트 자동화 전문가입니다.

다음 기준에 따라 실무에서 사용할 수 있는 `conftest.py` 파일을 생성해주세요:

- tests/conftest.py에 위치하며, 모든 테스트 파일에서 공유될 fixture를 정의합니다.
- Selenium WebDriver 설정을 fixture로 정의하고, session 스코프를 사용합니다.
- HEADLESS, TIMEOUT, BROWSER_TYPE 설정은 config.py에서 import하여 반영합니다.
- WebDriver 설정은 운영체제에 따라 자동으로 ChromeDriver 경로를 적용할 수 있어야 합니다.
- 테스트 실패 시 스크린샷을 ./reports/screenshots/ 에 저장해주세요.
- fixture 이름은 driver, base_url을 사용해주세요.
- 명시적 대기를 위한 wait 메서드 또는 WebDriverWait 설정도 포함해주세요.
- BROWSER_TYPE은 "chrome"만 처리해도 괜찮습니다.

📌 추가 조건:
- 코드는 Page Object Model(POM) 기반 구조로 작성되어야 합니다.
- 각 파일은 반드시 모듈화되어야 하며, 재사용 가능해야 합니다.
- 각 파일은 명확한 역할을 가지며, 단일 책임 원칙(SRP)을 따라야 합니다.
- 모든 코드 스텝에는 주석을 작성해주세요.
- 변수명과 함수명 등은 카멜 표기법(camelCase)을 사용해주세요.
"""

# ✅ requirements.txt 생성용 프롬프트
REQUIREMENTS_PROMPT = f"""{COMMON_CONTEXT}

---

이 프로젝트는 Selenium + Pytest + dotenv를 사용하는 테스트 자동화 프로젝트입니다.

다음 기준에 따라 `requirements.txt` 파일을 생성해주세요:

- Python 3.11 환경 기준이며, 최신 안정 버전의 패키지를 사용해주세요.
- 필수 패키지:
  - selenium
  - pytest
  - python-dotenv (.env 환경변수 파일을 로딩하기 위함)
- 추가 도구:
  - HTML 리포트를 위한 pytest-html
  - ChromeDriver 자동 설치를 위한 webdriver-manager
  - 테스트 병렬 실행을 위한 pytest-xdist
  - flaky 테스트 재시도를 위한 pytest-rerunfailures
- 각 패키지는 `패키지명==버전` 형식으로 버전을 명시해주세요.
- 이 파일은 프로젝트 루트 경로에 위치해야 하며,
  `pip install -r requirements.txt` 명령어로 모든 의존성을 한 번에 설치할 수 있어야 합니다.

📌 추가 조건:
- 구성된 패키지 목록은 명확한 목적을 기준으로 선택되어야 하며,
  불필요한 패키지는 포함하지 마세요.
- 유지보수가 쉬운 구조로 작성해주세요.

"""

# ✅ pytest.ini 생성용 프롬프트
PYTEST_INI_PROMPT = f"""{COMMON_CONTEXT}

---

다음 기준에 따라 `pytest.ini` 파일을 생성해주세요:

- testpaths: 테스트가 위치한 디렉토리를 지정해주세요 (예: tests)
- addopts:
    - `-v`: 상세 출력
    - `--html=reports/report.html`: HTML 리포트 생성
    - `--self-contained-html`: 하나의 HTML 파일로 포함
    - `--junitxml=reports/junit.xml`: Jenkins 연동을 위한 JUnit XML 리포트 생성
- log_cli = true, log_cli_level = INFO 설정
- markers:
    - smoke: 주요 기능 확인을 위한 빠른 테스트
    - regression: 릴리즈 후 기능 회귀 테스트용
- junit_family=legacy: JUnit 리포트를 Jenkins에서 안정적으로 인식할 수 있도록 설정

📌 추가 조건:
- 각 설정 항목은 명확한 목적을 가지고 구성되어야 하며,
  다양한 테스트 환경(Jenkins, GitHub Actions 등)에서 안정적으로 실행 가능해야 합니다.
- 설정은 충돌 없이 실행 가능해야 하며, 유지보수가 쉬운 구조로 작성해주세요.

"""
