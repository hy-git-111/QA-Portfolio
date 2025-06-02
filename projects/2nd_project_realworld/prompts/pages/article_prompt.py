from prompts.common_pages import COMMON_PAGE_CONTEXT

ARTICLE_PAGE_PROMPT = COMMON_PAGE_CONTEXT + """

🌟 목표:
- 게시글 상세 페이지(Article)의 Page Object 클래스를 생성해주세요.
- 다음 메서드를 포함해주세요:
  - getTitle()
  - getAuthor()
  - getBody()
  - addComment(comment)
  - getComments()
  - deleteCommentByIndex(index)

- 각 메서드는 BasePage의 메서드(_click, _send_keys, _get_text 등)을 사용해 구현해주세요.

📁 저장 위치:
- qa-realworld-automation/pages/article_page.py

📌 로케이터 사용 규칙:
- 로케이터는 qa-realworld-automation/locators/article_locators.py에 정의되어 있다고 가정합니다.
- 다음과 같이 import해서 사용해야 합니다:

  from locators.article_locators import ArticlePageLocators as Loc

- 모든 요소는 Loc.XXX 형식으로 사용하고, 클래스 내부에 직접 정의하지 마세요.

📊 기호 작성 규칙:
- 클래스명은 `ArticlePage`, PascalCase로 작성
- 함수/변수명은 camelCase로 작성
- 명시적 대기 규칙 등록
- 메서드는 간단한 설명 주석 포함

📌 예시 코드 참고:

```python
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from locators.article_locators import ArticlePageLocators as Loc

class ArticlePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def getTitle(self):
        # 게시글 제목 가져오기
        return self._get_text(Loc.TITLE)

    def getAuthor(self):
        # 작성자 이름 가져오기
        return self._get_text(Loc.AUTHOR)

    def getBody(self):
        # 게시글 내용 가져오기
        return self._get_text(Loc.BODY)

    def addComment(self, comment):
        # 댓글 입력 및 추가
        self._send_keys(Loc.COMMENT_INPUT, comment)
        self._click(Loc.POST_COMMENT_BUTTON)

    def getComments(self):
        # 댓글 목록 가져오기
        comment_elements = self._find_elements(Loc.COMMENT_LIST)
        return [el.text for el in comment_elements]

    def deleteCommentByIndex(self, index):
        # 특정 댓글(index) 삭제
        comment_delete_buttons = self._find_elements(Loc.DELETE_COMMENT_BUTTONS)
        if index < len(comment_delete_buttons):
            comment_delete_buttons[index].click()

📌 참고 로케이터 예시 (article_locators.py):

TITLE = (By.CSS_SELECTOR, "a.preview-link h1")
AUTHOR = (By.CSS_SELECTOR, "a.author")
BODY = (By.CSS_SELECTOR, "div.article-content p")
COMMENT_INPUT = (By.CSS_SELECTOR, "textarea[placeholder='Write a comment...']")
POST_COMMENT_BUTTON = (By.CSS_SELECTOR, "button.btn-primary")
COMMENT_LIST = (By.CSS_SELECTOR, "div.card-text")
DELETE_COMMENT_BUTTONS = (By.CSS_SELECTOR, "i.ion-trash-a")

"""
