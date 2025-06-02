from prompts.common_pages import COMMON_PAGE_CONTEXT

SETTINGS_PAGE_PROMPT = COMMON_PAGE_CONTEXT + """

🌟 목표:
- 사용자 설정 페이지(Settings)의 Page Object 클래스를 생성해주세요.
- 다음 메서드를 포함해주세요:
  - enterImageUrl()
  - enterUsername()
  - enterBio()
  - enterEmail()
  - enterPassword()
  - clickUpdateButton()
  - updateSettings(image, username, bio, email, password)

- 각 메서드는 BasePage의 메서드(_click, _send_keys 등)을 사용해 구현해주세요.

📁 저장 위치:
- qa-realworld-automation/pages/settings_page.py

📌 로케이터 사용 규칙:
- 로케이터는 qa-realworld-automation/locators/settings_locators.py에 정의되어 있다고 가정합니다.
- 다음과 같이 import해서 사용해야 합니다:

  from locators.settings_locators import SettingsPageLocators as Loc

- 모든 요소는 Loc.XXX 형식으로 사용하고, 클래스 내부에 직접 정의하지 마세요.

📊 기호 작성 규칙:
- 클래스명은 `SettingsPage`, PascalCase로 작성
- 함수/변수명은 camelCase로 작성
- 명시적 대기 기능 규현
- 메서드는 간단한 설명 주석 포함

📌 예시 코드 참고:

```python
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from locators.settings_locators import SettingsPageLocators as Loc

class SettingsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def enterImageUrl(self, url):
        # 이미지 URL 입력
        self._send_keys(Loc.IMAGE_INPUT, url)

    def enterUsername(self, username):
        # 사용자 이름 입력
        self._send_keys(Loc.USERNAME_INPUT, username)

    def enterBio(self, bio):
        # 자기소개 입력
        self._send_keys(Loc.BIO_INPUT, bio)

    def enterEmail(self, email):
        # 이메일 입력
        self._send_keys(Loc.EMAIL_INPUT, email)

    def enterPassword(self, password):
        # 비밀번호 입력
        self._send_keys(Loc.PASSWORD_INPUT, password)

    def clickUpdateButton(self):
        # 업데이트 버튼 클릭
        self._click(Loc.UPDATE_BUTTON)

    def updateSettings(self, image, username, bio, email, password):
        # 설정 전체 업데이트 행사
        self.enterImageUrl(image)
        self.enterUsername(username)
        self.enterBio(bio)
        self.enterEmail(email)
        self.enterPassword(password)
        self.clickUpdateButton()
        
    📌 참고 로케이터 예시 (settings_locators.py):

        IMAGE_INPUT = (By.CSS_SELECTOR, "input[placeholder='URL of profile picture']")
        USERNAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='Username']")
        BIO_INPUT = (By.CSS_SELECTOR, "textarea[placeholder='Short bio about you']")
        EMAIL_INPUT = (By.CSS_SELECTOR, "input[type='email'][placeholder='Email']")
        PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password'][placeholder='New Password']")
        UPDATE_BUTTON = (By.CSS_SELECTOR, "button.btn-primary")


        
        
        
        """
        