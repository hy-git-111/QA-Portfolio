import os
import sys
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
from pages.signup_page import SignupPage
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.base_page import BasePage

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

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

logger = setup_logger(__name__)

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

def goToSettings(driver, testData):
    # 각 테스트 전에 로그인 상태로 설정하는 함수
    # 로그인 페이지로 이동
    loginPage = LoginPage(driver)
    loginPage.navigate()
    
    # 로그인
    loginPage.login(testData["email"], testData["password"])
    
    # Global Feed 탭 클릭
    homePage = HomePage(driver)
    driver.find_element(*HomeLoc.NAV_SETTINGS_LINK).click()
    homePage.isPageLoaded()
    
class TestSettings:
    # 세팅 관련 테스트 클래스

    @pytest.mark.data_not_required
    def testAccessSettingsPage(self, driver):
        # SET-AUTO-001: 설정 페이지 진입 확인하는 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("successLogin")
            
            # 설정정 페이지로 이동
            goToSettings(driver, testData)

            # 설정 페이지 접근 확인
            settingsPage = SettingsPage(driver)
            assert settingsPage.wait_for_url_contains("/settings"), "설정 페이지로 이동하지 않았습니다."
            assert settingsPage.isSettingsPageLoaded(), "설정 페이지가 제대로 로드되지 않았습니다."
            
            # 설정 페이지 요소 확인
            assert settingsPage.is_element_visible(SettingsLoc.SETTINGS_UPDATE_BUTTON), "설정 페이지의 업데이트 버튼이 표시되지 않습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"설정 페이지 접근 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_not_required
    def testSettingsPageLayout(self, driver):
        # SET-AUTO-002: 설정 페이지의 전체적인 레이아웃을 확인하는 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("successLogin")
            
            # 설정정 페이지로 이동
            goToSettings(driver, testData)

            # 페이지 제목 확인
            page_title = driver.find_element(*SettingsLoc.SETTINGS_TITLE).text
            assert page_title == "Your Settings", f"페이지 제목이 일치하지 않습니다. 실제: {page_title}"
            
            # 입력 필드 순서 확인
            form_elements = [
                SettingsLoc.SETTINGS_PROFILE_PICTURE_INPUT,
                SettingsLoc.SETTINGS_USERNAME_INPUT,
                SettingsLoc.SETTINGS_BIO_TEXTAREA,
                SettingsLoc.SETTINGS_EMAIL_INPUT,
                SettingsLoc.SETTINGS_PASSWORD_INPUT
            ]
            
            # 각 요소가 존재하는지 확인
            settingsPage = SettingsPage(driver)
            for element_locator in form_elements:
                assert settingsPage.is_element_present(element_locator), f"요소가 존재하지 않습니다: {element_locator}"
            
            # 버튼 확인
            assert settingsPage.is_element_present(SettingsLoc.SETTINGS_UPDATE_BUTTON), "Update Settings 버튼이 존재하지 않습니다."
            assert settingsPage.is_element_present(SettingsLoc.SETTINGS_LOGOUT_BUTTON), "Logout 버튼이 존재하지 않습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 설정 페이지 레이아웃 테스트 성공")
        except Exception as e:
            logger.warning(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            raise
    
    @pytest.mark.data_not_required
    def testSettingsPagePlaceholders(self, driver):
        # SET-AUTO-003: 설정 페이지의 입력 필드 플레이스홀더를 확인하는 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("successLogin")
            
            # 설정정 페이지로 이동
            goToSettings(driver, testData)

            # 각 입력 필드의 플레이스홀더 확인
            imageUrlPlaceholder = driver.find_element(*SettingsLoc.SETTINGS_PROFILE_PICTURE_INPUT).get_attribute("placeholder")
            assert "URL of profile picture" in imageUrlPlaceholder, f"이미지 URL 플레이스홀더가 일치하지 않습니다. 실제: {imageUrlPlaceholder}"
            
            usernamePlaceholder = driver.find_element(*SettingsLoc.SETTINGS_USERNAME_INPUT).get_attribute("placeholder")
            assert "Username" in usernamePlaceholder, f"사용자 이름 플레이스홀더가 일치하지 않습니다. 실제: {usernamePlaceholder}"
            
            bioPlaceholder = driver.find_element(*SettingsLoc.SETTINGS_BIO_TEXTAREA).get_attribute("placeholder")
            assert "Short bio about you" in bioPlaceholder, f"상태 소개 플레이스홀더가 일치하지 않습니다. 실제: {bioPlaceholder}"
            
            emailPlaceholder = driver.find_element(*SettingsLoc.SETTINGS_EMAIL_INPUT).get_attribute("placeholder")
            assert "Email" in emailPlaceholder, f"이메일 플레이스홀더가 일치하지 않습니다. 실제: {emailPlaceholder}"
            
            passwordPlaceholder = driver.find_element(*SettingsLoc.SETTINGS_PASSWORD_INPUT).get_attribute("placeholder")
            assert "New Password" in passwordPlaceholder, f"비밀번호 플레이스홀더가 일치하지 않습니다. 실제: {passwordPlaceholder}"
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 설정 페이지 플레이스홀더 테스트 성공")
        except Exception as e:
            logger.warning(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            raise
    
    @pytest.mark.data_not_required
    def testLogoutFunctionality(self, driver):
        # SET-AUTO-004: 로그아웃 기능을 확인하는 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("successLogin")
            
            # 설정정 페이지로 이동
            goToSettings(driver, testData)

            # 로그아웃 버튼 클릭
            driver.find_element(*SettingsLoc.SETTINGS_LOGOUT_BUTTON).click()
            
            # 홈페이지로 리다이렉션 확인
            homePage = HomePage(driver)
            homePage.isPageLoaded()

            # 로그아웃 상태 확인 (로그인 버튼이 표시되는지)
            basePage = BasePage(driver)
            homePage = HomePage(driver)
            assert basePage.is_element_visible(*HomeLoc.HOME_NAV_LOGIN), "로그아웃 후 로그인 버튼이 표시되지 않습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 로그아웃 기능 테스트 성공")
        except Exception as e:
            logger.warning(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            raise
    
    @pytest.mark.data_not_required
    def testRemoveProfileImage(self, driver):
        # SET-AUTO-005: 프로필 이미지 URL 제거 기능을 확인하는 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("successLogin")
            
            # 설정정 페이지로 이동
            goToSettings(driver, testData)

            # 기존 이미지 URL 삭제
            settingsPage = SettingsPage(driver)
            settingsPage.clearField(SettingsLoc.SETTINGS_PROFILE_PICTURE_INPUT)
            
            # 업데이트 버튼 클릭
            settingsPage.clickUpdateButton()
            
            # 홈페이지로 리다이렉션 확인
            homePage = HomePage(driver)
            homePage.isPageLoaded()

            # 네비게이션 바의 프로필 이미지 확인
            profile_img = driver.find_element(*SettingsLoc.SETTINGS_USER_PIC)
            img_src = profile_img.get_attribute("src")
            
            # 기본 이미지 확인 (기본 이미지는 일반적으로 상대 경로이거나 특정 패턴을 가짐)
            assert not img_src or "default" in img_src.lower() or img_src.startswith("data:"), "프로필 이미지가 기본 이미지로 변경되지 않았습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 프로필 이미지 제거 테스트 성공")
        except Exception as e:
            logger.warning(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            raise
    
    @pytest.mark.data_not_required
    def testUpdateProfileImage(self, driver):
        # SET-AUTO-006: 프로필 이미지 URL 업데이트 기능을 확인하는 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("successLogin")
            
            # 설정정 페이지로 이동
            goToSettings(driver, testData)

            # 새로운 이미지 URL 입력
            new_image_url = "https://picsum.photos/200"
            settingsPage = SettingsPage(driver)
            settingsPage.enterImageUrl(new_image_url)
            
            # 업데이트 버튼 클릭
            settingsPage.clickUpdateButton()
            
            # 홈페이지로 리다이렉션 확인
            base_age = BasePage(driver)
            base_age.wait_for_url_contains("home")
            
            # 네비게이션 바의 프로필 이미지 확인
            profile_img = driver.find_element(*SettingsLoc.SETTINGS_USER_PIC)
            img_src = profile_img.get_attribute("src")
            
            # 새로운 이미지 URL로 변경되었는지 확인
            assert new_image_url in img_src, f"프로필 이미지가 새 URL로 변경되지 않았습니다. 실제: {img_src}"
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 프로필 이미지 업데이트 테스트 성공")
        except Exception as e:
            logger.warning(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            raise
    
    @pytest.mark.data_not_required
    def test_profile_picture_update(self, driver):
        # SET-AUTO-007: 비유효한 프로필 이미지 URL 업데이트 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("successLogin")
            
            # 설정 페이지로 이동
            goToSettings(driver, testData)
            
            # 새로운 이미지 URL 입력
            new_image_url = "https://elice.com"
            settingsPage = SettingsPage(driver)
            settingsPage.enterImageUrl(new_image_url)
            
            # 업데이트 버튼 클릭
            settingsPage.clickUpdateButton()
            
            # 홈페이지로 리다이렉션 확인
            homePage = HomePage(driver)
            assert homePage.isPageLoaded(), "홈페이지로 리다이렉션되지 않았습니다."

            # 네비게이션 바의 프로필 이미지 확인
            profile_img = driver.find_element(*SettingsLoc.SETTINGS_USER_PIC)
            img_src = profile_img.get_attribute("src")

            # 새로운 이미지 URL로 변경되었는지 확인
            assert "https://api.realworld.io/images/smiley-cyrus.jpeg" in img_src, f"프로필 이미지가 기본 프로필로 변경되지 않았습니다. 실제: {img_src}"

            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_not_required
    def test_empty_username_update(self, driver):
        # SET-AUTO-008: 빈 닉네임으로 업데이트 시도 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("successLogin")
            
            # 설정 페이지로 이동
            goToSettings(driver, testData)
            
            # 현재 사용자명 저장
            settingsPage = SettingsPage(driver)
            original_username = settingsPage.get_current_url().split("@")[1].split("/")[0]
            
            # Username 입력 필드의 기존 닉네임 삭제
            settingsPage.clearField(SettingsLoc.SETTINGS_USERNAME_INPUT)

            # Update Settings 버튼 클릭
            settingsPage.clickUpdateButton()
            
            # 설정 페이지에 머물러 있는지 확인 (에러 메시지 표시 또는 페이지 이동 없음)
            assert settingsPage.isSettingsPageLoaded(), "설정 페이지를 벗어났습니다."
            
            # 홈페이지로 이동하여 사용자명이 변경되지 않았는지 확인
            homePage = HomePage(driver)
            settingsPage.clickLogoButton()
            settingsPage.clickLogoButton()
            
            # 네비게이션 바에서 사용자명 확인
            current_username = homePage.getNavigateUserName()
            assert current_username == original_username, f"사용자명이 변경되었습니다. 예상: {original_username}, 실제: {current_username}"
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_not_required
    def test_duplicate_username_update(self, driver):
        # SET-AUTO-009: 중복된 닉네임으로 업데이트 시도 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("successLogin")
            existing_username = loadTestData("fullDataUser")
            
            # 설정 페이지로 이동
            goToSettings(driver, testData)
            settingsPage = SettingsPage(driver)

            # 이미 존재하는 사용자명 입력
            settingsPage.clearField(SettingsLoc.SETTINGS_USERNAME_INPUT)
            settingsPage.enterUsername(existing_username["userName"])

            # Update Settings 버튼 클릭
            settingsPage.clickUpdateButton()

            # 오류 메시지 확인
            # 에러 메시지 요소가 존재하는지 확인
            assert settingsPage.is_element_visible(SettingsLoc.SETTINGS_USERNAME_INPUT), "오류 메시지가 표시되지 않습니다."
            
            # 오류 메시지 내용 확인
            error_message = driver.find_element(*SettingsLoc.SETTINGS_USERNAME_INPUT).text  # ✅ 변수명 통일 필요
            assert "username has already been taken" in error_message.lower(), f"예상된 오류 메시지가 표시되지 않습니다. 실제: {error_message}"
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_not_required
    def test_valid_username_update(self, driver):
        # SET-AUTO-010: 유효한 새 닉네임으로 업데이트 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("fullDataUser")
            new_username = loadTestData("validUsernameUpdate")
            
            # 설정 페이지로 이동
            goToSettings(driver, testData)

            # 새로운 유효한 사용자명 입력
            settingsPage = SettingsPage(driver)
            settingsPage.clearField(SettingsLoc.SETTINGS_USERNAME_INPUT)
            settingsPage.enterUsername(new_username)
            
            # 홈페이지로 리다이렉션 확인
            homePage = HomePage(driver)
            assert homePage.isPageLoaded(), "홈페이지로 리다이렉션되지 않았습니다."
            
            # 네비게이션 바에서 변경된 닉네임 확인
            current_username = homePage.getNavigateUserName()
            assert current_username == new_username, f"사용자명이 변경되지 않았습니다. 예상: {new_username}, 실제: {current_username}"
            assert current_username == new_username, f"사용자명이 변경되지 않았습니다. 예상: {new_username}, 실제: {current_username}"
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_not_required
    def test_bio_update(self, driver):
        # SET-AUTO-011: 상태소개(bio) 업데이트 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("fullDataUser")
            new_bio = loadTestData("shortNewBio")
            
            # 설정 페이지로 이동
            goToSettings(driver, testData)
            
            # 새로운 상태소개 입력
            settingsPage = SettingsPage(driver)
            settingsPage.clearField(SettingsLoc.SETTINGS_BIO_TEXTAREA)
            settingsPage.enterBio(new_bio)
            
            # 홈페이지로 리다이렉션 확인
            home_page = HomePage(driver)
            assert home_page.isPageLoaded(), "홈페이지로 리다이렉션되지 않았습니다."
            
            # 현재 사용자명 가져오기
            username = home_page.getNavigateUserName()
            
            # 프로필 페이지로 이동
            driver.get(f"{driver.current_url.split('#')[0]}/@{username}")
            profile_page = ProfilePage(driver)
            
            # 프로필 페이지에서 상태소개 확인
            user_bio = profile_page.getUserBio()
            assert user_bio == testData["new_bio"], f"상태소개가 변경되지 않았습니다. 예상: {testData['new_bio']}, 실제: {user_bio}"
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_not_required
    def test_remove_bio_from_settings(self, driver):
        # SET-AUTO-012: 사용자 상태소개(bio) 삭제 후 프로필 페이지에서 확인
        try:
            # 테스트 데이터 로드
            testData = loadTestData("fullDataUser")
            
            # 설정 페이지로 이동
            goToSettings(driver, testData)
            
            # 새로운 상태소개 입력
            settings_page = SettingsPage(driver)
            settings_page.clearField(SettingsLoc.SETTINGS_BIO_TEXTAREA)
            settings_page.clickUpdateButton()
            
            # 현재 사용자명 가져오기
            home_page = HomePage(driver)
            username = home_page.getNavigateUserName()

            # 프로필 페이지로 이동
            driver.get(f"{driver.current_url.split('#')[0]}/@{username}")
            profile_page = ProfilePage(driver)
            
            # 프로필 페이지에서 상태소개 확인
            user_bio = profile_page.getUserBio()
            assert user_bio == testData["new_bio"], f"상태소개가 변경되지 않았습니다. 예상: {testData['new_bio']}, 실제: {user_bio}"
            
            # 기대 결과: 프로필 페이지에서 상태소개가 비어있는 것으로 표시되어야 함
            assert user_bio == "" or user_bio is None, f"상태소개가 비어있지 않습니다. 현재 값: {user_bio}"
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공: 상태소개가 성공적으로 삭제되었습니다.")
            
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"상태소개 삭제 테스트 실패: {str(e)}")
    
    @pytest.mark.data_not_required
    def test_multiline_bio_in_settings(self, driver):
        # SET-AUTO-013: 여러 줄로 구성된 상태소개(bio) 입력 후 프로필 페이지에서 확인
        try:
            # 테스트 데이터 준비
            testData = loadTestData("successLogin")
            newLineText = loadTestData("newLinetext")

            # 설정 페이지 진입
            goToSettings(driver, testData)

            # bio 텍스트 영역에 여러 줄로 구성된 텍스트 입력
            settingsPage = SettingsPage(driver)
            settingsPage.clearField(SettingsLoc.SETTINGS_BIO_TEXTAREA)
            settingsPage.enterBio(newLineText)
            
            # 'Update Settings' 버튼 클릭
            settingsPage.clickUpdateButton()
            
            # 사용자 프로필 페이지로 이동하여 상태소개 영역 확인
            homePage = HomePage(driver)
            username = homePage.getNavigateUserName()
            driver.get(f"{driver.current_url.split('#')[0]}@{username}")
            
            # 프로필 페이지에서 상태소개 확인
            profile_page = ProfilePage(driver)
            user_bio = profile_page.getUserBio()
            
            # 기대 결과: 프로필 페이지에서 입력한 줄바꿈이 적용되어 여러 줄로 표시되어야 함
            assert "첫 번째 줄" in user_bio and "두 번째 줄" in user_bio, f"상태소개에 줄바꿈이 제대로 적용되지 않았습니다. 현재 값: {user_bio}"
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공: 여러 줄 상태소개가 성공적으로 적용되었습니다.")
        
            
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"여러 줄 상태소개 테스트 실패: {str(e)}")
    
    @pytest.mark.data_not_required
    def test_invalid_email_without_at_symbol(self, driver):
        # SET-AUTO-014: @ 기호 없는 이메일 주소 입력 시 오류 메시지 확인
        try:
            # 테스트 데이터 준비
            testData = loadTestData("successLogin")
            wrongEmail = loadTestData("noAtMarkEmail")

            # 설정 페이지 진입
            goToSettings(driver, testData)

            # 'Email' 입력 필드에 @ 기호 없이 텍스트 입력
            settingsPage = SettingsPage(driver)
            settingsPage.clearField(SettingsLoc.SETTINGS_EMAIL_INPUT)
            settingsPage.enterEmail(wrongEmail)

            # 'Update Settings' 버튼 클릭
            settingsPage.clickUpdateButton()

            # 오류 메시지 확인
            error_message = driver.find_element(*SettingsLoc.SETTINGS_EMAIL_INPUT).text
            expected_error = f"이메일 주소에 '@'를 포함해 주세요. '{wrongEmail}'에 '@'가 없습니다."

            # 기대 결과: 오류 메시지가 표시되어야 함
            assert expected_error in error_message or "Please include an '@' in the email address" in error_message, f"예상된 오류 메시지가 표시되지 않았습니다. 현재 메시지: {error_message}"
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공: @ 기호 없는 이메일 오류 메시지 확인")

        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"@ 기호 없는 이메일 테스트 실패: {str(e)}")
    
    @pytest.mark.data_not_required
    def test_invalid_email_with_special_chars(self, driver):
        # SET-AUTO-015: 한글 또는 허용되지 않는 특수문자가 포함된 이메일 입력 시 오류 메시지 확인
        try:
            # 테스트 데이터 준비
            testData = loadTestData("successLogin")
            wrongEmail = loadTestData("includeNotAllowedCharEmail")

            # 설정 페이지 진입
            goToSettings(driver, testData)

            # 'Email' 입력 필드에 한글 또는 허용되지 않는 특수문자가 포함된 이메일 업데이트트
            settingsPage = SettingsPage(driver)
            settingsPage.clearField(SettingsLoc.SETTINGS_EMAIL_INPUT)
            settingsPage.updateSettings("", "", "", wrongEmail, "")

            # 오류 메시지 확인
            error_message = driver.find_element(*SettingsLoc.SETTINGS_EMAIL_INPUT).text
            expected_error = "'@' 앞 부분에 기호가 포함되면 안됩니다."

            # 기대 결과: 오류 메시지가 표시되어야 함
            assert expected_error in error_message or "A part following '@' should not contain the symbol" in error_message, f"예상된 오류 메시지가 표시되지 않았습니다. 현재 메시지: {error_message}"
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공: 특수문자 포함 이메일 오류 메시지 확인")

        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"특수문자 포함 이메일 테스트 실패: {str(e)}")
    
    @pytest.mark.data_not_required
    def test_empty_email_validation(self, driver):
        # SET-AUTO-016: 이메일 필드를 비워둔 상태로 업데이트 시도 시 검증
        try:
            # 테스트 준비
            testData = loadTestData("successLogin")
            goToSettings(driver, testData)

            # 기존 이메일 저장
            original_email = driver.find_element(*SettingsLoc.SETTINGS_EMAIL_INPUT).get_attribute("value")
            
            # 'Email' 입력 필드의 기존 이메일을 모두 삭제
            settingsPage = SettingsPage(driver)
            settingsPage.clearField(SettingsLoc.SETTINGS_EMAIL_INPUT)
            
            # 'Update Settings' 버튼 클릭
            settingsPage.clickUpdateButton()
            
            # 페이지 새로고침 후 이메일 필드 확인
            driver.refresh()
            current_email = driver.find_element(*SettingsLoc.SETTINGS_EMAIL_INPUT).get_attribute("value")
            
            # 기대 결과: 이메일 필드가 비어있는 상태로 업데이트되지 않아야 함
            assert current_email != "", "이메일 필드가 비어있는 상태로 업데이트되었습니다."
            assert current_email == original_email, f"이메일이 변경되었습니다. 원래 값: {original_email}, 현재 값: {current_email}"
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공: 빈 이메일 필드 검증 완료")
            
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"빈 이메일 필드 테스트 실패: {str(e)}")

    @pytest.mark.data_required
    def test_update_email_with_existing_email(self, driver):
        # SET-AUTO-017: 이미 존재하는 이메일로 업데이트 시도 시 오류 메시지 확인 테스트
        try:
            # 테스트 준비
            testData = loadTestData("successLogin")
            goToSettings(driver, testData)

            # 이미 존재하는 이메일 입력
            existing_email = loadTestData("email")
            settingsPage = SettingsPage(driver)
            settingsPage.clearField(SettingsLoc.SETTINGS_EMAIL_INPUT)
            settingsPage.enterEmail(existing_email)

            # Update Settings 버튼 클릭
            settingsPage.clickUpdateButton()

            # 오류 메시지 확인
            error_message = driver.find_element(*SettingsLoc.ERROR_MESSAGE).text
            assert "Email has already been taken" in error_message or "이미 사용 중인 이메일" in error_message, \
                f"예상된 오류 메시지가 표시되지 않았습니다. 실제 메시지: {error_message}"
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_not_required
    def test_update_email_with_new_valid_email(self, driver):
        """
        새로운 유효한 이메일로 업데이트 성공 테스트
        
        사전 조건:
        - 로그인된 사용자 (currentUser)가 설정 페이지(/settings)에 접근.
        
        재현 절차:
        1. 'Email' 입력 필드에 새롭고, 유효하며, 시스템에 존재하지 않는 이메일 (예: newValidEmail@example.com)을 입력한다.   
        2. 'Update Settings' 버튼을 클릭한다.   
        
        기대 결과:
        이메일이 성공적으로 newValidEmail@example.com으로 변경되어 홈페이지로 리다이렉션 된다.
        """
        try:
            # 1. 새로운 유효한 이메일 입력
            new_email = self.testData["newValidEmail"]
            settingsPage.clearField(SettingsLoc.EMAIL_INPUT)
            settingsPage.enterEmail(new_email)
            settingsPage.clearField(SettingsLoc.EMAIL_INPUT)
            settingsPage.enterEmail(new_email)
            
            # 2. Update Settings 버튼 클릭
            settingsPage.clickUpdateButton()
            settingsPage.clickUpdateButton()
            
            # 홈페이지로 리다이렉션 확인
            driver.wait_for_url_contains("home")
            currentUrl = driver.current_url
            assert "/home" in currentUrl or currentUrl.endswith('/'), \
                f"홈페이지로 리다이렉션되지 않았습니다. 현재 URL: {currentUrl}"
            
            # 이메일 변경 확인 (설정 페이지 다시 접속하여 확인)
            driver.get(f"{driver.current_url.split('#')[0]}settings")
            email_field_value = driver.find_element(*Loc.EMAIL_INPUT).get_attribute("value")
            assert email_field_value == new_email, \
                f"이메일이 성공적으로 변경되지 않았습니다. 현재 이메일: {email_field_value}"
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_required
    def test_update_password_with_new_valid_password(self, driver):
        """
        새로운 유효한 비밀번호로 업데이트 성공 테스트
        
        사전 조건:
        로그인된 사용자 (currentUser)가 현재 비밀번호 oldPassword로 로그인한 상태. 설정 페이지(/settings)에 접근.
        
        재현 절차:
        1. 'New Password' 입력 필드에 새로운 유효한 비밀번호 (예: newValidPassword123)를 입력한다.   
        2. 'Update Settings' 버튼을 클릭한다.   
        
        기대 결과:
        비밀번호 변경이 성공적으로 처리되어 홈페이지로 리다이렉션 된다.
        """
        try:
            # 1. 새로운 유효한 비밀번호 입력
            new_password = self.testData["newValidPassword"]
            settingsPage.clearField(SettingsLoc.PASSWORD_INPUT)
            settingsPage.enterPassword(new_password)
            settingsPage.clearField(SettingsLoc.PASSWORD_INPUT)
            settingsPage.enterPassword(new_password)
            
            # 2. Update Settings 버튼 클릭
            settingsPage.clickUpdateButton()
            settingsPage.clickUpdateButton()
            
            # 홈페이지로 리다이렉션 확인
            driver.wait_for_url_contains("home")
            currentUrl = driver.current_url
            assert "/home" in currentUrl or currentUrl.endswith('/'), \
                f"홈페이지로 리다이렉션되지 않았습니다. 현재 URL: {currentUrl}"
            
            # 비밀번호 변경 확인 (로그아웃 후 새 비밀번호로 로그인)
            # 로그아웃 처리
            logout_link = driver.find_element(*Loc.LOGOUTBUTTON)
            logout_link.click()
            
            # 새 비밀번호로 로그인
            self.loginPage.navigate()
            self.loginPage.login(
                self.testData["currentUser"]["email"], 
                new_password
            )
            
            # 로그인 성공 확인
            assert self.login_page.isLoggedIn(), "새 비밀번호로 로그인하지 못했습니다. 비밀번호 변경이 실패했을 수 있습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_not_required
    def test_update_with_empty_password(self, driver):
        """
        빈 비밀번호로 업데이트 시도 테스트
        
        사전 조건:
        - 로그인된 사용자 (currentUser)가 설정 페이지(/settings)에 접근.
        
        재현 절차:
        1. 'New Password' 입력 필드를 비워둔다.   
        2. 'Update Settings' 버튼을 클릭한다.
        
        기대 결과:
        비밀번호가 빈 값으로 변경되지 않고 홈페이지로 리다이렉션 된다.
        """
        try:
            # 1. 비밀번호 필드를 비워둠 (이미 비어있을 수 있으므로 명시적으로 비움)
            settingsPage.clearField(SettingsLoc.PASSWORD_INPUT)
            settingsPage.clearField(SettingsLoc.PASSWORD_INPUT)
            
            # 2. Update Settings 버튼 클릭
            settingsPage.clickUpdateButton()
            settingsPage.clickUpdateButton()
            
            # 홈페이지로 리다이렉션 확인
            driver.wait_for_url_contains("home")
            currentUrl = driver.current_url
            assert "/home" in currentUrl or currentUrl.endswith('/'), \
                f"홈페이지로 리다이렉션되지 않았습니다. 현재 URL: {currentUrl}"
            
            # 비밀번호가 변경되지 않았는지 확인 (원래 비밀번호로 로그인 가능한지 확인)
            # 로그아웃 처리
            logout_link = driver.find_element(*Loc.LOGOUTBUTTON)
            logout_link.click()
            
            # 원래 비밀번호로 로그인
            self.loginPage.navigate()
            self.loginPage.login(
                self.testData["currentUser"]["email"], 
                self.testData["currentUser"]["password"]
            )
            
            # 로그인 성공 확인
            assert self.login_page.isLoggedIn(), "원래 비밀번호로 로그인하지 못했습니다. 비밀번호가 변경되었을 수 있습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_not_required
    def test_update_password_with_leading_space(self, driver):
        """
        앞에 공백이 있는 비밀번호로 업데이트 시도 테스트
        
        사전 조건:
        - 로그인된 사용자 (currentUser)가 설정 페이지(/settings)에 접근.
        
        재현 절차:
        1. 'New Password' 입력 필드에 새 비밀번호(맨 앞에 공백 한 칸 + "testpassword")를 입력한다.   
        2. 'Update Settings' 버튼을 클릭한다.   
        
        기대 결과:
        "비밀번호는 앞/뒤 공백을 포함할 수 없습니다."와 같은 오류메시지가 표시 되어야한다.
        """
        try:
            # 1. 앞에 공백이 있는 비밀번호 입력
            password_with_space = " testpassword"
            settingsPage.clearField(SettingsLoc.PASSWORD_INPUT)
            settingsPage.enterPassword(password_with_space)
            settingsPage.clearField(SettingsLoc.PASSWORD_INPUT)
            settingsPage.enterPassword(password_with_space)
            
            # 2. Update Settings 버튼 클릭
            settingsPage.clickUpdateButton()
            settingsPage.clickUpdateButton()
            
            # 오류 메시지 확인
            errorMessage = driver.find_element(*Loc.ERROR_MESSAGE).text
            expected_errorMessages = [
                "비밀번호는 앞/뒤 공백을 포함할 수 없습니다",
                "Password cannot include leading or trailing whitespace",
                "Password cannot contain leading or trailing spaces"
            ]
            
            error_found = any(expected in errorMessage for expected in expected_errorMessages)
            assert error_found, f"예상된 오류 메시지가 표시되지 않았습니다. 실제 메시지: {error_message}"
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise
```

이 코드는 JSON 형식의 테스트 케이스에 맞게 5개의 테스트 함수를 구현했습니다:

1. `test_update_email_with_existing_email`: 이미 존재하는 이메일로 업데이트 시도 시 오류 메시지 확인
2. `test_update_email_with_new_valid_email`: 새로운 유효한 이메일로 업데이트 성공 확인
3. `test_update_password_with_new_valid_password`: 새로운 유효한 비밀번호로 업데이트 성공 확인
4. `test_update_with_empty_password`: 빈 비밀번호로 업데이트 시도 시 기존 비밀번호 유지 확인
5. `test_update_password_with_leading_space`: 앞에 공백이 있는 비밀번호로 업데이트 시도 시 오류 메시지 확인

각 테스트는 POM 구조를 따르며, 공통 코드와 로케이터를 import하여 사용합니다. 또한 각 테스트에는 명확한 docstring과 한글 주석이 포함되어 있습니다. 테스트 데이터는 JSON 파일에서 로드하며, 오류 처리를 위해 try-except 구문을 사용했습니다.

# ===== 다음 배치 =====

요청하신 대로 Python + Selenium 기반의 Pytest 테스트 코드를 작성하겠습니다. 주어진 JSON 형식의 테스트케이스에 맞춰 POM 구조를 따르는 테스트 코드를 생성하겠습니다.

```python
# qa-realworld-automation/tests/test_pages.py

import os
import json
import pytest
import inspect
import time
from selenium.webdriver.common.by import By

# 페이지 객체 임포트
from pages.settings_page import SettingsPage
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.article_page import ArticlePage

# 로케이터 임포트
from locators.settings_locators import SettingsPageLocators as SettingsLoc
from locators.home_locators import HomePageLocators as HomeLoc
from locators.article_locators import ArticlePageLocators as ArticleLoc

# 유틸리티 임포트
from utils.logger import setup_logger
import config

logger = setup_logger(__name__)

def loadTestData():
    """테스트 데이터 로드 함수"""
    dataFilePath = os.path.join(config.TEST_DATA_DIR, "test_data.json")
    with open(dataFilePath, 'r', encoding='utf-8') as file:
        return json.load(file)


class TestSettingsPage:
    """설정 페이지 관련 테스트 클래스"""
    
    @pytest.mark.data_required
    def test_password_with_trailing_space(self, driver):
        """
        테스트 시나리오: 비밀번호 뒤에 공백이 있는 경우 오류 메시지 확인
        
        사전 조건:
        - 로그인된 사용자 (currentUser)가 설정 페이지(/settings)에 접근.
        
        재현 절차:
        1. 'New Password' 입력 필드에 새 비밀번호("testpassword + 뒤에 공백 한 칸")를 입력한다.
        2. 'Update Settings' 버튼을 클릭한다.
        
        기대 결과:
        "비밀번호는 앞/뒤 공백을 포함할 수 없습니다."와 같은 오류메시지가 표시 되어야한다.
        """
        try:
            # 테스트 데이터 로드
            testData = loadTestData()["login"]
            
            # 로그인 진행
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 설정 페이지로 이동
            settingsPage = SettingsPage(driver)
            driver.get(f"{driver.current_url}settings")
            
            # 설정 페이지 로드 확인
            assert settingsPage.isSettingsPageLoaded(), "설정 페이지가 로드되지 않았습니다."
            
            # 비밀번호 필드에 공백이 포함된 비밀번호 입력
            password_with_space = "testpassword "  # 뒤에 공백 한 칸 추가
            settingsPage.enterPassword(password_with_space)
            
            # Update Settings 버튼 클릭
            settingsPage.clickUpdateButton()
            
            # 오류 메시지 확인 (실제 구현에 따라 로케이터 및 메시지 내용이 다를 수 있음)
            error_element = driver.find_element(By.CSS_SELECTOR, SettingsLoc.ERROR_MESSAGE)
            assert "공백을 포함할 수 없습니다" in error_element.text, "비밀번호 공백 관련 오류 메시지가 표시되지 않았습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"비밀번호 뒤 공백 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_required
    def test_password_with_only_space(self, driver):
        """
        테스트 시나리오: 비밀번호에 공백만 입력한 경우 오류 메시지 확인
        
        사전 조건:
        - 로그인된 사용자 (currentUser)가 설정 페이지(/settings)에 접근.
        
        재현 절차:
        1. 'New Password' 입력 필드에 새 비밀번호(" ", 빈 문자열만 입력)를 입력한다.
        2. 'Update Settings' 버튼을 클릭한다.
        
        기대 결과:
        "비밀번호는 공백을 포함할 수 없습니다."와 같은 오류메시지가 표시 되어야한다.
        """
        try:
            # 테스트 데이터 로드
            testData = loadTestData()["login"]
            
            # 로그인 진행
            loginPage = LoginPage(driver)
            loginPage.navigate()
            loginPage.login(testData["email"], testData["password"])
            
            # 설정 페이지로 이동
            settingsPage = SettingsPage(driver)
            driver.get(f"{driver.current_url}settings")
            
            # 설정 페이지 로드 확인
            assert settingsPage.isSettingsPageLoaded(), "설정 페이지가 로드되지 않았습니다."
            
            # 비밀번호 필드에 공백만 입력
            space_only_password = " "
            settingsPage.enterPassword(space_only_password)
            
            # Update Settings 버튼 클릭
            settingsPage.clickUpdateButton()
            
            # 오류 메시지 확인 (실제 구현에 따라 로케이터 및 메시지 내용이 다를 수 있음)
            error_element = driver.find_element(By.CSS_SELECTOR, SettingsLoc.ERROR_MESSAGE)
            assert "공백을 포함할 수 없습니다" in error_element.text, "비밀번호 공백 관련 오류 메시지가 표시되지 않았습니다."
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")
        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"비밀번호 공백만 입력 테스트 실패: {str(e)}")
            raise

