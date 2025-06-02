from pages.base_page import BasePage
from locators.home_locators import HomePageLocators as Loc
from selenium.common.exceptions import TimeoutException
import logging

class HomePage(BasePage):
    """
    🔍 홈(피드) 페이지 Page Object 클래스
    - 피드 탭 클릭, 태그 클릭, 기사 제목/태그 확인 기능을 포함합니다.
    """

    def __init__(self, driver):
        """🧱 WebDriver 초기화"""
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)

    def getNavigateUserName(self):
        """
        📰 게시글 제목을 가져오는 메서드
        - 성공 시 텍스트 반환
        - 실패 시 None 반환 + 에러 로그 출력
        """
        try:
            return self._get_text(Loc.ARTICLE_TITLE)
        except (TimeoutException) as e:
            self._log_error(f"네비게이션의 사용자명을을 가져오는 중 오류 발생: {str(e)}")
            return None
    

    def clickYourFeedTab(self):
        """📰 'Your Feed' 탭 클릭"""
        try:
            # self._click(Loc.TAB_YOUR_FEED)  # ⛔ 이전 방식 (사용 중지)
            self._click(Loc.HOME_YOUR_FEED_LINK)  # ✅ 일관된 네이밍으로 변경
            self.logger.info("Clicked on Your Feed tab")
        except TimeoutException:
            self.logger.error("Your Feed 탭 클릭 실패")
            raise

    def clickGlobalFeedTab(self):
        """📰 'Global Feed' 탭 클릭"""
        try:
            # self._click(Loc.TAB_GLOBAL_FEED)  # ⛔ 이전 방식 (사용 중지)
            self._click(Loc.HOME_GLOBAL_FEED_LINK)  # ✅ 로케이터 이름 통일
            self.logger.info("Clicked on Global Feed tab")
        except TimeoutException:
            self.logger.error("Global Feed 탭 클릭 실패")
            raise

    def clickTag(self, tagName):
        """
        🏷️ 인기 태그 중 지정된 태그 클릭
        Args:
            tagName (str): 클릭할 태그 텍스트
        """
        try:
            # ⛔ CSS Selector에서 contains 사용 불가 → 실패 가능성 있음
            # tag_locator = (Loc.HOME_POPULAR_TAG[0], Loc.HOME_POPULAR_TAG[1].replace("a.tag-default", f"a.tag-default:contains('{tagName}')"))

            # ✅ XPath 사용: 텍스트 일치 태그 선택
            tag_locator = (Loc.HOME_POPULAR_TAG_BY_TEXT[0], Loc.HOME_POPULAR_TAG_BY_TEXT[1].format(tagName))
            self._click(tag_locator)
            self.logger.info(f"'{tagName}' 태그 클릭 완료")
        except TimeoutException:
            self.logger.error(f"'{tagName}' 태그 클릭 실패")
            raise

    def getArticleTitles(self):
        """
        📄 현재 페이지에 표시된 모든 게시글 제목 가져오기
        Returns:
            list[str]: 게시글 제목 리스트
        """
        try:
            elements = self._find_elements(Loc.HOME_ARTICLE_TITLE)
            titles = [element.text for element in elements]
            self.logger.info(f"{len(titles)}개의 게시글 제목을 확인했습니다.")
            return titles
        except TimeoutException:
            self.logger.error("게시글 제목 탐색 실패")
            return []

    def isArticleVisible(self, title):
        """
        👀 특정 제목의 게시글이 보이는지 확인
        Args:
            title (str): 찾고자 하는 게시글 제목
        Returns:
            bool: 화면에 존재 여부
        """
        try:
            # ⛔ contains()는 CSS에선 불가 → XPath 또는 정확 매칭 필요
            # article_locator = (Loc.HOME_ARTICLE_TITLE[0], Loc.HOME_ARTICLE_TITLE[1].replace("h1", f"h1:contains('{title}')"))

            # ✅ 정적인 방식 사용 (단일 제목이 유일하게 존재한다고 가정)
            elements = self._find_elements(Loc.HOME_ARTICLE_TITLE)
            return any(title in e.text for e in elements)
        except TimeoutException:
            return False

    def getTagList(self):
        """
        🏷️ 현재 사이드바에서 보이는 인기 태그 목록 가져오기
        Returns:
            list[str]: 태그 이름 리스트
        """
        try:
            elements = self._find_elements(Loc.HOME_POPULAR_TAGS_LIST)
            tags = [element.text for element in elements]
            self.logger.info(f"{len(tags)}개의 인기 태그를 확인했습니다.")
            return tags
        except TimeoutException:
            self.logger.error("인기 태그 목록 탐색 실패")
            return []

    def isPageLoaded(self):
        """
        ✅ 페이지 주요 구성 요소가 보이는지 확인
        Returns:
            bool: 페이지가 완전히 로드되었는지 여부
        """
        try:
            return (self.is_element_visible(Loc.HOME_FEED_TOGGLE) and 
                    self.is_element_visible(Loc.HOME_ARTICLE_PREVIEW))
        except TimeoutException:
            return False
