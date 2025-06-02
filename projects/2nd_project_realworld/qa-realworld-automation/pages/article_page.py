from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage
from locators.article_locators import ArticlePageLocators as Loc

class ArticlePage(BasePage):
    """
    📄 게시글 상세 페이지의 주요 기능을 정의한 Page Object 클래스
    - 게시글 정보(제목, 작성자, 본문) 조회
    - 댓글 작성, 조회, 삭제 기능 포함
    """

    def __init__(self, driver):
        # Selenium WebDriver 주입
        super().__init__(driver)
    
    def getTitle(self):
        """
        📰 게시글 제목을 가져오는 메서드
        - 성공 시 텍스트 반환
        - 실패 시 None 반환 + 에러 로그 출력
        """
        try:
            return self._get_text(Loc.ARTICLE_TITLE)
        except (TimeoutException, NoSuchElementException) as e:
            self._log_error(f"게시글 제목을 가져오는 중 오류 발생: {str(e)}")
            return None
    
    def getAuthor(self):
        """
        🧑 작성자 이름을 가져오는 메서드
        - 성공 시 작성자 이름 문자열 반환
        - 실패 시 None 반환
        """
        try:
            return self._get_text(Loc.ARTICLE_AUTHOR_LINK)
        except (TimeoutException, NoSuchElementException) as e:
            self._log_error(f"작성자 정보를 가져오는 중 오류 발생: {str(e)}")
            return None
    
    def getBody(self):
        """
        📃 게시글 본문 내용을 가져오는 메서드
        - 성공 시 본문 텍스트 반환
        - 실패 시 None 반환
        """
        try:
            return self._get_text(Loc.ARTICLE_DESCRIPTION)
        except (TimeoutException, NoSuchElementException) as e:
            self._log_error(f"게시글 내용을 가져오는 중 오류 발생: {str(e)}")
            return None
    
    def addComment(self, comment):
        """
        💬 댓글을 입력하고 등록하는 메서드
        - 입력창에 텍스트 입력 후 등록 버튼 클릭
        - 등록 완료될 때까지 해당 댓글 텍스트가 화면에 나타날 때까지 대기
        - 성공 시 True, 실패 시 False
        """
        try:
            self._send_keys(Loc.ARTICLE_COMMENT_INPUT, comment)
            self._click(Loc.ARTICLE_POST_COMMENT_BUTTON)
            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element(Loc.ARTICLE_COMMENT_LIST, comment)
            )
            return True
        except (TimeoutException, NoSuchElementException) as e:
            self._log_error(f"댓글 추가 중 오류 발생: {str(e)}")
            return False
    
    def getComments(self):
        """
        📋 화면에 표시된 모든 댓글을 가져오는 메서드
        - 댓글 DOM 요소들을 모두 찾고, 텍스트만 리스트로 반환
        - 실패 시 빈 리스트 반환
        """
        try:
            comment_elements = self._find_elements(Loc.ARTICLE_COMMENT_LIST)
            return [el.text for el in comment_elements]
        except (TimeoutException, NoSuchElementException) as e:
            self._log_error(f"댓글 목록을 가져오는 중 오류 발생: {str(e)}")
            return []
    
    def deleteCommentByIndex(self, index):
        """
        ❌ 특정 순번(index)의 댓글을 삭제하는 메서드
        - 삭제 버튼 클릭
        - 삭제 전후 댓글 개수를 비교하여 삭제 완료 대기
        - 성공 시 True, 실패 시 False
        """
        try:
            comment_delete_buttons = self._find_elements(Loc.ARTICLE_DELETE_COMMENT_BUTTONS)
            if index < len(comment_delete_buttons):
                comment_count_before = len(self._find_elements(Loc.ARTICLE_COMMENT_LIST))
                comment_delete_buttons[index].click()
                WebDriverWait(self.driver, 10).until(
                    lambda driver: len(self._find_elements(Loc.ARTICLE_COMMENT_LIST)) < comment_count_before
                )
                return True
            else:
                self._log_error(f"인덱스 {index}에 해당하는 댓글이 존재하지 않습니다.")
                return False
        except (TimeoutException, NoSuchElementException) as e:
            self._log_error(f"댓글 삭제 중 오류 발생: {str(e)}")
            return False
    
    def _log_error(self, message):
        """
        🛠 내부 에러 로깅 헬퍼 메서드
        - 모든 예외 메시지를 콘솔에 출력
        """
        print(f"[ERROR] ArticlePage: {message}")
