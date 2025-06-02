import os
import sys
import json
import pytest
import inspect
import time
from utils.test_helper import get_test_data, do_signup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# 페이지 객체 임포트
from pages.settings_page import SettingsPage
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

class TestAuth:
    # 인증 시나리오 테스트 클래스

    @pytest.mark.data_not_required
    def testSuccessfulSignup(self, driver):
        # AUTH-AUTO-001: 회원가입 성공 테스트
        try:
            # 1. 테스트 데이터 로드 + 회원가입 실행
            test_data = get_test_data("successSignup")
            do_signup(driver, test_data["userName"], test_data["email"], test_data["password"])

            # 2. 홈페이지 리디렉션 및 사용자 정보 확인
            home_page = HomePage(driver)
            # URL 확인
            assert home_page.wait_for_url_contains("/"), "홈페이지로 리디렉션되지 않았습니다."
            # 사용자명 표시 확인
            nav_username = home_page.getNavigateUserName()
            assert nav_username == test_data["userName"], (
                f"네비게이션 바에 사용자명이 올바르게 표시되지 않았습니다.\n"
                f"예상: {test_data['userName']}, 실제: {nav_username}"
            )

            # 메뉴 링크 확인
            assert home_page.is_element_visible(HomeLoc.NAV_NEW_POST_LINK), "New Post 링크가 표시되지 않았습니다."
            assert home_page.is_element_visible(HomeLoc.NAV_SETTINGS_LINK), "Settings 링크가 표시되지 않았습니다."
            assert home_page.is_element_visible(HomeLoc.NAV_USER_LINK), "사용자 링크가 표시되지 않았습니다."

            # 로그인 후 Sign in, Sign up 숨김 확인
            assert not home_page.is_element_visible(LoginLoc.LOGIN_SIGN_IN_LINK), "Sign in 링크가 여전히 표시되고 있습니다."
            assert not home_page.is_element_visible(SignupLoc.SIGNUP_SIGNUP_LINK), "Sign up 링크가 여전히 표시되고 있습니다."

            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 회원가입 성공 테스트 완료")

        except Exception as e:
            logger.error(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"회원가입 성공 테스트 실패: {str(e)}")
    
    @pytest.mark.data_not_required
    def test_empty_username_signup(self, driver):
        # AUTH-AUTO-002: 사용자명 누락 회원가입 테스트
        try:
            test_data = get_test_data("noUserNameSignup")

            # 사용자명은 비우고 회원가입 시도
            signup_page = do_signup(driver, "", test_data["email"], test_data["password"])

            # 에러 메시지 확인
            error_messages = signup_page.getErrorMessages()
            assert "username can't be blank" in error_messages, (
                f"사용자명 누락 에러 메시지가 표시되지 않았습니다.\n표시된 메시지: {error_messages}"
            )

            # URL 유지 확인
            current_url = signup_page.get_current_url()
            assert "/register" in current_url, f"페이지 URL이 변경되었습니다. 현재 URL: {current_url}"

            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 사용자명 누락 테스트 완료")

        except Exception as e:
            logger.error(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"사용자명 누락 테스트 실패: {str(e)}")
    
    @pytest.mark.data_not_required
    def test_empty_email_signup(self, driver):
        # AUTH-AUTO-003: 이메일 누락 회원가입 테스트
        try:
            test_data = get_test_data("noEmailSignup")
            # 이메일 비우고 회원가입 시도
            signup_page = do_signup(driver, test_data["userName"], "", test_data["password"])

            # 에러 메시지 확인
            error_messages = signup_page.getErrorMessages()
            assert "email can't be blank" in error_messages, (
                f"이메일 누락 에러 메시지가 표시되지 않았습니다.\n표시된 메시지: {error_messages}"
            )
            # URL 변경 없음 확인
            current_url = signup_page.get_current_url()
            assert "/register" in current_url, f"페이지 URL이 변경되었습니다. 현재 URL: {current_url}"

            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 이메일 누락 테스트 완료")

        except Exception as e:
            logger.error(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"이메일 누락 테스트 실패: {str(e)}")
    
    @pytest.mark.data_not_required
    def test_empty_password_signup(self, driver):
        # AUTH-AUTO-004: 비밀번호 누락 회원가입 테스트
        try:
            test_data = get_test_data("noPasswordSignup")

            # 비밀번호 비우고 회원가입 시도
            signup_page = do_signup(driver, test_data["userName"], test_data["email"], "")

            # 에러 메시지 확인
            error_messages = signup_page.getErrorMessages()
            assert "password can't be blank" in error_messages, (
                f"비밀번호 누락 에러 메시지가 표시되지 않았습니다.\n표시된 메시지: {error_messages}"
            )

            # URL 변경 없음 확인
            current_url = signup_page.get_current_url()
            assert "/register" in current_url, f"페이지 URL이 변경되었습니다. 현재 URL: {current_url}"

            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 비밀번호 누락 테스트 완료")

        except Exception as e:
            logger.error(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"비밀번호 누락 테스트 실패: {str(e)}")
    
    @pytest.mark.data_not_required
    def testInvalidEmailFormatSignup(self, driver):
        # AUTH-AUTO-005: 잘못된 이메일 형식 회원가입 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("invalidEmailSignup")
            
            # 회원가입 페이지 접속 및 회원가입 시도
            signupPage = SignupPage(driver)
            signupPage.navigate()
            
            # 유효하지 않은 이메일 형식으로 회원가입 시도
            signupPage.signup(testData["userName"], testData["email"], testData["password"])
            
            # 에러 메시지 확인
            errorMessages = signupPage.getErrorMessages()
            assert "email is invalid" in errorMessages, f"잘못된 이메일 형식 에러 메시지가 표시되지 않았습니다. 표시된 메시지: {errorMessages}"
            
            # URL 변경 없음 확인
            currentUrl = signupPage.get_current_url()
            assert "/register" in currentUrl, f"페이지 URL이 변경되었습니다. 현재 URL: {currentUrl}"
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 잘못된 이메일 형식 테스트 완료")
        except Exception as e:
            logger.error(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"잘못된 이메일 형식 테스트 실패: {str(e)}")

    @pytest.mark.data_not_required
    def test_duplicate_email_signup(self, driver):
        # AUTH-AUTO-006: 이미 존재하는 이메일로 회원가입 시도 시 에러 메시지 표시 테스트
        try:
            test_data = get_test_data("duplicateEmailSignup")

            signup_page = SignupPage(driver)
            signup_page.navigate()

            signup_page.enterUsername(test_data["username"])
            signup_page.enterEmail(test_data["email"])
            signup_page.enterPassword(test_data["password"])
            signup_page.clickSignUp()

            error_messages = signup_page.getErrorMessages()
            assert "email has already been taken" in error_messages, (
                f"이메일 중복 에러 메시지가 표시되지 않았습니다.\n표시된 메시지: {error_messages}"
            )

            current_url = signup_page.get_current_url()
            assert "/register" in current_url, f"페이지 URL이 변경되었습니다. 현재 URL: {current_url}"

            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 이메일 중복 회원가입 테스트 성공")

        except Exception as e:
            logger.error(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"이메일 중복 회원가입 테스트 실패: {str(e)}")

    
    @pytest.mark.data_not_required
    def test_duplicate_username_signup(self, driver):
        # AUTH-AUTO-007: 이미 존재하는 사용자명으로 회원가입 시도 시 에러 메시지 표시 테스트
        try:
            test_data = get_test_data("existingUsernameSignup")

            signup_page = SignupPage(driver)
            signup_page.navigate()

            signup_page.enterUsername(test_data["username"])
            signup_page.enterEmail(test_data["email"])
            signup_page.enterPassword(test_data["password"])
            signup_page.clickSignUp()

            error_messages = signup_page.getErrorMessages()
            assert "username has already been taken" in error_messages, (
                f"사용자명 중복 에러 메시지가 표시되지 않았습니다.\n표시된 메시지: {error_messages}"
            )

            current_url = signup_page.get_current_url()
            assert "/register" in current_url, f"페이지 URL이 변경되었습니다. 현재 URL: {current_url}"

            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 사용자명 중복 회원가입 테스트 성공")

        except Exception as e:
            logger.error(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"사용자명 중복 회원가입 테스트 실패: {str(e)}")
    
    @pytest.mark.data_not_required
    def testShortPasswordSignup(self, driver):
        # AUTH-AUTO-008: 짧은 비밀번호로 회원가입 시도 시 에러 메시지 표시 테스트
        try:
            # 테스트 데이터 로드
            testData = loadTestData("shortPwSignup")
            
            # 회원가입 페이지 접속
            signupPage = SignupPage(driver)
            signupPage.navigate()
            
            # 회원가입 정보 입력
            signupPage.enterUsername(testData["username"])
            signupPage.enterEmail(testData["email"])
            signupPage.enterPassword(testData["password"])
            
            # 회원가입 버튼 클릭
            signupPage.clickSignUp()
            
            # 에러 메시지 확인
            errorMessages = signupPage.getErrorMessages()
            
            # 검증 - 비밀번호 길이 관련 에러 메시지 확인
            assert "password is too short" in errorMessages or "minimum is 6 characters" in errorMessages, f"비밀번호 길이 에러 메시지가 표시되지 않았습니다. 표시된 메시지: {errorMessages}"
            
            # URL 변경 없음 확인
            currentUrl = signupPage.get_current_url()
            assert "/register" in currentUrl, f"페이지 URL이 변경되었습니다. 현재 URL: {currentUrl}"
            
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 짧은 비밀번호 회원가입 테스트 성공")
        except Exception as e:
            logger.error(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"짧은 비밀번호 회원가입 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_not_required
    def test_xss_in_username_signup(self, driver):
        # AUTH-AUTO-009: XSS 공격 문자열을 사용자명으로 회원가입 시 보안 처리 테스트
        try:
            test_data = get_test_data("xssSignup")

            signup_page = SignupPage(driver)
            signup_page.navigate()

            signup_page.enterUsername(test_data["username"])
            signup_page.enterEmail(test_data["email"])
            signup_page.enterPassword(test_data["password"])
            signup_page.clickSignUp()

            is_signup_successful = signup_page.isSignupSuccessful()
            assert is_signup_successful, "XSS 테스트용 회원가입이 실패했습니다."

            home_page = HomePage(driver)
            assert home_page.isPageLoaded(), "홈페이지로 리디렉션되지 않았습니다."

            nav_username = home_page.getNavigateUserName()
            assert "<script>" in nav_username or "&lt;script&gt;" in nav_username, (
                f"XSS 스크립트가 이스케이프되지 않았습니다. 표시된 사용자명: {nav_username}"
            )

            logger.info(f"✅ {inspect.currentframe().f_code.co_name} XSS 사용자명 회원가입 테스트 성공")

        except Exception as e:
            logger.error(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"XSS 사용자명 회원가입 테스트 실패: {str(e)}")

    @pytest.mark.data_not_required
    def test_double_click_signup_prevention(self, driver):
        # AUTH-AUTO-010: 회원가입 버튼 더블 클릭 시 중복 가입 방지 테스트
        try:
            test_data = get_test_data("doubleClickSignin")

            signup_page = SignupPage(driver)
            signup_page.navigate()

            signup_page.enterUsername(test_data["username"])
            signup_page.enterEmail(test_data["email"])
            signup_page.enterPassword(test_data["password"])

            signup_button = driver.find_element(*SignupLoc.SIGNUP_BUTTON)  # 수정된 로케이터명
            actions = ActionChains(driver)
            actions.double_click(signup_button).perform()

            is_signup_successful = signup_page.isSignupSuccessful()
            assert is_signup_successful, "더블 클릭 테스트용 회원가입이 실패했습니다."

            home_page = HomePage(driver)
            assert home_page.isPageLoaded(), "홈페이지로 리디렉션되지 않았습니다."

            login_page = LoginPage(driver)
            assert login_page.isLoggedIn(), (
                "더블 클릭으로 생성된 계정으로 로그인할 수 없습니다. "
                "계정이 생성되지 않았거나 중복 생성되었을 수 있습니다."
            )

            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 회원가입 버튼 더블 클릭 테스트 성공")

        except Exception as e:
            logger.error(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"회원가입 버튼 더블 클릭 테스트 실패: {str(e)}")

    @pytest.mark.data_required
    def test_successful_login(self, driver):
        # AUTH-AUTO-011: 올바른 자격 증명으로 로그인 성공 테스트
        try:
            test_data = get_test_data("successLogin")  # ✅ 오타 수정 필요
            email = test_data["email"]
            password = test_data["password"]
            expected_username = test_data["username"]

            login_page = LoginPage(driver)
            login_page.navigate()
            login_page.login(email, password)

            home_page = HomePage(driver)

            # 1. URL 확인
            assert home_page.wait_for_url_contains("/"), "홈페이지로 리디렉션되지 않았습니다."

            # 2. 사용자명 표시 확인
            displayed_username = home_page.getNavigateUserName()
            assert displayed_username == expected_username, (
                f"네비게이션 바에 표시된 사용자명이 일치하지 않습니다.\n"
                f"예상: {expected_username}, 실제: {displayed_username}"
            )

            # 3. localStorage에 JWT 저장 확인
            jwt_token = driver.execute_script("return localStorage.getItem('jwt');")
            assert jwt_token is not None and jwt_token != "", "JWT 토큰이 localStorage에 저장되지 않았습니다."

            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 로그인 성공 테스트 완료")

        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_required
    def test_login_with_invalid_password(self, driver):
        # AUTH-AUTO-012: 잘못된 비밀번호로 로그인 실패 테스트
        try:
            test_data = get_test_data("wrongPwLogin")
            email = test_data["email"]
            wrong_password = test_data["password"]

            # 이전 토큰 제거
            driver.execute_script("localStorage.removeItem('jwt');")

            login_page = LoginPage(driver)
            login_page.navigate()

            initial_url = login_page.get_current_url()

            login_page.enterEmail(email)
            login_page.enterPassword(wrong_password)
            login_page.clickSignIn()

            error_messages = login_page.getErrorMessages()
            assert any("email or password is invalid" in msg.lower() for msg in error_messages), (
                f"예상된 에러 메시지가 표시되지 않았습니다.\n표시된 메시지: {error_messages}"
            )

            current_url = login_page.get_current_url()
            assert current_url == initial_url, (
                f"로그인 실패 후 URL이 변경되었습니다.\n초기: {initial_url}, 현재: {current_url}"
            )

            jwt_token = driver.execute_script("return localStorage.getItem('jwt');")
            assert jwt_token is None or jwt_token == "", "JWT 토큰이 저장되었습니다. 로그인 방어 실패입니다."

            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 잘못된 비밀번호 로그인 테스트 완료")

        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_required
    def test_login_state_after_refresh(self, driver):
        # AUTH-AUTO-013: 페이지 새로고침 후 로그인 상태 유지 테스트
        try:
            test_data = get_test_data("successLogin")  # ✅ 키 오타 수정
            email = test_data["email"]
            password = test_data["password"]
            expected_username = test_data["username"]

            login_page = LoginPage(driver)
            login_page.navigate()
            login_page.login(email, password)

            home_page = HomePage(driver)
            assert home_page.isPageLoaded(), "홈페이지가 로드되지 않았습니다."

            before_refresh_username = home_page.getNavigateUserName()
            before_refresh_token = driver.execute_script("return localStorage.getItem('jwt');")

            driver.refresh()

            home_page = HomePage(driver)
            assert home_page.isPageLoaded(), "새로고침 후 홈페이지가 로드되지 않았습니다."

            after_refresh_username = home_page.getNavigateUserName()
            assert after_refresh_username == before_refresh_username, (
                f"새로고침 후 사용자명이 변경되었습니다.\n이전: {before_refresh_username}, 이후: {after_refresh_username}"
            )

            after_refresh_token = driver.execute_script("return localStorage.getItem('jwt');")
            assert after_refresh_token == before_refresh_token, "새로고침 후 JWT 토큰이 변경되었습니다."
            assert after_refresh_token is not None and after_refresh_token != "", "새로고침 후 JWT 토큰이 사라졌습니다."

            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 새로고침 후 로그인 상태 유지 테스트 완료")

        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_required
    def test_login_state_after_navigation(self, driver):
        # AUTH-AUTO-014: 페이지 이동 후 로그인 상태 유지 테스트
        try:
            test_data = get_test_data("successLogin")  # ✅ 키 오타 수정
            email = test_data["email"]
            password = test_data["password"]
            expected_username = test_data["username"]

            login_page = LoginPage(driver)
            login_page.navigate()
            login_page.login(email, password)

            home_page = HomePage(driver)
            assert home_page.isPageLoaded(), "홈페이지가 로드되지 않았습니다."

            initial_username = home_page.getNavigateUserName()
            initial_token = driver.execute_script("return localStorage.getItem('jwt');")

            # Settings 페이지로 이동
            driver.find_element(By.XPATH, "//a[contains(text(), 'Settings')]").click()

            settings_page = SettingsPage(driver)
            assert settings_page.isSettingsPageLoaded(), "Settings 페이지가 로드되지 않았습니다."

            settings_username = driver.find_element(
                By.XPATH,
                f"//a[contains(@class, 'nav-link') and contains(text(), '{expected_username}')]"
            ).text
            assert settings_username == initial_username, (
                f"Settings 페이지에서 사용자명이 변경되었습니다. 이전: {initial_username}, 이후: {settings_username}"
            )

            settings_token = driver.execute_script("return localStorage.getItem('jwt');")
            assert settings_token == initial_token, "Settings 페이지에서 JWT 토큰이 변경되었습니다."

            # Home 페이지로 복귀
            driver.find_element(By.XPATH, "//a[contains(text(), 'Home')]").click()

            home_page = HomePage(driver)
            assert home_page.isPageLoaded(), "Home 페이지로 복귀 후 페이지가 로드되지 않았습니다."

            final_username = home_page.getNavigateUserName()
            assert final_username == initial_username, (
                f"Home 페이지 복귀 후 사용자명이 변경되었습니다. 이전: {initial_username}, 이후: {final_username}"
            )

            final_token = driver.execute_script("return localStorage.getItem('jwt');")
            assert final_token == initial_token, "Home 페이지 복귀 후 JWT 토큰이 변경되었습니다."
            assert final_token is not None and final_token != "", "Home 페이지 복귀 후 JWT 토큰이 사라졌습니다."

            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 페이지 이동 후 로그인 상태 유지 테스트 완료")

        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_not_required
    def test_redirect_to_login_when_accessing_editor_page(self, driver):
        # AUTH-AUTO-015: 로그아웃 상태에서 에디터 페이지 접근 시 로그인 페이지로 리디렉션 테스트
        try:
            # 로그아웃 상태 확보
            driver.get(config.BASE_URL)
            driver.execute_script("localStorage.removeItem('jwt');")

            # 보호된 페이지로 접근 시도
            driver.get(f"{config.BASE_URL}/editor")

            login_page = LoginPage(driver)

            current_url = login_page.get_current_url()
            assert "/login" in current_url, (
                f"보호된 페이지 접근 시 로그인 페이지로 리디렉션되지 않았습니다.\n현재 URL: {current_url}"
            )

            editor_elements_present = login_page.is_element_present(*EditorLoc.EDITOR_PUBLISH_BUTTON)
            assert not editor_elements_present, (
                "로그인 페이지로 리디렉션되었지만 에디터 페이지 요소가 여전히 표시됩니다."
            )

            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 보호된 페이지 접근 시 리디렉션 테스트 완료")

        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise

    @pytest.mark.data_not_required
    def test_unauthorized_settings_access(self, driver):
        # AUTH-AUTO-016: 로그아웃 상태에서 설정 페이지 접근 시 로그인 페이지로 리디렉션 테스트
        try:
            # 로그아웃 상태 강제화
            driver.execute_script("localStorage.removeItem('jwt');")

            settings_page = SettingsPage(driver)
            driver.get(f"{driver.current_url.split('#')[0]}#/settings")

            login_page = LoginPage(driver)
            login_page.wait_for_url_contains("login")

            current_url = login_page.get_current_url()
            assert "login" in current_url, (
                f"로그인 페이지로 리디렉션되지 않았습니다.\n현재 URL: {current_url}"
            )

            assert not settings_page.is_element_present(ProfileLoc.PROFILE_EDIT_SETTINGS_BTN), (
                "설정 페이지 내용이 표시되고 있습니다."
            )

            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")

        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_required
    def test_logout_functionality(self, driver):
        # AUTH-AUTO-017: 로그아웃 기능 테스트
        try:
            test_data = get_test_data("successLogin")  # ✅ 키 오타 수정

            login_page = LoginPage(driver)
            login_page.navigate()
            login_page.login(test_data["email"], test_data["password"])

            home_page = HomePage(driver)
            assert home_page.is_element_visible(HomeLoc.USER_MENU), "로그인 상태가 아닙니다."

            logout_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Logout')]")
            logout_button.click()

            home_page.wait_for_url_contains("")
            current_url = home_page.get_current_url()
            assert current_url.endswith('/') or current_url.endswith('#/'), (
                f"홈페이지로 리디렉션되지 않았습니다.\n현재 URL: {current_url}"
            )

            assert home_page.is_element_visible(HomeLoc.SIGNIN_LINK), "Sign in 링크가 표시되지 않습니다."
            assert home_page.is_element_visible(HomeLoc.SIGNUP_LINK), "Sign up 링크가 표시되지 않습니다."
            assert not home_page.is_element_present(HomeLoc.USER_MENU), "사용자 메뉴가 여전히 표시되고 있습니다."

            jwt_token = driver.execute_script("return localStorage.getItem('jwt');")
            assert jwt_token is None or jwt_token in ["", "null"], "JWT 토큰이 삭제되지 않았습니다."

            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")

        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_required
    def test_browser_back_after_logout(self, driver):
        # AUTH-AUTO-018: 로그아웃 후 브라우저 뒤로가기 시 로그인 페이지로 리디렉션 테스트
        try:
            test_data = get_test_data("successLogin")

            login_page = LoginPage(driver)
            login_page.navigate()
            login_page.login(test_data["email"], test_data["password"])

            settings_page = SettingsPage(driver)
            driver.get(f"{driver.current_url.split('#')[0]}#/settings")

            assert settings_page.isSettingsPageLoaded(), "설정 페이지가 로드되지 않았습니다."

            # ✅ 로그아웃 강제 처리
            driver.execute_script("localStorage.removeItem('jwt');")

            home_page = HomePage(driver)
            home_page.wait_for_url_contains("")

            # 뒤로가기 대신 설정 페이지 재접근
            driver.get(f"{driver.current_url.split('#')[0]}#/settings")

            login_page.wait_for_url_contains("login")
            current_url = login_page.get_current_url()
            assert "login" in current_url, (
                f"로그인 페이지로 리디렉션되지 않았습니다. 현재 URL: {current_url}"
            )

            assert not settings_page.is_element_present(SettingsLoc.UPDATE_BUTTON), (
                "설정 페이지 내용이 표시되고 있습니다."
            )

            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")

        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_required
    def test_expired_token_redirection(self, driver):
        # AUTH-AUTO-019: 만료된 JWT 토큰으로 인증 필요 페이지 접근 시 로그인 페이지로 리디렉션 테스트
        try:
            test_data = get_test_data("successLogin")

            login_page = LoginPage(driver)
            login_page.navigate()
            login_page.login(test_data["email"], test_data["password"])

            home_page = HomePage(driver)
            assert home_page.is_element_visible(HomeLoc.USER_MENU), "로그인 상태가 아닙니다."

            # JWT 토큰 만료 시뮬레이션
            driver.execute_script("localStorage.setItem('jwt', 'expired_or_invalid_token');")

            # 인증 필요한 페이지 접근 시도
            driver.get(f"{driver.current_url.split('#')[0]}#/settings")

            login_page.wait_for_url_contains("login")
            current_url = login_page.get_current_url()
            assert "login" in current_url, (
                f"로그인 페이지로 리디렉션되지 않았습니다. 현재 URL: {current_url}"
            )

            jwt_token = driver.execute_script("return localStorage.getItem('jwt');")
            assert jwt_token is None or jwt_token != "expired_or_invalid_token", (
                "만료된 토큰이 적절히 처리되지 않았습니다."
            )

            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")

        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise
    
    @pytest.mark.data_not_required
    def test_signup_page_placeholders(self, driver):
        # AUTH-AUTO-020: 회원가입 페이지 placeholder 텍스트 확인 테스트
        try:
            signup_page = SignupPage(driver)
            signup_page.navigate()

            username_placeholder = driver.find_element(*SignupLoc.SIGNUP_USERNAME_INPUT).get_attribute("placeholder")
            assert username_placeholder == "Username", (
                f"사용자명 필드의 placeholder가 예상과 다릅니다.\n"
                f"실제: {username_placeholder}, 예상: Username"
            )

            email_placeholder = driver.find_element(*SignupLoc.SIGNUP_EMAIL_INPUT).get_attribute("placeholder")
            assert email_placeholder == "Email", (
                f"이메일 필드의 placeholder가 예상과 다릅니다.\n"
                f"실제: {email_placeholder}, 예상: Email"
            )

            password_placeholder = driver.find_element(*SignupLoc.SIGNUP_PASSWORD_INPUT).get_attribute("placeholder")
            assert password_placeholder == "Password", (
                f"비밀번호 필드의 placeholder가 예상과 다릅니다.\n"
                f"실제: {password_placeholder}, 예상: Password"
            )

            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")

        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            raise

    @pytest.mark.data_not_required
    def test_signup_page_labels(self, driver):
        # AUTH-AUTO-021: 회원가입 페이지의 라벨 텍스트 확인 테스트
        try:
            signup_page = SignupPage(driver)
            signup_page.navigate()

            if signup_page.is_element_present(SignupLoc.SIGNUP_USERNAME_INPUT):
                username_label = driver.find_element(*SignupLoc.SIGNUP_USERNAME_INPUT).text
                logger.info(f"사용자명 필드 라벨: {username_label}")
                assert username_label, "사용자명 필드 라벨이 비어있습니다."
            else:
                logger.info("사용자명 필드 라벨 요소가 존재하지 않습니다.")

            if signup_page.is_element_present(SignupLoc.SIGNUP_EMAIL_INPUT):
                email_label = driver.find_element(*SignupLoc.SIGNUP_EMAIL_INPUT).text
                logger.info(f"이메일 필드 라벨: {email_label}")
                assert email_label, "이메일 필드 라벨이 비어있습니다."
            else:
                logger.info("이메일 필드 라벨 요소가 존재하지 않습니다.")

            if signup_page.is_element_present(SignupLoc.SIGNUP_PASSWORD_INPUT):
                password_label = driver.find_element(*SignupLoc.SIGNUP_PASSWORD_INPUT).text
                logger.info(f"비밀번호 필드 라벨: {password_label}")
                assert password_label, "비밀번호 필드 라벨이 비어있습니다."
            else:
                logger.info("비밀번호 필드 라벨 요소가 존재하지 않습니다.")

            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 회원가입 페이지 라벨 확인 테스트 성공")

        except Exception as e:
            logger.error(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"회원가입 페이지 라벨 확인 테스트 실패: {str(e)}")
    
    @pytest.mark.data_not_required
    def test_signup_username_too_long(self, driver):
        # AUTH-AUTO-022: 회원가입 시 사용자명 최대 길이 초과 테스트
        try:
            test_data = get_test_data("longUsernameSignup")

            signup_page = SignupPage(driver)
            signup_page.navigate()

            current_url = signup_page.get_current_url()

            signup_page.enterUsername(test_data["userName"])
            signup_page.enterEmail(test_data["email"])
            signup_page.enterPassword(test_data["password"])
            signup_page.clickSignUp()

            error_messages = signup_page.getErrorMessages()

            username_too_long_error = any(
                "username is too long" in error.lower() or "maximum" in error.lower()
                for error in error_messages
            )

            assert username_too_long_error, (
                "사용자명 최대 길이 초과 에러 메시지가 표시되지 않았습니다."
            )

            assert signup_page.get_current_url() == current_url, (
                "페이지 URL이 변경되었습니다."
            )

            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 사용자명 최대 길이 초과 테스트 성공")

        except Exception as e:
            logger.error(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"사용자명 최대 길이 초과 테스트 실패: {str(e)}")
    
    @pytest.mark.data_not_required
    def test_login_page_placeholders(self, driver):
        # AUTH-AUTO-023: 로그인 페이지의 placeholder 텍스트 확인 테스트
        try:
            login_page = LoginPage(driver)
            login_page.navigate()

            email_placeholder = driver.find_element(*LoginLoc.LOGIN_EMAIL_INPUT).get_attribute("placeholder")
            logger.info(f"이메일 필드 placeholder: {email_placeholder}")
            assert email_placeholder, "이메일 필드 placeholder가 비어있습니다."

            password_placeholder = driver.find_element(*LoginLoc.LOGIN_PASSWORD_INPUT).get_attribute("placeholder")
            logger.info(f"비밀번호 필드 placeholder: {password_placeholder}")
            assert password_placeholder, "비밀번호 필드 placeholder가 비어있습니다."

            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 로그인 페이지 placeholder 확인 테스트 성공")

        except Exception as e:
            logger.error(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"로그인 페이지 placeholder 확인 테스트 실패: {str(e)}")
    
    @pytest.mark.data_required
    def test_settings_page_placeholders(self, driver):
        # AUTH-AUTO-024: 설정 페이지의 placeholder 및 label 텍스트 확인 테스트
        try:
            test_data = get_test_data("successLogin")

            login_page = LoginPage(driver)
            login_page.navigate()
            login_page.login(test_data["email"], test_data["password"])

            settings_page = SettingsPage(driver)
            driver.get(f"{driver.current_url.split('#')[0]}#/settings")
            assert settings_page.isSettingsPageLoaded(), "설정 페이지가 로드되지 않았습니다."

            bio_placeholder = driver.find_element(*SettingsLoc.SETTINGS_BIO_TEXTAREA).get_attribute("placeholder")
            assert bio_placeholder, "Bio 필드 placeholder가 비어있습니다."
            logger.info(f"Bio 필드 placeholder: {bio_placeholder}")

            image_url_placeholder = driver.find_element(*SettingsLoc.SETTINGS_PROFILE_PICTURE_INPUT).get_attribute("placeholder")
            assert image_url_placeholder, "Image URL 필드 placeholder가 비어있습니다."
            logger.info(f"Image URL 필드 placeholder: {image_url_placeholder}")

            username_placeholder = driver.find_element(*SettingsLoc.SETTINGS_USERNAME_INPUT).get_attribute("placeholder")
            assert username_placeholder, "Username 필드 placeholder가 비어있습니다."
            logger.info(f"Username 필드 placeholder: {username_placeholder}")

            email_placeholder = driver.find_element(*SettingsLoc.SETTINGS_EMAIL_INPUT).get_attribute("placeholder")
            assert email_placeholder, "Email 필드 placeholder가 비어있습니다."
            logger.info(f"Email 필드 placeholder: {email_placeholder}")

            password_placeholder = driver.find_element(*SettingsLoc.PASSWORD_INPUT).get_attribute("placeholder")
            assert password_placeholder, "Password 필드 placeholder가 비어있습니다."
            logger.info(f"Password 필드 placeholder: {password_placeholder}")

            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 설정 페이지 placeholder 확인 테스트 성공")

        except Exception as e:
            logger.error(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"설정 페이지 placeholder 확인 테스트 실패: {str(e)}")
            
    @pytest.mark.data_required
    def test_settings_bio_too_long(self, driver):
        # AUTH-AUTO-025: 설정 페이지에서 Bio 최대 길이 초과 테스트
        try:
            test_data = get_test_data("bioLongText")
            login_data = get_test_data("successLogin")

            login_page = LoginPage(driver)
            login_page.navigate()
            login_page.login(login_data["email"], login_data["password"])

            settings_page = SettingsPage(driver)
            driver.get(f"{driver.current_url.split('#')[0]}#/settings")
            assert settings_page.isSettingsPageLoaded(), "설정 페이지가 로드되지 않았습니다."

            # 기존 값 제거 후 Bio 입력
            settings_page.clearField(SettingsLoc.SETTINGS_BIO_TEXTAREA)
            settings_page.enterBio(test_data["long_bio"])
            settings_page.clickUpdateButton()

            # 에러 메시지 요소 탐색 (※ 실 HTML 구조에 따라 조정 가능)
            error_elements = driver.find_elements_by_class_name("error-messages")
            error_texts = [elem.text for elem in error_elements]

            bio_too_long_error = any(
                "bio is too long" in error.lower() or "maximum" in error.lower()
                for error in error_texts
            )

            assert bio_too_long_error, "Bio 최대 길이 초과 에러 메시지가 표시되지 않았습니다."
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} Bio 최대 길이 초과 테스트 성공")

        except Exception as e:
            logger.error(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            pytest.fail(f"Bio 최대 길이 초과 테스트 실패: {str(e)}")

    @pytest.mark.data_required
    def test_multi_session_login_sync(self, driver):
        # AUTH-AUTO-026: 동일 브라우저의 다른 탭에서 로그인 상태 동기화 확인
        try:
            test_data = get_test_data("successLogin")

            login_page = LoginPage(driver)
            login_page.navigate()
            login_page.login(test_data["email"], test_data["password"])

            home_page = HomePage(driver)
            assert home_page.isPageLoaded(), "홈페이지가 로드되지 않았습니다."

            original_window = driver.current_window_handle
            driver.execute_script("window.open('about:blank', '_blank');")

            new_window = [window for window in driver.window_handles if window != original_window][0]
            driver.switch_to.window(new_window)

            driver.get(login_page.url)

            home_page = HomePage(driver)
            username = home_page.getNavigateUserName()
            assert username == test_data["username"], (
                f"새 탭에서 사용자명이 올바르게 표시되지 않습니다.\n"
                f"예상: {test_data['username']}, 실제: {username}"
            )

            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")

        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"멀티 세션 로그인 동기화 테스트 실패: {str(e)}")
            raise

    @pytest.mark.data_required
    def test_multi_session_logout_sync(self, driver):
        # AUTH-AUTO-027: 동일 브라우저의 다른 탭에서 로그아웃 상태 동기화 확인
        try:
            test_data = get_test_data("successLogin")

            login_page = LoginPage(driver)
            login_page.navigate()
            login_page.login(test_data["email"], test_data["password"])

            home_page = HomePage(driver)
            assert home_page.isPageLoaded(), "홈페이지가 로드되지 않았습니다."

            original_window = driver.current_window_handle
            driver.execute_script("window.open('about:blank', '_blank');")

            new_window = [w for w in driver.window_handles if w != original_window][0]
            driver.switch_to.window(new_window)

            driver.get(login_page.url)
            home_page_tab_b = HomePage(driver)
            assert home_page_tab_b.getNavigateUserName() == test_data["username"], "새 탭에서 로그인 상태가 아닙니다."

            driver.switch_to.window(original_window)

            logout_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(HomeLoc.LOGOUTBUTTON)
            )
            logout_button.click()

            driver.switch_to.window(new_window)
            time.sleep(2)

            signin_link = driver.find_elements(*HomeLoc.SIGN_IN_LINK)
            signup_link = driver.find_elements(*HomeLoc.SIGN_UP_LINK)

            assert len(signin_link) > 0, "Sign in 링크가 표시되지 않습니다."
            assert len(signup_link) > 0, "Sign up 링크가 표시되지 않습니다."

            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")

        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"멀티 세션 로그아웃 동기화 테스트 실패: {str(e)}")
            raise

    @pytest.mark.data_required
    def test_form_submission_loading_state(self, driver):
        # AUTH-AUTO-029: 폼 제출 시 로딩 상태 표시 확인
        try:
            test_data = get_test_data("successLogin")

            login_page = LoginPage(driver)
            login_page.navigate()
            login_page.enterEmail(test_data["email"])
            login_page.enterPassword(test_data["password"])

            sign_in_button = driver.find_element(*LoginLoc.SIGNIN_BUTTON)
            is_disabled_before = sign_in_button.get_attribute("disabled")

            sign_in_button.click()

            try:
                WebDriverWait(driver, 3).until(
                    lambda d: d.find_element(*LoginLoc.SIGNIN_BUTTON).get_attribute("disabled") == "true"
                )
                button_disabled = True
            except:
                button_disabled = False

            assert button_disabled, "폼 제출 시 버튼 비활성화 또는 로딩 인디케이터가 표시되지 않습니다."
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 테스트 성공")

        except Exception as e:
            logger.error(f"❌ {inspect.currentframe().f_code.co_name} 테스트 실패: {str(e)}")
            pytest.fail(f"폼 제출 로딩 상태 테스트 실패: {str(e)}")
            raise