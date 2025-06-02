from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators.editor_locators import EditorPageLocators as Loc

class EditorPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
    
    def enterTitle(self, title):
        # 게시글 제목 입력
        try:
            self._send_keys(Loc.EDITOR_TITLE_INPUT, title)
            return True
        except Exception as e:
            print(f"제목 입력 중 오류 발생: {str(e)}")
            return False
    
    def enterDescription(self, description):
        # 게시글 설명 입력
        try:
            self._send_keys(Loc.EDITOR_ABOUT_INPUT, description)
            return True
        except Exception as e:
            print(f"설명 입력 중 오류 발생: {str(e)}")
            return False
    
    def enterBody(self, body):
        # 게시글 본문 내용 입력
        try:
            self._send_keys(Loc.EDITOR_CONTENT_TEXTAREA, body)
            return True
        except Exception as e:
            print(f"본문 입력 중 오류 발생: {str(e)}")
            return False
    
    def enterTags(self, tags):
        # 게시글 태그 입력
        try:
            # 여러 태그를 입력하는 경우 처리
            if isinstance(tags, list):
                for tag in tags:
                    self._send_keys(Loc.EDITOR_TAGS_INPUT, tag + "\n")  # 엔터키로 태그 구분
            else:
                self._send_keys(Loc.EDITOR_TAGS_INPUT, tags)
            return True
        except Exception as e:
            print(f"태그 입력 중 오류 발생: {str(e)}")
            return False
    
    def clickPublishButton(self):
        # 게시 버튼 클릭
        try:
            self._click(Loc.EDITOR_PUBLISH_BUTTON)
            # 게시 후 페이지 전환 대기
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("/article/")
            )
            return True
        except Exception as e:
            print(f"게시 버튼 클릭 중 오류 발생: {str(e)}")
            return False
    
    def writeEditor(self, title, description, body, tags):
        # 새 게시글 작성 전체 프로세스 수행
        try:
            self.enterTitle(title)
            self.enterDescription(description)
            self.enterBody(body)
            self.enterTags(tags)
            return self.clickPublishButton()
        except Exception as e:
            print(f"게시글 작성 중 오류 발생: {str(e)}")
            return False
