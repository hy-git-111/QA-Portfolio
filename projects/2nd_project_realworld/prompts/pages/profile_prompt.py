from prompts.common_pages import COMMON_PAGE_CONTEXT

PROFILE_PAGE_PROMPT = COMMON_PAGE_CONTEXT + """

🌟 목표:
- 사용자 프로필 페이지(Profile)의 Page Object 클래스를 생성해주세요.
- 다음 메서드를 포함해주세요:
  - getUsername()
  - getUserBio()
  - clickFollowButton()
  - clickUnfollowButton()

- 각 메서드는 BasePage의 메서드(_click, _get_text 등)을 사용해 구현해주세요.

📁 저장 위치:
- qa-realworld-automation/pages/profile_page.py

📌 로케이터 사용 규칙:
- 로케이터는 qa-realworld-automation/locators/profile_locators.py에 정의되어 있다고 가정합니다.
- 다음과 같이 import해서 사용해야 합니다:

  from locators.profile_locators import ProfilePageLocators as Loc

- 모든 요소는 Loc.XXX 형식으로 사용하고, 클래스 내부에 직접 정의하지 마세요.

📊 기호 작성 규칙:
- 클래스명은 `ProfilePage`, PascalCase로 작성
- 함수/변수명은 camelCase로 작성
- 명시적 대기 구성
- 메서드는 간단한 설명 주석 포함

📌 예시 코드 참고:

```python
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from locators.profile_locators import ProfilePageLocators as Loc

class ProfilePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def getUsername(self):
        # 사용자 이름 가져오기
        return self._get_text(Loc.USERNAME)

    def getUserBio(self):
        # 자기소개 가져오기
        return self._get_text(Loc.USER_BIO)

    def clickFollowButton(self):
        # Follow 버튼 클릭
        self._click(Loc.FOLLOW_BUTTON)

    def clickUnfollowButton(self):
        # Unfollow 버튼 클릭
        self._click(Loc.UNFOLLOW_BUTTON)
        
    📌 참고 로케이터 예시 (profile_locators.py):

    USERNAME = (By.CSS_SELECTOR, "div.user-info h4")
    USER_BIO = (By.CSS_SELECTOR, "div.user-info p")
    FOLLOW_BUTTON = (By.CSS_SELECTOR, "button.btn-outline-secondary")
    UNFOLLOW_BUTTON = (By.CSS_SELECTOR, "button.btn-outline-secondary")

        
        """