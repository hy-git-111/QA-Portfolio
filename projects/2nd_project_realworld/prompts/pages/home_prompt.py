from prompts.common_pages import COMMON_PAGE_CONTEXT
                
HOME_PAGE_PROMPT = COMMON_PAGE_CONTEXT + """

🎯 목표:
- 홈(피드) 페이지의 Page Object 클래스를 생성해주세요.
- 다음 메서드를 포함해주세요: clickYourFeedTab(), clickGlobalFeedTab(), clickTag(), getArticleTitles()
- 각 메서드는 BasePage의 메서드(_click, _find_elements 등)를 사용해 구현해주세요.

📁 저장 위치:
- qa-realworld-automation/pages/home_page.py

📌 로케이터 사용 규칙:
- 로케이터는 qa-realworld-automation/locators/home_locators.py에 정의되어 있다고 가정합니다.
- 다음과 같이 import해서 사용해야 합니다:

  from locators.home_locators import HomePageLocators as Loc

- 모든 요소는 Loc.GLOBAL_TAB, Loc.TAG_ITEM 등으로 접근하며 클래스 내부에 직접 정의하지 마세요.

📐 기타 작성 규칙:
- 클래스명은 `HomePage`, PascalCase로 작성
- 함수명 및 변수명은 camelCase로 작성
- 모든 메서드는 명시적 대기 기반으로 안정적으로 작성
- 간단한 설명 주석 포함 필수

📌 예시 코드 참고:

```python
from pages.base_page import BasePage
from locators.home_locators import HomePageLocators as Loc

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def clickYourFeedTab(self):
        self._click(Loc.YOUR_FEED_TAB)

    def clickGlobalFeedTab(self):
        self._click(Loc.GLOBAL_FEED_TAB)

    def clickTag(self, tagName):
        self._click(Loc.tagElement(tagName))  # 예: 동적 태그 요소

    def getArticleTitles(self):
        elements = self._find_elements(Loc.ARTICLE_TITLE_LIST)
        return [e.text for e in elements]
        
    📌 참고 로케이터 예시 (home_locators.py):

    YOUR_FEED_TAB = (By.CSS_SELECTOR, "a.nav-link.active")
    GLOBAL_FEED_TAB = (By.CSS_SELECTOR, "a.nav-link:not(.active)")
    ARTICLE_TITLE_LIST = (By.CSS_SELECTOR, "a.preview-link h1")
    def tagElement(tagName):
        return (By.XPATH, f"//a[@class='tag-pill tag-default' and text()='{tagName}']")
    
        
        
"""
