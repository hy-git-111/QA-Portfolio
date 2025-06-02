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

class TestSocial:
    # 마이페이지 시나리오 테스트 클래스

    @pytest.mark.data_required_below_ten_articles_below_ten_articles
    def testFavoriteArticle(self, driver):
        # SOC-AUTO-001: 로그인 상태에서 게시글 좋아요(Favorite) 기능 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("belowTenArticlesUser")
            
            # 로그인
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # Global Feed 탭 클릭
            homePage = HomePage(driver)
            homePage.clickGlobalFeedTab()
            
            # 첫 번째 게시글 클릭
            driver.find_element(*HomeLoc.ARTICLE_PREVIEW).click()
            
            # Favorite 버튼 클릭 전 좋아요 수 확인
            favoriteButton = driver.find_element(*HomeLoc.HOME_ARTICLE_LIKE_COUNT)
            counterBefore = int(favoriteButton.text.strip())
            
            # Favorite 버튼 클릭
            favoriteButton.click()
            time.sleep(1)  # 버튼 상태 변경 대기
            
            # 1. Favorite 버튼 클래스 변경 확인
            favoriteButton = driver.find_element(*HomeLoc.HOME_ARTICLE_LIKE_COUNT)
            assert "btn-primary" in favoriteButton.get_attribute("class"), "Favorite 버튼이 초록색 배경으로 변경되지 않았습니다."
            
            # 2. 좋아요 수 증가 확인
            counterAfter = int(favoriteButton.text.strip())
            assert counterAfter == counterBefore + 1, f"좋아요 수가 증가하지 않았습니다. 이전: {counterBefore}, 이후: {counterAfter}"
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(str(e))
    
    @pytest.mark.data_required_below_ten_articles
    def testFavoritedArticleAppearsInProfile(self, driver):
        # SOC-AUTO-002: 좋아요한 게시글이 프로필의 Favorited Articles 탭에 표시되는지 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("belowTenArticlesUser2")
            
            # 로그인
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 홈페이지 접속 확인
            homePage = HomePage(driver)
            assert homePage.isPageLoaded(), "홈페이지가 로드되지 않았습니다."
            
            # Global Feed 탭 클릭
            homePage.clickGlobalFeedTab()
            
            # 첫 번째 게시글의 제목 저장
            articleTitle = driver.find_element(*HomeLoc.HOME_ARTICLE_TITLE).text
            
            # 첫 번째 게시글의 Favorite 버튼 클릭
            favoriteButton = driver.find_element(*HomeLoc.HOME_ARTICLE_LIKE_HART)
            favoriteButton.click()
            time.sleep(1)  # 버튼 상태 변경 대기

            # 프로필 아이콘 클릭
            driver.find_element(*HomeLoc.HOME_NAV_USER_PIC).click()
            
            # Favorited Articles 탭 클릭
            profilePage = ProfilePage(driver)
            profilePage.clickFavoritedArticleTab()
            
            # 1. 즐겨찾기한 게시글 카드가 목록에 표시되는지 확인
            articleTitles = driver.find_elements(*ProfileLoc.PROFILE_ARTICLE_PREVIEW)
            foundArticle = False
            
            for titleElement in articleTitles:
                if titleElement.text == articleTitle:
                    foundArticle = True
                    break
            
            assert foundArticle, f"즐겨찾기한 게시글 '{articleTitle}'이 Favorited Articles 탭에 표시되지 않습니다."
            
            # 2. 카드의 Favorite 버튼이 btn-primary 상태인지 확인
            favoriteButtons = driver.find_elements(*ProfileLoc.PROFILE_FAVORITE_BTN)
            assert len(favoriteButtons) > 0, "Favorite 버튼을 찾을 수 없습니다."
            assert "btn-primary" in favoriteButtons[0].get_attribute("class"), "Favorite 버튼이 초록색 배경 상태가 아닙니다."
            
            # 3. 카드 내 좋아요 수가 정수 ≥ 1 표시되는지 확인
            favoriteCounters = driver.find_elements(*ProfileLoc.PROFILE_FAVORITE_COUNT)
            assert len(favoriteCounters) > 0, "좋아요 수 카운터를 찾을 수 없습니다."
            counter_value = int(favoriteCounters[0].text)
            assert counter_value >= 1, f"좋아요 수가 1 이상이어야 하는데 {counter_value}입니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(str(e))
    
    @pytest.mark.data_required_below_ten_articles
    def testUnfavoriteArticleDisappearsFromProfile(self, driver):
        # SOC-AUTO-003: 좋아요 취소한 게시글이 프로필의 Favorited Articles 탭에서 사라지는지 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("belowTenArticlesUser")
            
            # 로그인
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 홈페이지 접속 확인
            homePage = HomePage(driver)
            assert homePage.isPageLoaded(), "홈페이지가 로드되지 않았습니다."
            
            # 프로필 아이콘 클릭
            driver.find_element(*HomeLoc.HOME_NAV_USER_PIC).click()
            
            # Favorited Articles 탭 클릭
            driver.find_element(*ProfileLoc.PROFILE_FAVORITED_ARTICLES_TAB).click()
            time.sleep(1)  # 탭 전환 대기
            
            # 첫 번째 게시글의 제목 저장
            articleTitle = driver.find_element(*ProfileLoc.PROFILE_ARTICLE_PREVIEW).text
            
            # 첫 번째 Favorite 버튼 클릭 (좋아요 취소)
            favoriteButton = driver.find_element(*ProfileLoc.PROFILE_FAVORITE_BTN)
            assert "btn-primary" in favoriteButton.get_attribute("class"), "Favorite 버튼이 이미 초록색 배경 상태가 아닙니다."
            
            favoriteButton.click()
            time.sleep(1)  # 버튼 상태 변경 대기
            
            # 1. Favorite 버튼 클래스 변경 확인
            favoriteButton = driver.find_element(*HomeLoc.HOME_ARTICLE_LIKE_COUNT)
            assert "btn-outline-primary" in favoriteButton.get_attribute("class"), "Favorite 버튼이 흰색 배경으로 변경되지 않았습니다."
            
            # 브라우저 새로고침
            driver.refresh()
            time.sleep(2)  # 페이지 로드 대기
            
            # 2. 해당 카드가 목록에서 사라졌는지 확인
            articleTitles = driver.find_elements(*HomeLoc.HOME_ARTICLE_LIKE_COUNT)
            for titleElement in articleTitles:
                assert titleElement.text != articleTitle, f"좋아요 취소한 게시글 '{articleTitle}'이 여전히 Favorited Articles 탭에 표시됩니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(str(e))
    
    @pytest.mark.data_required_below_ten_articles
    def testFollowAuthor(self, driver):
        # SOC-AUTO-004: 작성자 팔로우 기능 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("belowTenArticlesUser")
            
            # 로그인
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 홈페이지 접속 확인
            homePage = HomePage(driver)
            assert homePage.isPageLoaded(), "홈페이지가 로드되지 않았습니다."
            
            # Global Feed 탭 클릭
            homePage.clickGlobalFeedTab()

            # 게시글 클릭
            authorName = driver.find_element(*HomeLoc.HOME_ARTICLE_AUTHOR_LINK).text
            driver.find_element(*HomeLoc.HOME_ARTICLE_AUTHOR_LINK).click()
            
            # 다른 사용자 프로필 클릭
            driver.find_element(ArticleLoc.ARTICLE_ANOTHER_WRITER).click()

            # 이미 팔로우 중인 경우 언팔로우 먼저 수행
            profile_page = ProfilePage(driver)
            followButton = driver.find_element(*ProfileLoc.PROFILE_UNFOLLOW_BTN)
            if "Unfollow" in followButton.text:
                profile_page.clickUnfollowButton()
                time.sleep(1)  # 버튼 상태 변경 대기
                followButton = driver.find_element(*ProfileLoc.PROFILE_FOLLOW_BTN)
            
            # Follow 버튼 클릭
            profile_page.clickFollowButton()
            time.sleep(1)  # 버튼 상태 변경 대기
            
            # 1. 버튼 텍스트 변경 확인
            followButton = driver.find_element(*ProfileLoc.PROFILE_UNFOLLOW_BTN)
            assert f"Unfollow {authorName}" in followButton.text, f"버튼 텍스트가 'Unfollow {authorName}'으로 변경되지 않았습니다."
            
            # 2. 버튼 클래스 변경 확인
            assert "btn-secondary" in followButton.get_attribute("class"), "Follow 버튼의 클래스가 변경되지 않았습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(str(e))

    @pytest.mark.data_required_below_ten_articles
    def testFollowAuthorAndCheckFeed(self, driver):
        # SOC-AUTO-005: 팔로우한 작성자의 게시글이 Your Feed에 표시되는지 확인하는 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("belowTenArticlesUser2")
            
            # 홈페이지 접속 및 로그인 상태 확인
            homePage = HomePage(driver)
            if not homePage.isLoggedIn():
                loginPage = LoginPage(driver)
                loginPage.navigate()
                loginPage.login(testData["email"], testData["password"])
            
            # Global Feed 탭 클릭
            homePage.clickGlobalFeedTab()
        
            # 첫 번째 게시글 진입
            driver.find_element(*HomeLoc.ARTICLE_PREVIEW).click()

            # 작성자 이름 클릭하여 프로필 페이지로 이동
            driver.find_element(*ArticleLoc.ARTICLE_ANOTHER_WRITER).click()
            
            # 프로필 페이지에서 Follow 버튼 클릭
            profile_page = ProfilePage(driver)
            authorName = profile_page.getUsername()
            profile_page.clickFollowButton()
            
            # 로고 클릭하여 메인 페이지로 이동
            driver.find_element(*ProfileLoc.PROFILE_NAVBAR_BRAND).click()
            
            # Your Feed 탭 클릭
            homePage.clickYourFeedTab()
            
            # 1. Your Feed 탭이 활성화되었는지 확인
            yourFeedTab = driver.find_element(*HomeLoc.HOME_YOUR_FEED_LINK)
            assert "active" in yourFeedTab.get_attribute("class"), "Your Feed 탭이 활성화되지 않았습니다."
            
            # 2. 팔로우한 작성자의 게시글이 표시되는지 확인
            articleTitles = homePage.getArticleTitles()
            assert len(articleTitles) > 0, "Your Feed에 게시글이 표시되지 않습니다."
            
            # 작성자 이름으로 게시글 확인
            authorElements = driver.find_elements(*ArticleLoc.ARTICLE_ANOTHER_WRITER)
            found_author = False
            for element in authorElements:
                if element.text == authorName:
                    found_author = True
                    break
            
            assert found_author, f"팔로우한 작성자({authorName})의 게시글이 Your Feed에 표시되지 않습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise

    @pytest.mark.data_required_below_ten_articles
    def testFollowUnfollowButtonState(self, driver):
        # SOC-AUTO-006: 팔로우/언팔로우 버튼 상태 변경 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("belowTenArticlesUser")
            
            # 홈페이지 접속 및 로그인 상태 확인
            homePage = HomePage(driver)
            loginPage = LoginPage(driver)
            if not loginPage.isLoggedIn():
                loginPage.navigate()
                loginPage.login(testData["email"], testData["password"])
            
            # Global Feed 탭 클릭
            homePage.clickGlobalFeedTab()

            # 첫 번째 게시글 진입
            driver.find_element(*HomeLoc.ARTICLE_PREVIEW).click()
            
            # 작성자 이름 클릭하여 프로필 페이지로 이동
            driver.find_element(*ArticleLoc.ARTICLE_ANOTHER_WRITER).click()
            
            # 이미 언팔로우 중인 경우 팔로우 먼저 수행
            profile_page = ProfilePage(driver)
            authorName = profile_page.getUsername()
            if profile_page.isUnFollowing():
                profile_page.clickFollowButton()

            # Unfollow 버튼 클릭
            profile_page.clickUnfollowButton()
            
            # 결과 검증
            # 1. 버튼 텍스트가 "Follow 작성자명"으로 변경되었는지 확인
            followButton = driver.find_element(*ProfileLoc.PROFILE_UNFOLLOW_BTN)
            expected_text = f"Follow {authorName}"
            assert expected_text in followButton.text, f"버튼 텍스트가 '{expected_text}'로 변경되지 않았습니다."
            
            # 2. 버튼 클래스가 btn-outline-secondary인지 확인
            button_class = followButton.get_attribute("class")
            assert "btn-outline-secondary" in button_class, "버튼 클래스가 btn-outline-secondary로 변경되지 않았습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise

    @pytest.mark.data_required_below_ten_articles
    def testUnfollowAuthorFeedDisappears(self, driver):
        # SOC-AUTO-007: 언팔로우한 작성자의 게시글이 Your Feed에서 사라지는지 확인하는 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("belowTenArticlesUser2")
            
            # 1. 홈페이지 접속 및 로그인 상태 확인
            homePage = HomePage(driver)
            if not homePage.isLoggedIn():
                loginPage = LoginPage(driver)
                loginPage.navigate()
                loginPage.login(testData["email"], testData["password"])
            
            # Global Feed 탭 클릭
            homePage.clickGlobalFeedTab()
            
            # 첫 번째 게시글 진입
            driver.find_element(*HomeLoc.ARTICLE_PREVIEW).click()
            
            # 작성자 이름 클릭하여 프로필 페이지로 이동
            driver.find_element(*ArticleLoc.ARTICLE_ANOTHER_WRITER).click()
            
            # 이미 팔로우 중인 경우 언팔로우 먼저 수행
            profile_page = ProfilePage(driver)
            authorName = profile_page.getUsername()
            if profile_page.isFollowing():
                profile_page.clickUnfollowButton()

            profile_page.clickFollowButton()
            profile_page.clickUnfollowButton()
            
            # 5. 로고 클릭하여 메인 페이지로 이동
            driver.find_element(*ProfileLoc.PROFILE_NAVBAR_BRAND).click()
            
            # 6. Your Feed 탭 클릭
            homePage.clickYourFeedTab()
            
            # 결과 검증
            # 언팔로우한 작성자의 게시글이 표시되지 않는지 확인
            authorElements = driver.find_elements(*HomeLoc.HOME_ARTICLE_PREVIEW)
            for element in authorElements:
                assert element.text != authorName, f"언팔로우한 작성자({authorName})의 게시글이 Your Feed에 여전히 표시됩니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise

    @pytest.mark.data_not_required
    def testFavoriteArticleRedirectsTo_Login(self, driver):
        # SOC-AUTO-008: 비로그인 상태에서 Favorite 버튼 클릭 시 로그인 페이지로 이동하는지 확인하는 테스트
        try:
            # 홈페이지 접속
            homePage = HomePage(driver)
            
            # Global Feed 탭 클릭
            homePage.clickGlobalFeedTab()
            
            # 첫 번째 게시글 Favorite 클릭
            driver.find_element(*HomeLoc.HOME_ARTICLE_LIKE_COUNT).click()

            # 2. 로그인 페이지로 이동했는지 확인
            loginPage = LoginPage(driver)
            assert loginPage.wait_for_url_contains("login"), "로그인 페이지로 이동하지 않았습니다."
            
            # 2. 로그인 폼의 Email 입력 필드가 표시되는지 확인
            assert loginPage.is_element_visible(LoginLoc.LOGIN_EMAIL_INPUT), "로그인 폼의 Email 입력 필드가 표시되지 않습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise

    @pytest.mark.data_not_required
    def testFollowAuthorRedirectsToLogin(self, driver):
        # SOC-AUTO-009: 비로그인 상태에서 Follow 버튼 클릭 시 로그인 페이지로 이동하는지 확인하는 테스트
        try:
            # 홈페이지 접속
            homePage = HomePage(driver)
            
            # Global Feed 탭 클릭
            homePage.clickGlobalFeedTab()
            
            # 첫 번째 게시글 카드 클릭
            driver.find_element(*HomeLoc.ARTICLE_PREVIEW).click()
            
            # 작성자 이름 클릭하여 프로필 페이지로 이동
            driver.find_element(*ArticleLoc.ARTICLE_ANOTHER_WRITER).click()
            
            # Follow 버튼 클릭
            profilePage = ProfilePage(driver)
            driver.find_element(*ProfileLoc.PROFILE_FOLLOW_BTN).click()
            
            # 결과 검증
            # 1. 로그인 페이지로 이동했는지 확인
            loginPage = LoginPage(driver)
            assert loginPage.wait_for_url_contains("login"), "로그인 페이지로 이동하지 않았습니다."
            
            # 2. 로그인 폼의 Email 입력 필드가 표시되는지 확인
            assert loginPage.is_element_visible(LoginLoc.LOGIN_EMAIL_INPUT), "로그인 폼의 Email 입력 필드가 표시되지 않습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise