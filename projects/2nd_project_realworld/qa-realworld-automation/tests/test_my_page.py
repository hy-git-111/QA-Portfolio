import os
import json
import pytest
import inspect
import time
from selenium.webdriver.common.by import By

# 페이지 객체 임포트
from pages.settings_page import SettingsPage
from pages.article_page import ArticlePage
from pages.profile_page import ProfilePage
from pages.login_page import LoginPage
from pages.home_page import HomePage

# 로케이터 임포트
from locators.profile_locators import ProfilePageLocators as ProfileLoc
from locators.home_locators import HomePageLocators as HomeLoc

# 유틸리티 임포트
from utils.logger import setup_logger
from config import config

def loadTestData(key):
    # 테스트 데이터 로드 함수
    dataFilePath = os.path.join(config.TEST_DATA_DIR, "test_data.json")
    with open(dataFilePath, encoding="utf-8") as f:
        data = json.load(f)

        # data는 리스트이고, 각 요소는 딕셔너리임 → 반복하며 key를 가진 딕셔너리를 찾는다
        for item in data:
            if key in item:
                return item[key]

        raise KeyError(f"'{key}' not found in test_data.json")

    raise KeyError(f"'{key}' not found in test_data.json")

logger = setup_logger(__name__)

class TestMyPage:
    # 마이페이지 시나리오 테스트 클래스

    @pytest.mark.data_not_required
    def testNavigateToProfilePage(self, driver):
        # MYP-AUTO-001: 테스트 ID: unnamed
        try:
            # 테스트 데이터 로드
            testData = loadTestData("fullDataUser")
            
            # 로그인 진행
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 홈페이지 로드
            homePage = HomePage(driver)

            # 네비게이션바에서 사용자 이름 확인 및 클릭
            username = homePage.getNavigateUserName()

            # 프로필 이미지/이름 클릭 (네비게이션바에서)
            driver.find_element(*HomeLoc.NAV_USER_LINK).click()
            
            # 프로필 페이지 URL 확인
            profilePage = ProfilePage(driver)
            expectedUrlPart = f"/@{testData['username']}"
            assert profilePage.wait_for_url_contains(expectedUrlPart), f"프로필 페이지 URL에 {expectedUrlPart}가 포함되어 있지 않습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 프로필 페이지 접근 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} : {e}")
            raise

    @pytest.mark.data_not_required
    def testProfileUiElements(self, driver):
        # MYP-AUTO-002: 프로필 페이지 UI 요소 확인 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("fullDataUser")
            
            # 로그인 및 프로필 페이지 접근
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 프로필 이미지/이름 클릭 (네비게이션바에서)
            driver.find_element(*HomeLoc.NAV_USER_PIC).click()

            # 프로필 페이지 객체 생성
            profilePage = ProfilePage(driver)
            
            # UI 요소 확인
            # 1. 프로필 이미지 확인
            assert profilePage.is_element_visible(ProfileLoc.PROFILE_USER_IMG), "프로필 이미지가 표시되지 않습니다."
            
            # 2. 사용자 이름 확인
            username = profilePage.getUsername()
            assert username == testData["username"], f"프로필 페이지의 사용자 이름이 일치하지 않습니다. 예상: {testData['username']}, 실제: {username}"
            
            # 3. 상태 소개(bio) 확인
            bio = profilePage.getUserBio()
            assert bio is not None, "상태 소개(bio)가 표시되지 않습니다."
            
            # 4. 'Edit Profile Settings' 버튼 확인
            assert profilePage.is_element_visible(ProfileLoc.PROFILE_EDIT_SETTINGS_BTN), "'Edit Profile Settings' 버튼이 표시되지 않습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 프로필 페이지 UI 요소 확인 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} : {e}")
            raise

    @pytest.mark.data_not_required
    def testNavigateToSettingsPage(self, driver):
        # MYP-AUTO-003: 프로필 페이지에서 설정 페이지 접근 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("fullDataUser")
            
            # 로그인 및 프로필 페이지 접근
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 네비게이션바에서 사용자 이름 클릭하여 프로필 페이지로 이동
            driver.find_element(*HomeLoc.NAV_USER_LINK).click()
            
            # 프로필 페이지 객체 생성
            profilePage = ProfilePage(driver)
            
            # 'Edit Profile Settings' 버튼 클릭
            driver.find_element(*ProfileLoc.PROFILE_EDIT_SETTINGS_BTN).click()
            
            # 설정 페이지 객체 생성
            settingsPage = SettingsPage(driver)
            
            # 설정 페이지 URL 및 로드 확인
            assert settingsPage.wait_for_url_contains("/settings"), "설정 페이지 URL이 올바르지 않습니다."
            assert settingsPage.isSettingsPageLoaded(), "설정 페이지가 제대로 로드되지 않았습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 설정 페이지 접근 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} : {e}")
            raise

    @pytest.mark.data_not_required
    def testMyArticlesTabDefaultSelected(self, driver):
        # MYP-AUTO-004: 프로필 페이지 'My Articles' 탭 기본 선택 확인 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("fullDataUser")
            
            # 로그인 및 프로필 페이지 접근
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 네비게이션바에서 사용자 이름 클릭하여 프로필 페이지로 이동
            driver.find_element(*HomeLoc.NAV_USER_LINK).click()
            
            # 프로필 페이지 객체 생성
            profilePage = ProfilePage(driver)
            
            # 'My Articles' 탭 활성화 확인
            my_articles_tab = driver.find_element(*ProfileLoc.PROFILE_MY_ARTICLES_ACTIVE_TAB)
            favorited_articles_tab = driver.find_element(*ProfileLoc.PROFILE_FAVORITED_ARTICLES_TAB)
            
            # 'My Articles' 탭이 활성화되어 있는지 확인 (active 클래스 포함)
            assert "active" in my_articles_tab.get_attribute("class"), "'My Articles' 탭이 기본적으로 활성화되어 있지 않습니다."
            
            # 'Favorited Articles' 탭이 비활성화되어 있는지 확인 (active 클래스 미포함)
            assert "active" not in favorited_articles_tab.get_attribute("class"), "'Favorited Articles' 탭이 비활성화되어 있지 않습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 'My Articles' 탭 기본 선택 확인 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} : {e}")
            raise

    @pytest.mark.data_not_required
    def testSwitchToFavoritedArticlesTab(self, driver):
        # MYP-AUTO-005: 프로필 페이지 'Favorited Articles' 탭 전환 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("fullDataUser")
            
            # 로그인 및 프로필 페이지 접근
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 네비게이션바에서 사용자 이름 클릭하여 프로필 페이지로 이동
            driver.find_element(*HomeLoc.NAV_USER_LINK).click()
            
            # 프로필 페이지 객체 생성
            profilePage = ProfilePage(driver)
            
            # 'My Articles' 탭이 기본 선택되어 있는지 확인
            my_articles_tab = driver.find_element(*ProfileLoc.PROFILE_MY_ARTICLES_TAB)
            assert "active" in my_articles_tab.get_attribute("class"), "'My Articles' 탭이 기본적으로 활성화되어 있지 않습니다."
            
            # 'Favorited Articles' 탭 클릭
            favorited_articles_tab = driver.find_element(*ProfileLoc.PROFILE_FAVORITED_ARTICLES_TAB)
            favorited_articles_tab.click()
            
            # 'Favorited Articles' 탭이 활성화되어 있는지 확인
            assert "active" in favorited_articles_tab.get_attribute("class"), "'Favorited Articles' 탭이 클릭 후 활성화되지 않았습니다."
            
            # 'My Articles' 탭이 비활성화되어 있는지 확인
            assert "active" not in my_articles_tab.get_attribute("class"), "'My Articles' 탭이 비활성화되지 않았습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 'Favorited Articles' 탭 전환 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} : {e}")
            raise

    @pytest.mark.data_not_required
    def testEmptyMyArticlesTab(self, driver):
        # MYP-AUTO-006: 사용자가 작성한 게시글이 없을 때 'My Articles' 탭 확인
        try:
            # 테스트 데이터 로드
            testData = loadTestData("fullDataUser")
            
            # 로그인 진행
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 프로필 페이지로 이동
            profilePage = ProfilePage(driver)
            driver.get(f"{driver.current_url}/@{testData['username']}")
            
            # 1. 'My Articles' 탭이 기본 선택되어 있는지 확인
            assert profilePage.is_element_visible(ProfileLoc.PROFILE_MY_ARTICLES_ACTIVE_TAB), "'My Articles' 탭이 기본으로 선택되어 있지 않습니다."
            
            # 2. 게시글 목록 영역 확인
            no_articles_text = profilePage.getArticlePreviewText(ProfileLoc.PROFILE_ARTICLE_PREVIEW)
            assert no_articles_text == "No articles are here... yet.", f"예상 메시지와 다릅니다. 실제: {no_articles_text}"
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"테스트 실패: {str(e)}")
    
    @pytest.mark.data_not_required
    def testEmptyFavoritedArticlesTab(self, driver):
        # MYP-AUTO-007: 사용자가 좋아요를 누른 게시글이 없을 때 'Favorited Articles' 탭 확인
        try:
            # 테스트 데이터 로드
            testData = loadTestData("fullDataUser")
            
            # 로그인 진행
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 프로필 페이지로 이동
            profilePage = ProfilePage(driver)
            driver.get(f"{driver.current_url}/@{testData['username']}")
            
            # 1. 'Favorited Articles' 탭 클릭
            profilePage.clickFavoritedArticleTab()
            
            # 2. 게시글 목록 영역 확인
            no_articles_text = profilePage.getArticlePreviewText(ProfileLoc.PROFILE_ARTICLE_PREVIEW)
            assert no_articles_text == "No articles are here... yet.", f"예상 메시지와 다릅니다. 실제: {no_articles_text}"
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"테스트 실패: {str(e)}")
    
    @pytest.mark.data_required
    def testMyArticlesUiElements(self, driver):
        # MYP-AUTO-008: 사용자가 작성한 게시글의 UI 요소 확인
        try:
            # 테스트 데이터 로드
            testData = loadTestData("profile_with_articles")
            
            # 로그인 진행
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 프로필 페이지로 이동
            profilePage = ProfilePage(driver)
            driver.get(f"{driver.current_url}/@{testData['username']}")
            
            # 1. 'My Articles' 탭이 기본 선택되어 있는지 확인
            assert profilePage.is_element_visible(ProfileLoc.PROFILE_MY_ARTICLES_ACTIVE_TAB), "'My Articles' 탭이 기본으로 선택되어 있지 않습니다."
            
            # 2. 첫 번째 게시글의 UI 요소 확인
            # 프로필 이미지 확인
            assert profilePage.is_element_visible(ProfileLoc.PROFILE_ARTICLE_META), "프로필 이미지가 표시되지 않습니다."
            
            # 게시글 업로드 날짜 확인
            assert profilePage.is_element_visible(ProfileLoc.PROFILE_ARTICLE_DATE), "게시글 업로드 날짜가 표시되지 않습니다."
            
            # 게시글 타이틀 확인
            assert profilePage.is_element_visible(ProfileLoc.PROFILE_ARTICLE_TITLE), "게시글 타이틀이 표시되지 않습니다."
            
            # 서브타이틀 확인
            assert profilePage.is_element_visible(ProfileLoc.PROFILE_ARTICLE_DESCRIPTION), "서브타이틀이 표시되지 않습니다."
            
            # 좋아요 버튼 확인
            assert profilePage.is_element_visible(ProfileLoc.PROFILE_READ_MORE_LINK), "좋아요 버튼이 표시되지 않습니다."
            
            # 태그 확인
            assert profilePage.is_element_visible(ProfileLoc.PROFILE_TAG_LIST), "태그가 표시되지 않습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"테스트 실패: {str(e)}")
    
    @pytest.mark.data_required
    def testFavoritedArticlesUiElements(self, driver):
        # MYP-AUTO-009: 사용자가 좋아요를 누른 게시글의 UI 요소 확인
        try:
            # 테스트 데이터 로드
            testData = loadTestData("fullDataUser")
            
            # 로그인 진행
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 프로필 페이지로 이동
            profilePage = ProfilePage(driver)
            driver.get(f"{driver.current_url}/@{testData['username']}")
            
            # 1. 'Favorited Articles' 탭 클릭
            profilePage.clickFavoritedArticleButton()
            
            # 2. 첫 번째 게시글의 UI 요소 확인
            # 프로필 이미지 확인
            assert profilePage.is_element_visible(ProfileLoc.PROFILE_ARTICLE_META), "프로필 이미지가 표시되지 않습니다."
            
            # 게시글 업로드 날짜 확인
            assert profilePage.is_element_visible(ProfileLoc.PROFILE_ARTICLE_DATE), "게시글 업로드 날짜가 표시되지 않습니다."
            
            # 게시글 타이틀 확인
            assert profilePage.is_element_visible(ProfileLoc.PROFILE_ARTICLE_TITLE), "게시글 타이틀이 표시되지 않습니다."
            
            # 서브타이틀 확인
            assert profilePage.is_element_visible(ProfileLoc.PROFILE_ARTICLE_DESCRIPTION), "서브타이틀이 표시되지 않습니다."
            
            # 좋아요 버튼 확인
            assert profilePage.is_element_visible(ProfileLoc.PROFILE_READ_MORE_LINK), "좋아요 버튼이 표시되지 않습니다."
            
            # 태그 확인
            assert profilePage.is_element_visible(ProfileLoc.PROFILE_TAG_LIST), "태그가 표시되지 않습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"테스트 실패: {str(e)}")
    
    @pytest.mark.data_required
    def testLongTagDisplay(self, driver):
        # MYP-AUTO-010: 긴 태그 이름이 있는 게시글의 레이아웃 확인
        try:
            # 테스트 데이터 로드
            testData = loadTestData("fullDataUser")
            
            # 로그인 진행
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 프로필 페이지로 이동
            profilePage = ProfilePage(driver)
            driver.get(f"{driver.current_url}/@{testData['username']}")
            
            # 1. 'My Articles' 탭에서 긴 태그가 있는 게시글 확인
            # 태그 영역 확인
            tagElement = driver.find_element(*ProfileLoc.PROFILE_TAG_LIST)
            
            # 태그 요소의 위치와 크기 확인
            tagLocation = tagElement.location
            tagSize = tagElement.size
            
            # 게시글 요소의 위치 확인
            articleElements = driver.find_elements(*ProfileLoc.PROFILE_ARTICLE_PREVIEW)
            
            if articleElements:
                nextArticle = articleElements[0]
                nextArticleLocation = nextArticle.location
                
                # 태그 영역이 다음 게시글 영역을 침범하지 않는지 확인
                assert tagLocation['y'] + tagSize['height'] <= nextArticleLocation['y'], "긴 태그가 다음 게시글 영역을 침범합니다."
            
            # 태그 요소가 부모 컨테이너 내에 적절히 표시되는지 확인
            parentContainer = driver.find_element(*ProfileLoc.PROFILE_ARTICLE_PREVIEW)
            parentSize = parentContainer.size
            
            assert tagSize['width'] <= parentSize['width'], "태그 너비가 부모 컨테이너 너비를 초과합니다."

            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"테스트 실패: {str(e)}")

    @pytest.mark.data_required
    def testLongTagDisplayInFavoritedArticles(self, driver):
        # MYP-AUTO-011: 긴 태그 표시 확인
        try:
            # 테스트 데이터 로드
            testData = loadTestData("fullDataUser")
            
            # 로그인 및 프로필 페이지 접근
            loginPage = LoginPage(driver)
            loginPage.login(testData["email"], testData["password"])
            
            # 프로필 페이지로 이동
            profilePage = ProfilePage(driver)
            base_url = config.BASE_URL
            driver.get(f"{base_url}/@{testData['username']}")
            
            # Favorited Articles 탭 클릭
            driver.find_element(By.XPATH, ProfileLoc.FAVORITED_ARTICLES_TAB).click()
            
            # 태그 영역 확인
            tagElement = driver.find_element(*ProfileLoc.PROFILE_TAG_LIST)
            
            # 태그 요소의 위치와 크기 확인
            tagLocation = tagElement.location
            tagSize = tagElement.size
            
            # 게시글 요소의 위치 확인
            articleElements = driver.find_elements(*ProfileLoc.PROFILE_ARTICLE_PREVIEW)
            
            if articleElements:
                nextArticle = articleElements[0]
                nextArticleLocation = nextArticle.location
                
                # 태그 영역이 다음 게시글 영역을 침범하지 않는지 확인
                assert tagLocation['y'] + tagSize['height'] <= nextArticleLocation['y'], "긴 태그가 다음 게시글 영역을 침범합니다."
            
            # 태그 요소가 부모 컨테이너 내에 적절히 표시되는지 확인
            parentContainer = driver.find_element(*ProfileLoc.PROFILE_ARTICLE_PREVIEW)
            parentSize = parentContainer.size
            
            assert tagSize['width'] <= parentSize['width'], "태그 너비가 부모 컨테이너 너비를 초과합니다."

            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"긴 태그 표시 테스트 실패: {str(e)}")
    
    @pytest.mark.data_required
    def testArticleNavigationFromProfile(self, driver):
        # MYP-AUTO-012: 게시글의 상세 페이지로 이동 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("fullDataUser")
            
            # 로그인 및 프로필 페이지 접근
            loginPage = LoginPage(driver)
            loginPage.login(testData["email"], testData["password"])
            
            # 프로필 페이지로 이동
            profilePage = ProfilePage(driver)
            base_url = config.BASE_URL
            driver.get(f"{base_url}/@{testData['username']}")

            # 게시글 클릭
            articleTitleElement = driver.find_element(*ProfileLoc.PROFILE_ARTICLE_TITLE)
            articleTitleElement.click()
            
            # 게시글 상세 페이지로 이동했는지 확인
            article_page = ArticlePage(driver)

            currentUrl = article_page.get_current_url()
            assert "/article" in currentUrl, f"페이지 URL이 변경되었습니다. 현재 URL: {currentUrl}"
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"게시글 이동 테스트 실패: {str(e)}")
    
    @pytest.mark.data_required_below_ten_articles
    def testMyArticlesDisplayUnderTen(self, driver):
        # MYP-AUTO-013: My Articles 탭 게시글 10개 이하
        try:
            # 테스트 데이터 로드
            testData = loadTestData("belowTenArticlesUser")
            
            # 로그인 및 프로필 페이지 접근
            loginPage = LoginPage(driver)
            loginPage.login(testData["email"], testData["password"])
            
            # 프로필 페이지로 이동
            profilePage = ProfilePage(driver)
            base_url = config.BASE_URL
            driver.get(f"{base_url}/@{testData['username']}")  
            
            # 게시글 목록 요소 가져오기
            articleElements = driver.find_elements(*ProfileLoc.PROFILE_ARTICLE_PREVIEW)
            
            # 예상 게시글 수와 실제 표시된 게시글 수 비교
            actual_count = len(articleElements)
            
            assert actual_count <= 10, f"표시된 게시글 수가 예상과 다릅니다. 예상: 10개 이하, 실제: {actual_count}"
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"10개 이하 게시글 표시 테스트 실패: {str(e)}")
    
    @pytest.mark.data_required
    def testMyArticlesPagination(self, driver):
        # MYP-AUTO-014: My Articles 탭에서 10개 초과 게시글이 있을 때 페이지네이션
        try:
            # 테스트 데이터 로드
            testData = loadTestData("fullDataUser")
            
            # 로그인 및 프로필 페이지 접근
            loginPage = LoginPage(driver)
            loginPage.login(testData["email"], testData["password"])
            
            # 프로필 페이지로 이동
            profilePage = ProfilePage(driver)
            base_url = config.BASE_URL
            driver.get(f"{base_url}/@{testData['username']}")

            
            # My Articles 탭 클릭 (기본 선택되어 있을 수 있음)
            driver.find_element(*ProfileLoc.PROFILE_MY_ARTICLES_TAB).click()
            
            # 첫 페이지 게시글 수 확인
            first_page_articles = driver.find_elements(*ProfileLoc.PROFILE_ARTICLE_PREVIEW)
            assert len(first_page_articles) == 10, f"첫 페이지에 10개의 게시글이 표시되어야 합니다. 실제: {len(first_page_articles)}"
            
            # 페이지네이션 UI 확인
            pagination = driver.find_element(*ProfileLoc.PROFILE_PAGE_ITEMS)
            assert pagination.is_displayed(), "페이지네이션 UI가 표시되지 않습니다"
            
            # 페이지 2로 이동
            page_two_button = driver.find_elements(*ProfileLoc.PROFILE_PAGE_ITEMS)
            page_two_button[1].click()
            
            # 두 번째 페이지 게시글 수 확인
            profilePage.is_element_visible(ProfileLoc.PROFILE_ARTICLE_PREVIEW)  # 페이지 로딩 대기
            second_page_articles = driver.find_elements(*ProfileLoc.PROFILE_ARTICLE_PREVIEW)
            expected_second_page_count = testData["total_articleCount"] - 10
            
            assert len(second_page_articles) == expected_second_page_count, \
                f"두 번째 페이지에 {expected_second_page_count}개의 게시글이 표시되어야 합니다. 실제: {len(second_page_articles)}"
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"페이지네이션 테스트 실패: {str(e)}")
    
    @pytest.mark.data_required
    def testLikeButtonToggleOnProfile(self, driver):
        # MYP-AUTO-015: My Articles 탭에서 좋아요 버튼 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("fullDataUser")
            
            # 로그인 및 프로필 페이지 접근
            loginPage = LoginPage(driver)
            loginPage.login(testData["email"], testData["password"])
            
            # 프로필 페이지로 이동
            profilePage = ProfilePage(driver)
            base_url = config.BASE_URL
            driver.get(f"{base_url}/@{testData['username']}")
            
            # My Articles 탭 클릭
            driver.find_element(*ProfileLoc.PROFILE_MY_ARTICLES_TAB).click()
            
            # 첫 번째 게시글의 좋아요 버튼 및 카운트 확인
            likeButton = driver.find_element(*ProfileLoc.PROFILE_FAVORITE_COUNT)
            initialCount_text = likeButton.text.strip()
            initialCount = int(initialCount_text) if initialCount_text else 0
            
            # 좋아요 버튼 클릭
            likeButton.click()
            
            # UI 업데이트 확인 (버튼 스타일 변경)
            profilePage.is_element_visible(ProfileLoc.PROFILE_FAVORITE_COUNT)
            
            # 카운트 증가 확인
            updatedLikeButton = driver.find_element(*ProfileLoc.PROFILE_FAVORITE_COUNT)
            updatedCountText = updatedLikeButton.text.strip()
            updated_count = int(updatedCountText) if updatedCountText else 0
            
            assert updated_count == initialCount + 1, \
                f"좋아요 카운트가 증가해야 합니다. 초기: {initialCount}, 업데이트: {updated_count}"
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"좋아요 버튼 토글 테스트 실패: {str(e)}")

    @pytest.mark.data_required
    def testToggleFavoriteOnOwProfile(self, driver):
        # MYP-AUTO-016: 좋아요 버튼 토글 해제 기능 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("fullDataUser")
            
            # 로그인 진행
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 자신의 프로필 페이지로 이동
            profilePage = ProfilePage(driver)
            driver.get(f"{driver.current_url}/@{testData['username']}")
            
            # 좋아요 버튼 상태 확인 (활성화 상태인지)
            favoriteButton = driver.find_element(*ProfileLoc.PROFILE_FAVORITE_COUNT)
            isActive = "btn-primary" in favoriteButton.get_attribute("class")
            assert isActive, "좋아요 버튼이 활성화 상태가 아닙니다."
            
            # 좋아요 카운트 초기값 저장
            initialCount = int(favoriteButton.text.strip())
            
            # 좋아요 버튼 클릭
            favoriteButton.click()
            time.sleep(1)  # UI 업데이트 대기
            
            # 좋아요 버튼 상태 변경 확인 (비활성화 상태로 변경되었는지)
            favoriteButton = driver.find_element(*ProfileLoc.PROFILE_FAVORITE_COUNT)
            isInactive = "btn-outline-primary" in favoriteButton.get_attribute("class")
            assert isInactive, "좋아요 버튼이 비활성화 상태로 변경되지 않았습니다."
            
            # 좋아요 카운트 감소 확인
            updated_count = favoriteButton.text.strip()
            assert updated_count == initialCount - 1, f"좋아요 카운트가 예상대로 감소하지 않았습니다. 예상: {initialCount-1}, 실제: {updated_count}"
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise

    @pytest.mark.data_required_below_ten_articles
    def testFavoriteArticleAppearsInFavoritedTab(self, driver):
        # MYP-AUTO-017: 좋아요한 게시글이 Favorited Articles 탭에 표시되는지 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("belowTenArticlesUser")
            
            # 로그인 진행
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 홈페이지로 이동하여 Global Feed 클릭
            homePage = HomePage(driver)
            homePage.clickGlobalFeedTab()
            
            # 게시글 제목 저장 (나중에 비교용)
            articleTitles = homePage.getArticleTitles()
            targetArticleTitle = articleTitles[0]  # 첫 번째 게시글 선택
            
            # 좋아요 버튼 클릭
            driver.find_element(*HomeLoc.HOME_ARTICLE_LIKE_BUTTON).click()
            time.sleep(1)  # UI 업데이트 대기
            
            # 사용자 프로필 페이지로 이동
            profilePage = ProfilePage(driver)
            driver.get(f"{driver.current_url.split('/#')[0]}/#/@{testData['username']}")
            
            # Favorited Articles 탭 클릭
            driver.find_element(*ProfileLoc.PROFILE_MY_ARTICLES_ACTIVE_TAB).click()
            time.sleep(1)  # 탭 전환 대기
            
            # 좋아요한 게시글이 목록에 표시되는지 확인
            favoritedArticleTitles = homePage.getArticleTitles()
            assert targetArticleTitle in favoritedArticleTitles, f"좋아요한 게시글 '{targetArticleTitle}'이 Favorited Articles 탭에 표시되지 않습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise

    @pytest.mark.data_required_below_ten_articles
    def testUnfavoriteArticleRemovedFromFavoritedTab(self, driver):
        # MYP-AUTO-018: 좋아요 해제한 게시글이 Favorited Articles 탭에서 제거되는지 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("belowTenArticlesUser")
            
            # 로그인 진행
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 사용자 프로필 페이지로 이동
            profilePage = ProfilePage(driver)
            driver.get(f"{driver.current_url.split('/#')[0]}/#/@{testData['username']}")
            
            # Favorited Articles 탭 클릭
            driver.find_element(*ProfileLoc.PROFILE_FAVORITED_ARTICLES_TAB).click()
            time.sleep(1)  # 탭 전환 대기
            
            # 좋아요한 게시글 제목 저장
            homePage = HomePage(driver)
            articleTitlesBefore = homePage.getArticleTitles()
            assert len(articleTitlesBefore) > 0, "좋아요한 게시글이 없습니다."
            targetArticleTitle = articleTitlesBefore[0]  # 첫 번째 게시글 선택
            
            # 좋아요 버튼 클릭하여 좋아요 해제
            driver.find_element(*ProfileLoc.PROFILE_FAVORITE_BTN).click()
            time.sleep(1)  # UI 업데이트 대기
            
            # 페이지 새로고침
            driver.refresh()
            time.sleep(2)  # 페이지 로딩 대기
            
            # Favorited Articles 탭 다시 클릭
            driver.find_element(*ProfileLoc.PROFILE_FAVORITED_ARTICLES_TAB).click()
            time.sleep(1)  # 탭 전환 대기
            
            # 좋아요 해제한 게시글이 목록에서 제거되었는지 확인
            articleTitlesAfter = homePage.getArticleTitles()
            
            # 게시글이 없거나 해당 게시글이 목록에 없는지 확인
            if len(articleTitlesAfter) == 0:
                assert True, "모든 게시글이 제거되었습니다."
            else:
                assert targetArticleTitle not in articleTitlesAfter, f"좋아요 해제한 게시글 '{targetArticleTitle}'이 여전히 Favorited Articles 탭에 표시됩니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise

    @pytest.mark.data_required_below_ten_articles
    def testFavoritedArticlesDisplayWithinLimit(self, driver):
        # MYP-AUTO-019: 10개 이하의 좋아요한 게시글이 모두 표시되는지 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("belowTenArticlesUser")
            
            # 로그인 진행
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 사용자 프로필 페이지로 이동
            profilePage = ProfilePage(driver)
            driver.get(f"{driver.current_url.split('/#')[0]}/#/@{testData['username']}")
            
            # Favorited Articles 탭 클릭
            driver.find_element(*ProfileLoc.PROFILE_FAVORITED_ARTICLES_TAB).click()
            time.sleep(1)  # 탭 전환 대기
            
            # 좋아요한 게시글 수 확인
            homePage = HomePage(driver)
            articleTitles = homePage.getArticleTitles()
            expectedCount = 10
            
            assert len(articleTitles) <= expectedCount, f"좋아요한 게시글 수가 예상과 다릅니다. 예상: {expectedCount}, 실제: {len(articleTitles)}"
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise

    @pytest.mark.data_required
    def testFavoritedArticlesPagination(self, driver):
        # MYP-AUTO-020: 10개 초과의 좋아요한 게시글에 대한 페이지네이션 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("fullDataUser")
            
            # 로그인 진행
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 사용자 프로필 페이지로 이동
            profilePage = ProfilePage(driver)
            driver.get(f"{driver.current_url.split('/#')[0]}/#/@{testData['username']}")
            
            # Favorited Articles 탭 클릭
            driver.find_element(*ProfileLoc.PROFILE_FAVORITED_ARTICLES_TAB).click()
            time.sleep(1)  # 탭 전환 대기
            
            # 첫 페이지 게시글 수 확인
            homePage = HomePage(driver)
            first_page_articles = homePage.getArticleTitles()
            assert len(first_page_articles) == 10, f"첫 페이지에 표시된 게시글 수가 예상과 다릅니다. 예상: 10, 실제: {len(first_page_articles)}"
            
            # 페이지네이션 UI 확인
            pagination = driver.find_elements(*ProfileLoc.PROFILE_PAGE_ITEMS)
            assert len(pagination) > 0, "페이지네이션 UI가 표시되지 않습니다."
            
            # 2번 페이지로 이동
            pagination[1].click()
            time.sleep(1)  # 페이지 전환 대기
            
            # 두 번째 페이지 게시글 수 확인
            second_page_articles = homePage.getArticleTitles()
            expected_remaining = testData.get("total_articles", 20) - 10
            assert len(second_page_articles) == expected_remaining, f"두 번째 페이지에 표시된 게시글 수가 예상과 다릅니다. 예상: {expected_remaining}, 실제: {len(second_page_articles)}"
            
            # 첫 페이지와 두 번째 페이지의 게시글이 중복되지 않는지 확인
            for article in second_page_articles:
                assert article not in first_page_articles, f"게시글 '{article}'이 첫 페이지와 두 번째 페이지에 모두 표시됩니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise