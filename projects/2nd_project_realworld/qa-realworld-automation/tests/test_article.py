import os
import json
import pytest
import inspect
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# 페이지 객체 임포트
from pages.settings_page import SettingsPage
from pages.article_page import ArticlePage
from pages.profile_page import ProfilePage
from pages.editor_page import EditorPage
from pages.signup_page import SignupPage
from pages.login_page import LoginPage
from pages.home_page import HomePage

# 로케이터 임포트
from locators.settings_locators import SettingsPageLocators as SettingsLoc
from locators.profile_locators import ProfilePageLocators as ProfileLoc
from locators.signup_locators import SignupPageLocators as SignupLoc
from locators.editor_locators import EditorPageLocators as EditorLoc
from locators.login_locators import LoginPageLocators as LoginLoc
from locators.home_locators import HomePageLocators as HomeLoc
from locators.article_locators import ArticlePageLocators as ArticleLoc

# 유틸리티 임포트
from utils.logger import setup_logger
from config import config
from utils import time_utils

def loadTestData():
    # 테스트 데이터 로드 함수
    dataFilePath = os.path.join(config.TEST_DATA_DIR, "test_data.json")
    with open(dataFilePath, 'r', encoding='utf-8') as file:
        return json.load(file)

logger = setup_logger(__name__)

class TestPopularTags:
    """Popular Tags 관련 테스트 클래스"""
    
    @pytest.mark.data_required
    def test_empty_popular_tags(self, driver):
        # ARTI-PERF-01: 게시글이 없을 때 Popular Tags 섹션 표시 확인

        try:

            # 테스트 데이터 로드
            testData = loadTestData()["EmptyPopularTagUser"]
            
            # 로그인
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])

            # 홈페이지 접속
            homePage = HomePage(driver)
            driver.get(home_page.url)
            
            # Popular Tags 섹션 제목 확인
            popular_tags_title = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(HomeLoc.POPULAR_TAGS_TEXT)
            )
            
            # Popular Tags 제목이 표시되는지 확인
            assert popular_tags_title.is_displayed(), "Popular Tags 제목이 표시되지 않습니다."
            
            # 태그 목록 가져오기
            tag_list = homePage.getTagList()
            
            # 태그 목록이 비어있는지 확인
            assert len(tag_list) == 0, f"게시글이 없는데도 태그 목록이 표시됩니다: {tag_list}"
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"빈 Popular Tags 테스트 실패: {str(e)}")
            raise
        
    
    @pytest.mark.data_required
    def test_popular_tags_visibility(self, driver):
        # ARTI-PERF-02: Popular Tags 섹션에 동일한 태그가 등록된 게시글이 노출되는지 확인

        try:
            # 테스트 데이터 로드
            testData = loadTestData()["TwoArticlesUser"]

            # 로그인
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])

            # 홈페이지 접속
            homePage = HomePage(driver)
            
            # Popular Tags 섹션 확인
            tag_list = homePage.getTagList()
            
            # 태그 목록이 존재하는지 확인
            assert len(tag_list) > 0, "Popular Tags 목록이 비어 있습니다."
            
            # 첫 번째 태그 클릭하여 해당 태그의 게시글 확인
            first_tag = tag_list[0]
            homePage.clickTag(first_tag)
            
            # 해당 태그로 필터링된 게시글 목록 확인
            articleTitles = homePage.getArticleTitles()
            
            # 최소 2개 이상의 게시글이 있는지 확인
            assert len(articleTitles) >= 2, f"태그 '{first_tag}'로 필터링된 게시글이 2개 미만입니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"Popular Tags 노출 테스트 실패: {str(e)}")
    

    @pytest.mark.data_required
    def test_popular_tags_max_count(self, driver):
        # ARTI-PERF-03: Popular Tags 섹션에 최대 10개의 태그만 노출되는지 확인
        
        try:
            # 테스트 데이터 로드
            testData = loadTestData()["TwoArticlesUser"]

            # 로그인
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])

            # 홈페이지 접속
            homePage = HomePage(driver)
            
            # Popular Tags 섹션 확인
            tag_list = homePage.getTagList()
            
            # 태그 목록이 존재하는지 확인
            assert len(tag_list) > 0, "Popular Tags 목록이 비어 있습니다."
            
            # 최대 10개의 태그만 노출되는지 확인
            assert len(tag_list) <= 10, f"Popular Tags 목록에 10개 이상의 태그({len(tag_list)}개)가 노출됩니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"Popular Tags 최대 개수 테스트 실패: {str(e)}")
    

    @pytest.mark.data_required
    def test_longTag_display(self, driver):
        # ARTI-PERF-04: 긴 태그가 화면 레이아웃을 벗어나지 않고 정상적으로 표시되는지 확인
        
        try:
            # 테스트 데이터 로드
            testData = loadTestData()["TwoArticlesUser"]

            # 로그인
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])

            # 홈페이지 접속
            homePage = HomePage(driver)
            
            # Popular Tags 섹션 확인
            tag_list = homePage.getTagList()
            
            # 태그 목록이 존재하는지 확인
            assert len(tag_list) > 0, "Popular Tags 목록이 비어 있습니다."
            
            # 긴 태그가 있는지 확인 (20자 이상)
            longTags = [tag for tag in tag_list if len(tag) >= 20]
            assert len(longTags) > 0, "20자 이상의 긴 태그가 존재하지 않습니다."
            
            # 긴 태그가 정상적으로 표시되는지 확인 (요소가 화면에 보이는지)
            for longTag in longTags:
                # 태그 요소가 화면에 보이는지 확인
                is_visible = homePage.is_element_visible(HomeLoc.TAG_ITEM(longTag))
                assert is_visible, f"긴 태그 '{longTag}'가 화면에 정상적으로 표시되지 않습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"긴 태그 표시 테스트 실패: {str(e)}")
    
    @pytest.mark.data_required
    def test_tag_click_navigation(self, driver):
        # ARTI-PERF-05: 태그 클릭 시 해당 태그의 게시글 목록 페이지로 이동하는지 확인
        
        try:
            # 테스트 데이터 로드
            testData = loadTestData()["TwoArticlesUser"]

            # 로그인
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])

            # 홈페이지 접속
            homePage = HomePage(driver)
            
            # Popular Tags 섹션 확인
            tag_list = homePage.getTagList()
            
            # 태그 목록이 존재하는지 확인
            assert len(tag_list) > 0, "Popular Tags 목록이 비어 있습니다."
            
            # 첫 번째 태그 선택
            selected_tag = tag_list[0]
            
            # 태그 클릭
            homePage.clickTag(selected_tag)
            
            # 새 네비바가 표시되는지 확인 (태그 이름이 포함된 네비바)
            tag_nav_locator = (HomeLoc.HOME_POPULAR_TAG_BY_TEXT[0], HomeLoc.HOME_POPULAR_TAG_BY_TEXT[1].format(selected_tag))
            is_tag_nav_visible = homePage.is_element_visible(tag_nav_locator)
            assert is_tag_nav_visible, f"태그 '{selected_tag}'를 클릭한 후 새 네비바가 표시되지 않습니다."
            
            # 해당 태그로 필터링된 게시글이 표시되는지 확인
            articleTitles = homePage.getArticleTitles()
            assert len(articleTitles) > 0, f"태그 '{selected_tag}'로 필터링된 게시글이 없습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"태그 클릭 네비게이션 테스트 실패: {str(e)}")


class TestArticleCreation:
    """게시글 작성 관련 테스트 클래스"""
    
    @pytest.mark.data_required
    def test_article_creation_with_tag(self, driver):
        """
        테스트 시나리오: 태그를 포함한 게시글 작성 기능 확인
        
        사전 조건:
        - 사용자가 로그인 되어 있고, 게시글 작성 페이지에 접근한다.
        
        재현 절차:
        1. "Article Title" 필드에 유효한 제목을 입력한다.
        2. "What's this article about?" 필드에 유효한 설명을 입력한다.
        3. "Write your article (in markdown)" 필드에 1자 이상의 유효한 본문 내용을 입력한다.
        4. "Enter tags" 필드에 유효한 태그를 입력하고 Enter 키를 누른다.
        5. [Publish Article] 버튼을 클릭한다.
        
        기대 결과:
        - 게시글이 정상적으로 등록되고, 작성된 게시글 상세 페이지로 이동한다.
        """
        try:
            # 테스트 데이터 로드
            testData = loadTestData()["article_creation"]
            
            # 로그인
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 게시글 작성 페이지로 이동
            editorPage = EditorPage(driver)
            
            # 게시글 작성
            article_title = testData["title"]
            article_description = testData["description"]
            article_body = testData["body"]
            article_tag = testData["tag"]
            
            editorPage.enterTitle(article_title)
            editorPage.enterDescription(article_description)
            editorPage.enterBody(article_body)
            editorPage.enterTags(article_tag)
            
            # 게시글 발행
            editorPage.clickPublishButton()
            
            # 게시글 상세 페이지로 이동했는지 확인
            article_page = ArticlePage(driver)
            
            # 게시글 제목 확인
            actual_title = article_page.getTitle()
            assert actual_title == article_title, f"게시글 제목이 일치하지 않습니다. 예상: {article_title}, 실제: {actual_title}"
            
            # 게시글 내용 확인
            actual_body = article_page.getBody()
            assert article_body in actual_body, f"게시글 내용이 포함되어 있지 않습니다. 예상 내용이 포함되어야 함: {article_body}"
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"게시글 작성 테스트 실패: {str(e)}")


class TestArticleCreation:
    """게시글 작성 관련 테스트 클래스"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """각 테스트 전에 로그인 및 에디터 페이지로 이동하는 설정"""
        try:
            # 테스트 데이터 로드
            testData = loadTestData()["login"]
            
            # 로그인 진행
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 에디터 페이지로 이동
            driver.get("https://demo.realworld.io/#/editor")
            
            # 에디터 페이지 객체 생성
            self.editorPage = EditorPage(driver)
            
            # 드라이버 저장
            self.driver = driver
            
        except Exception as e:
            logger.error(f"Setup failed: {str(e)}")
            pytest.fail(f"Setup failed: {str(e)}")
    
    @pytest.mark.data_required
    def test_empty_all_fields(self, driver):
        """
        테스트 ID: unnamed
        시나리오: 모든 필드가 비어있는 상태에서 게시글 등록 시도
        
        사전 조건: 사용자가 로그인 되어 있고, 게시글 작성 페이지에 접근한다
        
        재현 절차:
        1. 모든 필드를 비워둔다.
        2. [Publish Article] 버튼을 클릭한다.
        
        기대 결과: 에러 페이지로 이동되며 게시글은 등록되지 않는다.
        """
        try:
            # 모든 필드가 비어있는 상태에서 게시글 등록 시도
            self.editorPage.clickPublishButton()
            
            # 에러 페이지로 이동했는지 확인
            currentUrl = self.editor_page.get_current_url()
            assert "error" in currentUrl.lower(), "에러 페이지로 이동되지 않았습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"테스트 실패: {str(e)}")
    
    @pytest.mark.data_required
    def test_empty_title_field(self, driver):
        """
        테스트 ID: unnamed
        시나리오: 제목 필드가 비어있는 상태에서 게시글 등록 시도
        
        사전 조건: 사용자가 로그인 되어 있고, 게시글 작성 페이지에 접근한다
        
        재현 절차:
        1. "Article Title" 필드를 비워둔다.
        2. [Publish Article] 버튼을 클릭한다.
        
        기대 결과: 에러 페이지로 이동되며 게시글은 등록되지 않는다.
        """
        try:
            # 테스트 데이터 로드
            testData = loadTestData()["article"]
            
            # 제목을 제외한 필드 입력
            self.editorPage.enterDescription(testData["description"])
            self.editorPage.enterBody(testData["body"])
            self.editorPage.enterTags(testData["tags"])
            
            # 게시글 등록 시도
            self.editorPage.clickPublishButton()
            
            # 에러 페이지로 이동했는지 확인
            currentUrl = self.editor_page.get_current_url()
            assert "error" in currentUrl.lower(), "에러 페이지로 이동되지 않았습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"테스트 실패: {str(e)}")
    
    @pytest.mark.data_required
    def test_empty_description_field(self, driver):
        """
        테스트 ID: unnamed
        시나리오: 설명 필드가 비어있는 상태에서 게시글 등록 시도
        
        사전 조건: 사용자가 로그인 되어 있고, 게시글 작성 페이지에 접근한다
        
        재현 절차:
        1. "What's this article about?" 필드를 비워둔다.
        2. [Publish Article] 버튼을 클릭한다.
        
        기대 결과: 에러 페이지로 이동되며 게시글은 등록되지 않는다.
        """
        try:
            # 테스트 데이터 로드
            testData = loadTestData()["article"]
            
            # 설명을 제외한 필드 입력
            self.editorPage.enterTitle(testData["title"])
            self.editorPage.enterBody(testData["body"])
            self.editorPage.enterTags(testData["tags"])
            
            # 게시글 등록 시도
            self.editorPage.clickPublishButton()
            
            # 에러 페이지로 이동했는지 확인
            currentUrl = self.editor_page.get_current_url()
            assert "error" in currentUrl.lower(), "에러 페이지로 이동되지 않았습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"테스트 실패: {str(e)}")
    
    @pytest.mark.data_required
    def test_empty_body_field(self, driver):
        """
        테스트 ID: unnamed
        시나리오: 본문 필드가 비어있는 상태에서 게시글 등록 시도
        
        사전 조건: 사용자가 로그인 되어 있고, 게시글 작성 페이지에 접근한다
        
        재현 절차:
        1. "Write your article (in markdown)" 필드를 비워둔다.
        2. [Publish Article] 버튼을 클릭한다.
        
        기대 결과: 에러 페이지로 이동되며 게시글은 등록되지 않는다.
        """
        try:
            # 테스트 데이터 로드
            testData = loadTestData()["article"]
            
            # 본문을 제외한 필드 입력
            self.editorPage.enterTitle(testData["title"])
            self.editorPage.enterDescription(testData["description"])
            self.editorPage.enterTags(testData["tags"])
            
            # 게시글 등록 시도
            self.editorPage.clickPublishButton()
            
            # 에러 페이지로 이동했는지 확인
            currentUrl = self.editor_page.get_current_url()
            assert "error" in currentUrl.lower(), "에러 페이지로 이동되지 않았습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"테스트 실패: {str(e)}")
    
    @pytest.mark.data_required
    def test_empty_tags_field(self, driver):
        """
        테스트 ID: unnamed
        시나리오: 태그 필드가 비어있는 상태에서 게시글 등록 시도
        
        사전 조건: 사용자가 로그인 되어 있고, 게시글 작성 페이지에 접근한다
        
        재현 절차:
        1. "Enter tags" 필드를 비워둔다.
        2. [Publish Article] 버튼을 클릭한다.
        
        기대 결과: 에러 페이지로 이동되며 게시글은 등록되지 않는다.
        """
        try:
            # 테스트 데이터 로드
            testData = loadTestData()["article"]
            
            # 태그를 제외한 필드 입력
            self.editorPage.enterTitle(testData["title"])
            self.editorPage.enterDescription(testData["description"])
            self.editorPage.enterBody(testData["body"])
            
            # 게시글 등록 시도
            self.editorPage.clickPublishButton()
            
            # 에러 페이지로 이동했는지 확인
            currentUrl = self.editor_page.get_current_url()
            assert "error" in currentUrl.lower(), "에러 페이지로 이동되지 않았습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"테스트 실패: {str(e)}")
            
class TestArticleCreation:
    """게시글 작성 관련 테스트 클래스"""

    @pytest.mark.data_required
    def test_duplicate_article_title(self, driver):
        """
        동일한 제목의 게시글 등록 시도 시 오류 메시지 확인 테스트
        
        사전 조건: 사용자가 로그인 되어 있으며, 동일한 제목의 게시글이 이미 등록되어 있다.
        재현 절차:
        1. 게시글 작성 페이지로 이동한다.
        2. 이미 등록된 게시글과 정확히 동일한 제목으로 새로운 게시글을 작성 시도한다.
        3. [Publish Article] 버튼을 클릭한다.
        기대 결과: 동일한 제목으로는 게시글을 등록할 수 없다는 오류 메시지가 표시된다.
        """
        try:
            # 테스트 데이터 로드
            testData = loadTestData()["duplicate_article"]
            
            # 로그인 (사전 조건)
            loginPage = LoginPage(driver)
            loginPage.login(testData["email"], testData["password"])
            
            # 게시글 작성 페이지로 이동
            editorPage = EditorPage(driver)
            driver.get(testData["editor_url"])
            
            # 이미 등록된 게시글과 동일한 제목으로 새 게시글 작성
            editorPage.enterTitle(testData["duplicate_title"])
            editorPage.enterDescription(testData["description"])
            editorPage.enterBody(testData["body"])
            
            # Publish Article 버튼 클릭
            editorPage.clickPublishButton()
            
            # 오류 메시지 확인
            assert editor_page.is_element_visible(EditorLoc.ERROR_MESSAGE), "오류 메시지가 표시되지 않았습니다."
            errorMessage = driver.find_element(*EditorLoc.ERROR_MESSAGE).text
            assert "title" in error_message.lower(), f"제목 중복 관련 오류 메시지가 표시되지 않았습니다. 표시된 메시지: {error_message}"
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 중복 제목 게시글 등록 테스트 성공")
        except Exception as e:
            logger.warning(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"중복 제목 게시글 등록 테스트 실패: {str(e)}")
            raise

    @pytest.mark.data_required
    def test_markdown_rendering(self, driver):
        """
        마크다운 문법이 상세 페이지에서 정상적으로 렌더링되는지 확인하는 테스트
        
        사전 조건: 사용자가 로그인 되어 있고, 게시글 작성 페이지에 접근한다
        재현 절차:
        1. "Article Title" 필드에 유효한 제목을 입력한다.
        2. "What's this article about?" 필드에 유효한 설명을 입력한다.
        3. "Write your article (in markdown)" 필드에 1자 이상의 유효한 본문 내용을 입력한다.
        4. "Enter tags" 필드에 유효한 태그를 입력하고 Enter 키를 누른다
        5. [Publish Article] 버튼을 클릭한다.
        기대 결과: 입력한 마크다운 문법이 상세 페이지에서 정상적으로 렌더링 된다.
        """
        try:
            # 테스트 데이터 로드
            testData = loadTestData()["markdown_article"]
            
            # 로그인 (사전 조건)
            loginPage = LoginPage(driver)
            loginPage.login(testData["email"], testData["password"])
            
            # 게시글 작성 페이지로 이동
            editorPage = EditorPage(driver)
            driver.get(testData["editor_url"])
            
            # 게시글 작성
            editorPage.enterTitle(testData["title"])
            editorPage.enterDescription(testData["description"])
            editorPage.enterBody(testData["markdown_body"])
            editorPage.enterTags(testData["tag"])
            
            # Publish Article 버튼 클릭
            editorPage.clickPublishButton()
            
            # 게시글 상세 페이지로 이동 확인
            article_page = ArticlePage(driver)
            assert article_page.is_element_present(ArticleLoc.ARTICLE_TITLE), "게시글 상세 페이지로 이동하지 않았습니다."
            
            # 마크다운 렌더링 확인
            article_body = article_page.getBody()
            
            # 제목 렌더링 확인 (h1 태그)
            assert "<h1>" in article_body, "마크다운 제목(#)이 정상적으로 렌더링되지 않았습니다."
            
            # 굵은 텍스트 렌더링 확인 (strong 태그)
            assert "<strong>" in article_body, "마크다운 굵은 텍스트(**)가 정상적으로 렌더링되지 않았습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 마크다운 렌더링 테스트 성공")
        except Exception as e:
            logger.warning(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"마크다운 렌더링 테스트 실패: {str(e)}")
            raise

    @pytest.mark.data_required
    def test_tag_without_enter(self, driver):
        """
        Enter 키를 누르지 않고 태그 입력 후 게시글 등록 테스트
        
        사전 조건: 사용자가 로그인 되어 있고, 게시글 작성 페이지에 접근한다
        재현 절차:
        1. "Enter tags" 필드에 태그 내용을 입력한 후 Enter 키를 누르지 않고 [Publish Article] 버튼을 클릭한다.
        기대 결과: "Enter tags" 필드에 입력된 내용이 태그로 추가되지 않고 게시글이 등록된다.
        """
        try:
            # 테스트 데이터 로드
            testData = loadTestData()["tag_without_enter"]
            
            # 로그인 (사전 조건)
            loginPage = LoginPage(driver)
            loginPage.login(testData["email"], testData["password"])
            
            # 게시글 작성 페이지로 이동
            editorPage = EditorPage(driver)
            driver.get(testData["editor_url"])
            
            # 게시글 작성
            editorPage.enterTitle(testData["title"])
            editorPage.enterDescription(testData["description"])
            editorPage.enterBody(testData["body"])
            
            # 태그 입력 (Enter 키 누르지 않음)
            driver.find_element(*EditorLoc.TAG_INPUT).send_keys(testData["tag"])
            
            # Publish Article 버튼 클릭
            editorPage.clickPublishButton()
            
            # 게시글 상세 페이지로 이동 확인
            article_page = ArticlePage(driver)
            assert article_page.is_element_present(ArticleLoc.ARTICLE_TITLE), "게시글 상세 페이지로 이동하지 않았습니다."
            
            # 태그가 추가되지 않았는지 확인
            if article_page.is_element_present(ArticleLoc.TAGS):
                tags = driver.find_elements(*ArticleLoc.TAGS)
                tagTexts = [tag.text for tag in tags]
                assert testData["tag"] not in tagTexts, f"Enter 키를 누르지 않았는데도 태그({testData['tag']})가 추가되었습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} Enter 키 없이 태그 입력 테스트 성공")
        except Exception as e:
            logger.warning(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"Enter 키 없이 태그 입력 테스트 실패: {str(e)}")
            raise

    @pytest.mark.data_required
    def test_empty_tag_not_added(self, driver):
        """
        빈 태그가 추가되지 않는지 확인하는 테스트
        
        사전 조건: 사용자가 로그인 되어 있고, 게시글 작성 페이지에 접근한다
        재현 절차:
        1. "Enter tags" 필드에 아무것도 입력하지 않고 Enter 키를 누른다. (여러 번 반복)
        2. [Publish Article] 버튼을 클릭한다.
        3. 등록된 게시글을 확인한다.
        기대 결과: 빈 태그가 추가되지 않는다.
        """
        try:
            # 테스트 데이터 로드
            testData = loadTestData()["empty_tag"]
            
            # 로그인 (사전 조건)
            loginPage = LoginPage(driver)
            loginPage.login(testData["email"], testData["password"])
            
            # 게시글 작성 페이지로 이동
            editorPage = EditorPage(driver)
            driver.get(testData["editor_url"])
            
            # 게시글 작성
            editorPage.enterTitle(testData["title"])
            editorPage.enterDescription(testData["description"])
            editorPage.enterBody(testData["body"])
            
            # 빈 태그 입력 시도 (여러 번 반복)
            tag_input = driver.find_element(*EditorLoc.TAG_INPUT)
            for _ in range(3):  # 3번 반복
                tag_input.send_keys("")
                tag_input.send_keys("\n")  # Enter 키 입력
            
            # Publish Article 버튼 클릭
            editorPage.clickPublishButton()
            
            # 게시글 상세 페이지로 이동 확인
            article_page = ArticlePage(driver)
            assert article_page.is_element_present(ArticleLoc.ARTICLE_TITLE), "게시글 상세 페이지로 이동하지 않았습니다."
            
            # 빈 태그가 추가되지 않았는지 확인
            if article_page.is_element_present(ArticleLoc.TAGS):
                tags = driver.find_elements(*ArticleLoc.TAGS)
                assert len(tags) == 0, "빈 태그가 추가되었습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 빈 태그 추가 방지 테스트 성공")
        except Exception as e:
            logger.warning(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"빈 태그 추가 방지 테스트 실패: {str(e)}")
            raise

    @pytest.mark.data_required
    def test_tag_deletion(self, driver):
        """
        특정 태그 삭제 기능 테스트
        
        사전 조건: 사용자가 로그인 되어 있고, 게시글 작성 페이지에서 여러 개의 태그를 입력한 상태이다.
        재현 절차:
        1. 입력된 여러 태그 중 특정 태그 옆의 삭제 버튼(또는 아이콘)을 클릭한다.
        2. 남아있는 태그 목록을 확인한다.
        기대 결과: 클릭한 특정 태그만 삭제되고, 다른 태그들은 그대로 유지된다.
        """
        try:
            # 테스트 데이터 로드
            testData = loadTestData()["tag_deletion"]
            
            # 로그인 (사전 조건)
            loginPage = LoginPage(driver)
            loginPage.login(testData["email"], testData["password"])
            
            # 게시글 작성 페이지로 이동
            editorPage = EditorPage(driver)
            driver.get(testData["editor_url"])
            
            # 게시글 작성
            editorPage.enterTitle(testData["title"])
            editorPage.enterDescription(testData["description"])
            editorPage.enterBody(testData["body"])
            
            # 여러 태그 입력
            for tag in testData["tags"]:
                editorPage.enterTags(tag)
            
            # 입력된 태그 확인
            tag_pills = driver.find_elements(*EditorLoc.TAG_PILLS)
            initial_tag_count = len(tag_pills)
            assert initial_tag_count == len(testData["tags"]), f"입력한 태그 수({len(testData['tags'])})와 표시된 태그 수({initial_tag_count})가 일치하지 않습니다."
            
            # 특정 태그 삭제 (첫 번째 태그)
            delete_buttons = driver.find_elements(*EditorLoc.TAG_DELETE_BUTTONS)
            delete_buttons[0].click()
            
            # 태그 삭제 확인
            tag_pills_after_deletion = driver.find_elements(*EditorLoc.TAG_PILLS)
            assert len(tag_pills_after_deletion) == initial_tag_count - 1, "태그가 삭제되지 않았습니다."
            
            # 남은 태그들이 예상대로 유지되는지 확인
            remaining_tags = [pill.text.replace(' ×', '') for pill in tag_pills_after_deletion]
            expected_remaining_tags = testData["tags"][1:]  # 첫 번째 태그를 제외한 나머지
            assert set(remaining_tags) == set(expected_remaining_tags), f"삭제 후 남은 태그({remaining_tags})가 예상 태그({expected_remaining_tags})와 일치하지 않습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 태그 삭제 테스트 성공")
        except Exception as e:
            logger.warning(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"태그 삭제 테스트 실패: {str(e)}")
            raise


class TestArticleFeatures:
    
    @pytest.mark.data_required
    def test_duplicateTags_validation(self, driver):
        """
        테스트 시나리오: 동일한 태그 입력 시 중복 등록 방지 검증
        
        사전 조건:
        - 사용자가 로그인 되어 있고, 게시글 작성 페이지에 접근한다
        
        재현 절차:
        1. 여러 개의 동일한 태그를 입력한다.
        
        기대 결과:
        - 동일한 태그는 등록되지 않는다.
        - "이미 등록된 태그입니다." 에러문구 노출
        """
        try:
            # 테스트 데이터 로드
            testData = loadTestData()["article_creation"]
            
            # 로그인 진행
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 게시글 작성 페이지로 이동
            editorPage = EditorPage(driver)
            driver.get(testData["editor_url"])
            
            # 동일한 태그 여러 번 입력
            duplicateTag = testData["duplicateTag"]
            editorPage.enterTags(duplicateTag)
            editorPage.enterTags(duplicateTag)
            
            # 에러 메시지 확인
            errorMessage = driver.find_element(*EditorLoc.TAG_ERROR_MESSAGE).text
            assert "이미 등록된 태그입니다." in error_message, f"태그 중복 에러 메시지가 표시되지 않았습니다. 실제 메시지: {error_message}"
            
            # 태그 목록에서 중복 태그가 한 번만 표시되는지 확인
            tagElements = driver.find_elements(*EditorLoc.TAG_LIST)
            tagTexts = [tag.text for tag in tagElements]
            duplicateCount = tagTexts.count(duplicateTag)
            assert duplicateCount == 1, f"중복 태그가 여러 번 등록되었습니다. 중복 횟수: {duplicateCount}"
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 태그 중복 검증 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"태그 중복 검증 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_required
    def test_empty_fields_validation(self, driver):
        """
        테스트 시나리오: 공백만 입력한 게시글 등록 시도 시 검증
        
        사전 조건:
        - 사용자가 로그인 되어 있고, 게시글 작성 페이지에 접근한다
        
        재현 절차:
        1. 각 필드에 공백 문자만 입력한다.
        2. [Publish Article] 버튼을 클릭한다.
        
        기대 결과:
        - 공백만으로는 등록 불가하다는 오류 메시지가 표시된다.
        """
        try:
            # 테스트 데이터 로드
            testData = loadTestData()["article_creation"]
            
            # 로그인 진행
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 게시글 작성 페이지로 이동
            editorPage = EditorPage(driver)
            driver.get(testData["editor_url"])
            
            # 각 필드에 공백만 입력
            editorPage.enterTitle("   ")
            editorPage.enterDescription("   ")
            editorPage.enterBody("   ")
            
            # 게시글 등록 버튼 클릭
            editorPage.clickPublishButton()
            
            # 오류 메시지 확인
            errorElements = driver.find_elements(*EditorLoc.ERRORMESSAGES)
            errorTexts = [error.text for error in errorElements]
            
            # 최소 하나 이상의 오류 메시지가 표시되어야 함
            assert len(errorTexts) > 0, "공백 입력 시 오류 메시지가 표시되지 않았습니다."
            
            # 오류 메시지 내용 확인
            expectedErrorKeywords = ["empty", "blank", "required", "공백", "필수"]
            hasExpectedError = any(any(keyword in error.lower() for keyword in expectedErrorKeywords) for error in errorTexts)
            assert hasExpectedError, f"공백 관련 오류 메시지가 표시되지 않았습니다. 실제 메시지: {errorTexts}"
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 공백 입력 검증 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"공백 입력 검증 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_required
    def test_empty_global_feed(self, driver):
        """
        테스트 시나리오: 게시글이 없는 Global Feed 페이지 확인
        
        사전 조건:
        - 시스템에 등록된 게시글이 하나도 없다.
        
        재현 절차:
        1. Global Feed 페이지로 이동한다.
        
        기대 결과:
        - "No articles are here... yet." 문구가 노출된다.
        - 게시글 목록은 노출되지 않는다.
        """
        try:
            # 홈페이지로 이동
            homePage = HomePage(driver)
            driver.get(loadTestData()["urls"]["home_url"])
            
            # Global Feed 탭 클릭
            homePage.clickGlobalFeedTab()
            
            # "No articles" 메시지 확인
            noArticlesMessage = driver.find_element(*HomeLoc.NO_ARTICLES_MESSAGE).text
            assert "No articles are here... yet." in noArticlesMessage, f"게시글 없음 메시지가 표시되지 않았습니다. 실제 메시지: {noArticlesMessage}"
            
            # 게시글 목록이 표시되지 않는지 확인
            articleElements = driver.find_elements(*HomeLoc.ARTICLE_PREVIEW)
            assert len(articleElements) == 0, f"게시글이 없어야 하는데 {len(articleElements)}개의 게시글이 표시되었습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 빈 글로벌 피드 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"빈 글로벌 피드 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_required
    def test_global_feed_with_articles(self, driver):
        """
        테스트 시나리오: 게시글이 있는 Global Feed 페이지 확인
        
        사전 조건:
        - 시스템에 등록된 게시글이 존재한다.
        
        재현 절차:
        1. Global Feed 페이지로 이동한다.
        
        기대 결과:
        - 등록된 게시글 목록이 노출된다.
        - 프로필 이미지, 타이틀, 서브타이틀이 표시된다.
        """
        try:
            # 홈페이지로 이동
            homePage = HomePage(driver)
            driver.get(loadTestData()["urls"]["home_url"])
            
            # Global Feed 탭 클릭
            homePage.clickGlobalFeedTab()
            
            # 게시글 목록이 표시되는지 확인
            articleElements = driver.find_elements(*HomeLoc.ARTICLE_PREVIEW)
            assert len(articleElements) > 0, "게시글이 하나도 표시되지 않았습니다."
            
            # 첫 번째 게시글의 요소들 확인
            firstArticle = articleElements[0]
            
            # 프로필 이미지 확인
            profileImage = firstArticle.find_element(*HomeLoc.ARTICLE_AUTHOR_IMAGE)
            assert profileImage.is_displayed(), "프로필 이미지가 표시되지 않았습니다."
            
            # 타이틀 확인
            title = firstArticle.find_element(*HomeLoc.ARTICLE_TITLE)
            assert title.text.strip() != "", "게시글 타이틀이 비어있습니다."
            
            # 서브타이틀(설명) 확인
            description = firstArticle.find_element(*HomeLoc.ARTICLE_DESCRIPTION)
            assert description.is_displayed(), "게시글 설명이 표시되지 않았습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 게시글 목록 표시 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"게시글 목록 표시 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_required
    def test_user_article_in_global_feed(self, driver):
        """
        테스트 시나리오: 사용자 본인 게시글이 Global Feed에 표시되는지 확인
        
        사전 조건:
        - 사용자가 로그인 되어 있고, 해당 사용자가 작성한 게시글이 존재한다.
        
        재현 절차:
        1. Global Feed 페이지로 이동한다.
        2. 본인이 작성한 게시글이 목록에 노출되는지 확인한다.
        
        기대 결과:
        - 본인이 작성한 게시글이 Global Feed 목록에 정상적으로 노출된다.
        """
        try:
            # 테스트 데이터 로드
            testData = loadTestData()["user_article"]
            
            # 로그인 진행
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 홈페이지로 이동
            homePage = HomePage(driver)
            driver.get(testData["home_url"])
            
            # 사용자 이름 가져오기
            username = homePage.getNavigateUserName()
            
            # Global Feed 탭 클릭
            homePage.clickGlobalFeedTab()
            
            # 게시글 목록 가져오기
            articleTitles = homePage.getArticleTitles()
            assert len(articleTitles) > 0, "게시글이 하나도 표시되지 않았습니다."
            
            # 사용자 본인의 게시글 찾기
            articleElements = driver.find_elements(*HomeLoc.ARTICLE_PREVIEW)
            userArticleFound = False
            
            for article in articleElements:
                authorElement = article.find_element(*HomeLoc.ARTICLE_AUTHOR)
                authorName = authorElement.text
                
                if authorName == username:
                    userArticleFound = True
                    break
            
            assert userArticleFound, f"사용자({username})의 게시글이 Global Feed에 표시되지 않았습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 사용자 게시글 표시 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"사용자 게시글 표시 테스트 실패: {str(e)}")
            raise


class TestArticleFeatures:
    """게시글 관련 기능 테스트 클래스"""
    
    @pytest.mark.data_required
    def test_newline_in_subtitle_display(self, driver):
        """
        테스트 ID: unnamed
        시나리오: 서브타이틀(About)에 줄바꿈이 포함된 게시글이 피드에서 정상 노출되는지 확인
        
        사전 조건:
        게시글 작성 시 서브타이틀(About)에 줄바꿈을 포함하여 등록한 게시글이 존재한다.
        """
        try:
            # 테스트 데이터 로드
            testData = loadTestData().get("article_with_newline", {})
            
            # 홈페이지로 이동 및 Global Feed 클릭
            homePage = HomePage(driver)
            homePage.clickGlobalFeedTab()
            
            # 줄바꿈이 포함된 서브타이틀이 있는 게시글 확인
            articleTitles = homePage.getArticleTitles()
            
            # 해당 게시글이 존재하는지 확인
            assert homePage.isArticleVisible(test_data.get("title", "")), \
                f"줄바꿈이 포함된 서브타이틀이 있는 게시글 '{test_data.get('title', '')}' 이 피드에 노출되지 않습니다."
            
            # 서브타이틀에 줄바꿈이 정상적으로 적용되었는지 확인
            # 줄바꿈이 적용된 서브타이틀 요소 확인
            subtitleElement = driver.find_element(*HomeLoc.ARTICLE_DESCRIPTION)
            subtitleText = subtitleElement.text
            
            # 줄바꿈 문자가 포함되어 있는지 확인
            assert "\n" in subtitleText or "<br>" in subtitleElement.get_attribute("innerHTML"), \
                "서브타이틀에 줄바꿈이 정상적으로 적용되지 않았습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"서브타이틀 줄바꿈 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_required
    def test_like_button_toggle(self, driver):
        """
        테스트 ID: unnamed
        시나리오: 좋아요 버튼 클릭 시 상태 토글 및 좋아요 수 증감 확인
        
        사전 조건:
        Global Feed에 게시글이 노출되어 있다.
        """
        try:
            # 홈페이지로 이동 및 Global Feed 클릭
            homePage = HomePage(driver)
            homePage.clickGlobalFeedTab()
            
            # 첫 번째 게시글의 좋아요 버튼 및 초기 좋아요 수 확인
            likeButton = driver.find_element(*HomeLoc.FIRSTARTICLE_LIKE_BUTTON)
            initialLikeCount = int(likeButton.text.strip() or "0")
            initial_button_state = "active" in likeButton.get_attribute("class")
            
            # 1. 좋아요 버튼 클릭
            likeButton.click()
            driver.implicitly_wait(2)  # 상태 변경 대기
            
            # 2. 버튼 상태와 좋아요 수 확인
            likeButton = driver.find_element(*HomeLoc.FIRSTARTICLE_LIKE_BUTTON)  # 요소 다시 가져오기
            afterClickLikeCount = int(likeButton.text.strip() or "0")
            afterClickButtonState = "active" in likeButton.get_attribute("class")
            
            # 버튼 상태가 변경되었는지 확인
            assert initial_button_state != afterClickButtonState, \
                "좋아요 버튼 클릭 후 상태가 변경되지 않았습니다."
            
            # 좋아요 수가 적절히 변경되었는지 확인
            expectedCount = initialLikeCount + (1 if afterClickButtonState else -1)
            assert afterClickLikeCount == expectedCount, \
                f"좋아요 수가 예상대로 변경되지 않았습니다. 예상: {expectedCount}, 실제: {afterClickLikeCount}"
            
            # 3. 좋아요 버튼 다시 클릭
            likeButton.click()
            driver.implicitly_wait(2)  # 상태 변경 대기
            
            # 4. 버튼 상태와 좋아요 수 다시 확인
            likeButton = driver.find_element(*HomeLoc.FIRSTARTICLE_LIKE_BUTTON)  # 요소 다시 가져오기
            finalLikeCount = int(likeButton.text.strip() or "0")
            finalButtonState = "active" in likeButton.get_attribute("class")
            
            # 버튼 상태가 원래대로 돌아왔는지 확인
            assert afterClickButtonState != finalButtonState, \
                "좋아요 버튼 재클릭 후 상태가 변경되지 않았습니다."
            
            # 좋아요 수가 원래대로 돌아왔는지 확인
            assert finalLikeCount == initialLikeCount, \
                f"좋아요 수가 원래대로 돌아오지 않았습니다. 초기: {initialLikeCount}, 최종: {finalLikeCount}"
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"좋아요 버튼 토글 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_required
    def test_tag_display_in_article(self, driver):
        """
        테스트 ID: unnamed
        시나리오: 게시글에 등록된 태그 목록이 정상적으로 노출되는지 확인
        
        사전 조건:
        태그가 등록된 게시글이 Global Feed에 노출되어 있다.
        """
        try:
            # 테스트 데이터 로드
            testData = loadTestData().get("article_with_tags", {})
            
            # 홈페이지로 이동 및 Global Feed 클릭
            homePage = HomePage(driver)
            homePage.clickGlobalFeedTab()
            
            # 태그가 등록된 게시글이 존재하는지 확인
            articleTitles = homePage.getArticleTitles()
            assert len(articleTitles) > 0, "Global Feed에 게시글이 존재하지 않습니다."
            
            # 첫 번째 게시글의 태그 목록 확인
            tagElements = driver.find_elements(*HomeLoc.ARTICLE_TAGS)
            
            # 태그가 존재하는지 확인
            assert len(tagElements) > 0, "게시글에 태그가 존재하지 않습니다."
            
            # 태그 텍스트 추출
            tagTexts = [tag.text for tag in tagElements]
            
            # 태그가 정상적으로 노출되는지 확인
            for tag in tagTexts:
                assert tag.strip() != "", "빈 태그가 존재합니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공: 태그 목록 {tagTexts}")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"태그 노출 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_required
    def test_longTag_display(self, driver):
        """
        테스트 ID: unnamed
        시나리오: 20자 이상인 긴 태그가 레이아웃을 벗어나지 않고 정상 표시되는지 확인
        
        사전 조건:
        20자 이상인 태그가 등록된 게시글이 Global Feed에 노출되어 있다.
        - 일이삼사오육칠팔구십일이삼사오육칠팔구십
        """
        try:
            # 테스트 데이터 로드
            testData = loadTestData().get("article_with_longTag", {})
            longTag = "일이삼사오육칠팔구십일이삼사오육칠팔구십"
            
            # 홈페이지로 이동 및 Global Feed 클릭
            homePage = HomePage(driver)
            homePage.clickGlobalFeedTab()
            
            # 긴 태그가 등록된 게시글 확인
            articleFound = False
            
            # 모든 게시글의 태그를 확인
            articles = driver.find_elements(*HomeLoc.ARTICLE_PREVIEW)
            for article in articles:
                tagElements = article.find_elements(*HomeLoc.ARTICLE_TAG)
                for tag in tagElements:
                    if longTag in tag.text:
                        articleFound = True
                        
                        # 태그의 레이아웃 확인
                        # 1. 태그가 화면에 보이는지 확인
                        assert tag.is_displayed(), "긴 태그가 화면에 표시되지 않습니다."
                        
                        # 2. 태그의 위치와 크기 확인
                        tagRect = tag.rect
                        articleRect = article.rect
                        
                        # 태그가 게시글 영역 내에 있는지 확인
                        assert tagRect['x'] >= articleRect['x'], "태그가 게시글 왼쪽 경계를 벗어납니다."
                        assert tagRect['x'] + tagRect['width'] <= articleRect['x'] + articleRect['width'], \
                            "태그가 게시글 오른쪽 경계를 벗어납니다."
                        assert tagRect['y'] >= articleRect['y'], "태그가 게시글 상단 경계를 벗어납니다."
                        assert tagRect['y'] + tagRect['height'] <= articleRect['y'] + articleRect['height'], \
                            "태그가 게시글 하단 경계를 벗어납니다."
                        
                        break
                if articleFound:
                    break
            
            assert articleFound, f"긴 태그 '{longTag}'가 포함된 게시글을 찾을 수 없습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"긴 태그 표시 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_required
    def test_pagination_with_many_articles(self, driver):
        """
        테스트 ID: unnamed
        시나리오: 페이지네이션 기능 확인 및 1페이지당 게시글 수 확인
        
        사전 조건:
        시스템에 총 10개 초과의 게시글이 등록되어 있다.
        """
        try:
            # 홈페이지로 이동 및 Global Feed 클릭
            homePage = HomePage(driver)
            homePage.clickGlobalFeedTab()
            
            # 1. 1페이지에 노출되는 게시글의 개수 확인
            articles = driver.find_elements(*HomeLoc.ARTICLE_PREVIEW)
            articleCount = len(articles)
            
            # 1페이지에 최대 10개의 게시글이 노출되는지 확인
            assert articleCount <= 10, f"1페이지에 10개 초과의 게시글({articleCount}개)이 노출됩니다."
            
            # 2. 페이지네이션 컨트롤이 있는지 확인
            paginationControls = driver.find_elements(*HomeLoc.PAGINATION)
            
            # 페이지네이션 컨트롤이 존재하는지 확인
            assert len(paginationControls) > 0, "페이지네이션 컨트롤이 존재하지 않습니다."
            
            # 페이지 번호 또는 다음/이전 버튼이 존재하는지 확인
            paginationItems = driver.find_elements(*HomeLoc.PAGINATIONITEMS)
            assert len(paginationItems) > 0, "페이지 번호 또는 다음/이전 버튼이 존재하지 않습니다."
            
            # 다음 페이지로 이동 가능한지 확인
            nextPageLink = None
            for item in paginationItems:
                if item.text.strip() == "2" or "next" in item.get_attribute("class").lower():
                    nextPageLink = item
                    break
            
            assert nextPageLink is not None, "다음 페이지로 이동할 수 있는 컨트롤이 존재하지 않습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"페이지네이션 테스트 실패: {str(e)}")
            raise


class TestYourFeed:
    """Your Feed 페이지 관련 테스트 클래스"""
    
    @pytest.mark.data_required
    def test_empty_your_feed_no_following(self, driver):
        """
        테스트 시나리오: 사용자가 로그인 되어 있으며, 팔로우하는 사용자가 한 명도 없을 때
        Your Feed 페이지에 "No articles are here... yet." 문구가 노출되는지 확인
        """
        try:
            # 테스트 데이터 로드
            testData = loadTestData()["emptyYourFeedNoFollowing"]
            
            # 로그인
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # Your Feed 페이지로 이동
            homePage = HomePage(driver)
            homePage.clickYourFeedTab()
            
            # "No articles are here... yet." 문구 확인
            assert homePage.is_element_visible(Loc.NO_ARTICLES_MESSAGE), "No articles 메시지가 표시되지 않았습니다."
            
            # 게시글 목록이 노출되지 않는지 확인
            assert not homePage.isArticleVisible(), "게시글이 표시되었습니다. 게시글이 없어야 합니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.warning(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"빈 Your Feed 테스트 실패 (팔로우 없음): {str(e)}")
            raise
    
    @pytest.mark.data_required
    def test_empty_your_feed_with_following_no_articles(self, driver):
        """
        테스트 시나리오: 사용자가 로그인 되어 있으며, 팔로우하는 사용자는 있으나 
        팔로우하는 사용자들이 게시글을 하나도 작성하지 않았을 때
        Your Feed 페이지에 "No articles are here... yet." 문구가 노출되는지 확인
        """
        try:
            # 테스트 데이터 로드
            testData = loadTestData()["emptyYourFeedWithFollowing"]
            
            # 로그인
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # Your Feed 페이지로 이동
            homePage = HomePage(driver)
            homePage.clickYourFeedTab()
            
            # "No articles are here... yet." 문구 확인
            assert homePage.is_element_visible(Loc.NO_ARTICLES_MESSAGE), "No articles 메시지가 표시되지 않았습니다."
            
            # 게시글 목록이 노출되지 않는지 확인
            assert not homePage.isArticleVisible(), "게시글이 표시되었습니다. 게시글이 없어야 합니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.warning(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"빈 Your Feed 테스트 실패 (팔로우 있으나 게시글 없음): {str(e)}")
            raise
    
    @pytest.mark.data_required
    def test_your_feed_with_articles(self, driver):
        """
        테스트 시나리오: 사용자가 로그인 되어 있으며, 게시글을 작성한 사용자를 팔로우하고 있을 때
        Your Feed 페이지에 팔로우하는 사용자들이 작성한 게시글 목록이 노출되는지 확인
        """
        try:
            # 테스트 데이터 로드
            testData = loadTestData()["yourFeedWithArticles"]
            
            # 로그인
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # Your Feed 페이지로 이동
            homePage = HomePage(driver)
            homePage.clickYourFeedTab()
            
            # 게시글 목록이 노출되는지 확인
            assert homePage.isArticleVisible(), "게시글이 표시되지 않았습니다."
            
            # 게시글 요소들 확인
            assert homePage.is_element_visible(Loc.ARTICLE_TITLE), "게시글 타이틀이 표시되지 않았습니다."
            assert homePage.is_element_visible(Loc.ARTICLE_SUBTITLE), "게시글 서브타이틀이 표시되지 않았습니다."
            assert homePage.is_element_visible(Loc.FAVORITEBUTTON), "좋아요 버튼이 표시되지 않았습니다."
            assert homePage.is_element_visible(Loc.ARTICLE_TAGS), "태그가 표시되지 않았습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.warning(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"Your Feed 게시글 표시 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_required
    def test_favoriteButton_toggle(self, driver):
        """
        테스트 시나리오: Your Feed에 게시글이 노출되어 있을 때
        좋아요(하트) 버튼을 클릭하여 상태와 좋아요 수가 정상적으로 변경되는지 확인
        """
        try:
            # 테스트 데이터 로드
            testData = loadTestData()["favoriteButtonToggle"]
            
            # 로그인
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # Your Feed 페이지로 이동
            homePage = HomePage(driver)
            homePage.clickYourFeedTab()
            
            # 게시글이 표시되는지 확인
            assert homePage.isArticleVisible(), "게시글이 표시되지 않았습니다."
            
            # 좋아요 버튼 초기 상태 확인
            favoriteButton = driver.find_element(*Loc.FAVORITEBUTTON)
            initialCount = int(favoriteButton.text.strip())
            initialState = "active" in favoriteButton.get_attribute("class")
            
            # 좋아요 버튼 클릭
            favoriteButton.click()
            driver.implicitly_wait(2)  # 상태 변경 대기
            
            # 좋아요 버튼 상태 변경 확인
            favoriteButton = driver.find_element(*Loc.FAVORITEBUTTON)  # 요소 다시 가져오기
            afterClickCount = int(favoriteButton.text.strip())
            afterClickState = "active" in favoriteButton.get_attribute("class")
            
            # 상태가 토글되었는지 확인
            assert initialState != afterClickState, "좋아요 버튼 상태가 변경되지 않았습니다."
            
            # 좋아요 수가 적절히 변경되었는지 확인
            expectedCount = initialCount + (1 if afterClickState else -1)
            assert afterClickCount == expectedCount, f"좋아요 수가 예상대로 변경되지 않았습니다. 예상: {expectedCount}, 실제: {afterClickCount}"
            
            # 다시 클릭하여 원래 상태로 돌아가는지 확인
            favoriteButton.click()
            driver.implicitly_wait(2)  # 상태 변경 대기
            
            # 좋아요 버튼 상태 재확인
            favoriteButton = driver.find_element(*Loc.FAVORITEBUTTON)  # 요소 다시 가져오기
            finalCount = int(favoriteButton.text.strip())
            finalState = "active" in favoriteButton.get_attribute("class")
            
            # 원래 상태로 돌아갔는지 확인
            assert finalState == initialState, "좋아요 버튼이 원래 상태로 돌아가지 않았습니다."
            assert finalCount == initialCount, f"좋아요 수가 원래대로 돌아가지 않았습니다. 예상: {initialCount}, 실제: {finalCount}"
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.warning(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"좋아요 버튼 토글 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_required
    def test_article_tags_display(self, driver):
        """
        테스트 시나리오: 태그가 등록된 게시글이 Your Feed에 노출되어 있을 때
        해당 게시글에 등록된 태그 목록이 정상적으로 노출되는지 확인
        """
        try:
            # 테스트 데이터 로드
            testData = loadTestData()["articleTagsDisplay"]
            
            # 로그인
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # Your Feed 페이지로 이동
            homePage = HomePage(driver)
            homePage.clickYourFeedTab()
            
            # 게시글이 표시되는지 확인
            assert homePage.isArticleVisible(), "게시글이 표시되지 않았습니다."
            
            # 태그가 표시되는지 확인
            assert homePage.is_element_visible(Loc.ARTICLE_TAGS), "태그가 표시되지 않았습니다."
            
            # 태그 목록 가져오기
            tag_list = homePage.getTagList()
            
            # 태그가 하나 이상 존재하는지 확인
            assert len(tag_list) > 0, "태그가 하나도 없습니다."
            
            # 테스트 데이터에 있는 태그가 실제로 표시되는지 확인 (선택적)
            if "expected_tags" in test_data:
                for expected_tag in testData["expected_tags"]:
                    assert expected_tag in tag_list, f"예상 태그 '{expected_tag}'가 표시되지 않았습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.warning(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"게시글 태그 표시 테스트 실패: {str(e)}")
            raise

class TestFeedAndArticles:
    """피드 및 게시글 관련 테스트 클래스"""
    
    @pytest.mark.data_required
    def test_longTag_display(self, driver):
        """
        테스트 ID: unnamed
        시나리오: 긴 태그(20자 이상)가 있는 게시글이 Your Feed에서 정상적으로 표시되는지 확인
        
        사전 조건:
        20자 이상인 태그가 등록된 게시글이 Your Feed에 노출되어 있다.
        - 일이삼사오육칠팔구십일이삼사오육칠팔구십
        """
        try:
            # 테스트 데이터 로드
            testData = loadTestData().get("longTag_test", {})
            
            # 로그인 진행
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(test_data.get("email"), test_data.get("password"))
            
            # Your Feed 탭으로 이동
            homePage = HomePage(driver)
            homePage.clickYourFeedTab()
            
            # 긴 태그가 있는 게시글 확인
            assert homePage.isArticleVisible(test_data.get("article_title")), "긴 태그가 있는 게시글이 Your Feed에 표시되지 않습니다."
            
            # 태그 요소가 정상적으로 표시되는지 확인
            longTag_element = driver.find_element(*HomeLoc.ARTICLE_TAG)
            
            # 태그 요소의 위치와 크기 확인
            tag_location = longTag_element.location
            tag_size = longTag_element.size
            
            # 화면 레이아웃을 벗어나지 않는지 확인
            viewport_width = driver.execute_script("return window.innerWidth")
            assert tag_location['x'] + tag_size['width'] <= viewport_width, "태그가 화면 레이아웃을 벗어납니다."
            
            # 다음 게시글 요소를 찾아 태그가 침범하지 않는지 확인
            next_article = driver.find_elements(*HomeLoc.ARTICLE_PREVIEW)[1] if len(driver.find_elements(*HomeLoc.ARTICLE_PREVIEW)) > 1 else None
            
            if next_article:
                next_article_top = next_article.location['y']
                tag_bottom = tag_location['y'] + tag_size['height']
                assert tag_bottom < next_article_top, "태그가 다음 게시글 영역을 침범합니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 긴 태그 표시 테스트 성공")
        except Exception as e:
            logger.warning(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"긴 태그 표시 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_required
    def test_pagination_control(self, driver):
        """
        테스트 ID: unnamed
        시나리오: 페이지네이션 컨트롤 확인
        
        사전 조건:
        팔로우하는 사용자들이 작성한 총 게시글 수가 10개를 초과한다.
        """
        try:
            # 테스트 데이터 로드
            testData = loadTestData().get("pagination_test", {})
            
            # 로그인 진행
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(test_data.get("email"), test_data.get("password"))
            
            # Global Feed 탭으로 이동
            homePage = HomePage(driver)
            homePage.clickGlobalFeedTab()
            
            # 1페이지에 노출되는 게시글 개수 확인
            articleTitles = homePage.getArticleTitles()
            assert len(articleTitles) <= 10, f"1페이지에 10개 이상의 게시글이 노출됩니다. 현재 개수: {len(articleTitles)}"
            
            # 페이지네이션 컨트롤 존재 확인
            pagination_exists = homePage.is_element_present(HomeLoc.PAGINATION)
            assert pagination_exists, "페이지네이션 컨트롤이 존재하지 않습니다."
            
            # 다음 페이지 버튼 확인
            next_page_button_exists = homePage.is_element_present(HomeLoc.NEXT_PAGE_BUTTON)
            assert next_page_button_exists, "다음 페이지 버튼이 존재하지 않습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 페이지네이션 컨트롤 테스트 성공")
        except Exception as e:
            logger.warning(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"페이지네이션 컨트롤 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_required
    def test_article_navigation(self, driver):
        """
        테스트 ID: unnamed
        시나리오: 게시글 클릭 시 상세 페이지로 이동
        
        사전 조건:
        Global Feed 또는 Your Feed에 게시글이 노출되어 있다.
        """
        try:
            # 테스트 데이터 로드
            testData = loadTestData().get("article_navigation_test", {})
            
            # 로그인 진행
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(test_data.get("email"), test_data.get("password"))
            
            # Global Feed 탭으로 이동
            homePage = HomePage(driver)
            homePage.clickGlobalFeedTab()
            
            # 게시글 목록 확인
            articleTitles = homePage.getArticleTitles()
            assert len(articleTitles) > 0, "피드에 게시글이 존재하지 않습니다."
            
            # 첫 번째 게시글의 제목 저장
            firstArticle_title = articleTitles[0]
            
            # Read more 버튼 클릭
            driver.find_element(*HomeLoc.READ_MORE_BUTTON).click()
            
            # 게시글 상세 페이지로 이동했는지 확인
            article_page = ArticlePage(driver)
            article_title = article_page.getTitle()
            
            # 제목 비교
            assert article_title == firstArticle_title, f"게시글 상세 페이지의 제목이 일치하지 않습니다. 예상: {firstArticle_title}, 실제: {article_title}"
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 게시글 이동 테스트 성공")
        except Exception as e:
            logger.warning(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"게시글 이동 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_required
    def test_own_article_edit_delete_buttons(self, driver):
        """
        테스트 ID: unnamed
        시나리오: 본인 게시글에 Edit/Delete 버튼 노출 확인
        
        사전 조건:
        사용자가 로그인 되어 있으며, 본인이 작성한 게시글의 상세 페이지로 이동한다.
        """
        try:
            # 테스트 데이터 로드
            testData = loadTestData().get("own_article_test", {})
            
            # 로그인 진행
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(test_data.get("email"), test_data.get("password"))
            
            # 본인 게시글 URL로 직접 이동
            driver.get(test_data.get("own_article_url"))
            
            # 게시글 상세 페이지 확인
            article_page = ArticlePage(driver)
            
            # Edit Article 버튼 확인
            edit_button_exists = article_page.is_element_visible(ArticleLoc.EDIT_ARTICLE_BUTTON)
            assert edit_button_exists, "Edit Article 버튼이 노출되지 않습니다."
            
            # Delete Article 버튼 확인
            delete_button_exists = article_page.is_element_visible(ArticleLoc.DELETE_ARTICLE_BUTTON)
            assert delete_button_exists, "Delete Article 버튼이 노출되지 않습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 본인 게시글 버튼 테스트 성공")
        except Exception as e:
            logger.warning(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"본인 게시글 버튼 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_required
    def test_other_article_no_edit_delete_buttons(self, driver):
        # ARTI-AUTO-036: 타인 게시글에 Edit/Delete 버튼 미노출 확인

        try:
            # 테스트 데이터 로드
            testData = loadTestData().get("other_article_test", {})
            
            # 로그인 진행
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData.get("email"), testData.get("password"))
            
            # 타인 게시글 URL로 직접 이동
            driver.get(testData.get("other_article_url"))
            
            # 게시글 상세 페이지 확인
            article_page = ArticlePage(driver)
            
            # Edit Article 버튼 확인 (없어야 함)
            edit_button_exists = article_page.is_element_present(ArticleLoc.EDIT_ARTICLE_BUTTON)
            assert not edit_button_exists, "타인 게시글에 Edit Article 버튼이 노출됩니다."
            
            # Delete Article 버튼 확인 (없어야 함)
            delete_button_exists = article_page.is_element_present(ArticleLoc.DELETE_ARTICLE_BUTTON)
            assert not delete_button_exists, "타인 게시글에 Delete Article 버튼이 노출됩니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 타인 게시글 버튼 테스트 성공")
        except Exception as e:
            logger.warning(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"타인 게시글 버튼 테스트 실패: {str(e)}")
            raise
        
class TestArticleManagement:
    """게시글 관리 관련 테스트 클래스"""

    @pytest.mark.data_required
    def test_edit_article_button_click(self, driver):
        # ARTI-AUTO-037: 게시글 수정 페이지 이동 및 기존 내용 확인

        try:
            # 테스트 데이터 로드
            testData = loadTestData()["article_edit"]
            
            # 로그인 및 게시글 상세 페이지로 이동 (사전 조건)
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 게시글 상세 페이지 접근 (사전 조건)
            article_page = ArticlePage(driver)
            driver.get(testData["article_url"])
            
            # 게시글 원본 내용 저장
            original_title = article_page.getTitle()
            original_body = article_page.getBody()
            
            # 1. [Edit Article] 버튼 클릭
            driver.find_element(*ArticleLoc.EDIT_ARTICLE_BUTTON).click()
            
            # 에디터 페이지로 이동 확인
            editorPage = EditorPage(driver)
            assert editor_page.wait_for_url_contains("/editor/"), "에디터 페이지로 이동하지 않았습니다."
            
            # 기존 게시글 내용이 입력 필드에 채워져 있는지 확인
            title_field = driver.find_element(*EditorLoc.TITLE_FIELD)
            body_field = driver.find_element(*EditorLoc.BODY_FIELD)
            
            assert title_field.get_attribute("value") == original_title, "제목이 에디터에 올바르게 로드되지 않았습니다."
            assert original_body in body_field.text, "본문이 에디터에 올바르게 로드되지 않았습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"게시글 수정 페이지 이동 테스트 실패: {str(e)}")
            raise


    @pytest.mark.data_required
    def test_edit_article_content(self, driver):
        # ARTI-AUTO-038: 게시글 내용 수정 및 반영 확인

        try:
            # 테스트 데이터 로드
            testData = loadTestData()["TwoArticlesUser"]
            
            # 로그인 및 게시글 수정 페이지로 이동 (사전 조건)
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 게시글 수정 페이지 접근 (사전 조건)
            driver.get(testData["edit_url"])
            
            # 에디터 페이지 객체 생성
            editorPage = EditorPage(driver)
            timestamp = time_utils.get_current_timestamp()
            
            # 1. 게시글 내용 수정
            updated_title = f"Updated Title {timestamp}"
            updated_body = f"Updated Body Content {timestamp}"
            
            editorPage.enterTitle(updated_title)
            editorPage.enterBody(updated_body)
            
            # 2. [Publish Article] 버튼 클릭
            editorPage.clickPublishButton()
            
            # 3. 수정된 게시글 상세 페이지로 이동 확인
            article_page = ArticlePage(driver)
            assert article_page.wait_for_url_contains("/article/"), "게시글 상세 페이지로 이동하지 않았습니다."
            
            # 게시글 내용이 성공적으로 수정되었는지 확인
            displayed_title = article_page.getTitle()
            displayed_body = article_page.getBody()
            
            assert displayed_title == updated_title, f"제목이 올바르게 수정되지 않았습니다. 예상: {updated_title}, 실제: {displayed_title}"
            assert updated_body in displayed_body, f"본문이 올바르게 수정되지 않았습니다. 본문에 '{updated_body}' 가 포함되어야 합니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"게시글 내용 수정 테스트 실패: {str(e)}")
            raise


    @pytest.mark.data_required
    def test_edit_article_empty_content(self, driver):
        # ARTI-AUTO-039: 게시글 내용 전체 삭제 후 발행 시도
        
        try:
            # 테스트 데이터 로드
            testData = loadTestData()["TwoArticlesUser"]
            
            # 로그인 및 게시글 수정 페이지로 이동 (사전 조건)
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 게시글 수정 페이지 접근 (사전 조건)
            driver.get(testData["edit_url"])
            
            # 에디터 페이지 객체 생성
            editorPage = EditorPage(driver)
            
            # 1. 기존 게시글 내용 전부 삭제
            editorPage.enterTitle("")  # 제목 삭제
            editorPage.enterDescription("")  # 설명 삭제
            editorPage.enterBody("")  # 본문 삭제
            
            # 2. [Publish Article] 버튼 클릭
            editorPage.clickPublishButton()
            
            # 3. 오류 메시지 확인
            errorElements = driver.find_elements(EditorLoc.ERRORMESSAGES)
            assert len(errorElements) > 0, (
                                            "오류 메시지가 표시되지 않았습니다."
                                            "→ 빈 제목/본문/설명에 대한 유효성 검증이 누락된 것으로 보입니다.")
            
            # 에디터 페이지에 머물러 있는지 확인 (상세 페이지로 이동하지 않음)
            currentUrl = driver.current_url
            assert "/editor/" in currentUrl, "오류가 발생했음에도 에디터 페이지를 벗어났습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"게시글 내용 전체 삭제 테스트 실패: {str(e)}")
            raise

    @pytest.mark.data_required
    def test_delete_article(self, driver):
        # ARTI-AUTO-040: 게시글 삭제

        try:
            # 테스트 데이터 로드
            testData = loadTestData()["TwoArticlesUser"]
            
            # 로그인 및 게시글 상세 페이지로 이동 (사전 조건)
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 게시글 상세 페이지 접근 (사전 조건)
            article_page = ArticlePage(driver)
            driver.get(testData["article_url"])
            
            # 삭제 전 게시글 제목 저장
            article_title = article_page.getTitle()
            
            # 1. [Delete Article] 버튼 클릭
            driver.find_element(*ArticleLoc.ARTICLE_DELETE_BUTTON).click()
            
            # 홈페이지로 리디렉션 확인
            homePage = HomePage(driver)
            assert homePage.wait_for_url_contains("/"), "홈페이지로 리디렉션되지 않았습니다."
            assert homePage.isPageLoaded(), "홈페이지가 제대로 로드되지 않았습니다."
            
            # 삭제된 게시글이 더 이상 노출되지 않는지 확인
            homePage.clickGlobalFeedTab()  # 글로벌 피드 탭 클릭
            
            # 게시글 목록 가져오기
            article_titles = homePage.getArticleTitles()
            
            # 삭제한 게시글이 목록에 없는지 확인
            assert article_title not in article_titles, f"삭제된 게시글 '{article_title}'이 여전히 목록에 표시됩니다."
            
            # 삭제된 게시글 URL로 직접 접근 시도
            driver.get(testData["article_url"])
            
            # 404 페이지 또는 다른 페이지로 리디렉션 확인
            currentUrl = driver.current_url
            assert testData["article_url"] not in currentUrl or "404" in driver.page_source, "삭제된 게시글에 여전히 접근 가능합니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"게시글 삭제 테스트 실패: {str(e)}")
            raise
