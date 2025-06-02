from prompts.common_pages import COMMON_PAGE_CONTEXT

SIGNUP_PAGE_PROMPT = COMMON_PAGE_CONTEXT + """

🎯 목표:
- 회원가입(Signup) 페이지의 Page Object 클래스를 생성해주세요.
- 다음 메서드를 포함해주세요: enterUsername(), enterEmail(), enterPassword(), clickSignUp(), signup(), getErrorMessages()
- 각 메서드는 BasePage의 메서드(_click, _send_keys, _find_elements 등)를 사용해 구현해주세요.

📁 저장 위치:
- qa-realworld-automation/pages/signup_page.py

📌 로케이터 사용 규칙:
- 로케이터는 qa-realworld-automation/locators/signup_locators.py에 정의되어 있다고 가정합니다.
- 다음과 같이 import해서 사용해야 합니다:

  from locators.signup_locators import SignupPageLocators as Loc

- 모든 요소는 Loc.USERNAME_INPUT, Loc.EMAIL_INPUT, Loc.PASSWORD_INPUT 등으로 접근합니다.
- 로케이터는 클래스 내부에 직접 정의하지 마세요.

📐 기타 작성 규칙:
- 클래스명은 `SignupPage`, PascalCase로 작성
- 변수명과 함수명은 camelCase로 작성
- 모든 메서드는 간단한 설명 주석을 포함
- 명시적 대기 기반의 안정적인 코드로 작성

📌 예시 코드 참고:

```python
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from locators.signup_locators import SignupPageLocators as Loc

class SignupPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def enterUsername(self, username):
        self._send_keys(Loc.USERNAME_INPUT, username)

    def enterEmail(self, email):
        self._send_keys(Loc.EMAIL_INPUT, email)

    def enterPassword(self, password):
        self._send_keys(Loc.PASSWORD_INPUT, password)

    def clickSignUp(self):
        self._click(Loc.SIGNUP_BUTTON)

    def signup(self, username, email, password):
        self.enterUsername(username)
        self.enterEmail(email)
        self.enterPassword(password)
        self.clickSignUp()

    def getErrorMessages(self):
        elements = self._find_elements(Loc.ERROR_MESSAGES)
        return [e.text for e in elements]
    
    📌 참고 로케이터 예시 (signup_locators.py):

        USERNAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='Username']")
        EMAIL_INPUT = (By.CSS_SELECTOR, "input[placeholder='Email']")
        PASSWORD_INPUT = (By.CSS_SELECTOR, "input[placeholder='Password']")
        SIGNUP_BUTTON = (By.CSS_SELECTOR, "button.btn-primary")
        ERROR_MESSAGES = (By.CSS_SELECTOR, ".error-messages li")    
    
    
    
        
        """