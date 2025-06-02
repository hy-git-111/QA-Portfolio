from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators.settings_locators import SettingsPageLocators as Loc
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class SettingsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def enterImageUrl(self, url):
        try:
            self._send_keys(Loc.SETTINGS_PROFILE_PICTURE_INPUT, url)
            return True
        except Exception as e:
            print(f"이미지 URL 입력 중 오류 발생: {str(e)}")
            return False

    def enterUsername(self, username):
        try:
            self._send_keys(Loc.SETTINGS_USERNAME_INPUT, username)
            return True
        except Exception as e:
            print(f"사용자 이름 입력 중 오류 발생: {str(e)}")
            return False

    def enterBio(self, bio):
        try:
            self._send_keys(Loc.SETTINGS_BIO_TEXTAREA, bio)
            return True
        except Exception as e:
            print(f"자기소개 입력 중 오류 발생: {str(e)}")
            return False

    def enterEmail(self, email):
        try:
            self._send_keys(Loc.SETTINGS_EMAIL_INPUT, email)
            return True
        except Exception as e:
            print(f"이메일 입력 중 오류 발생: {str(e)}")
            return False

    def enterPassword(self, password):
        try:
            self._send_keys(Loc.SETTINGS_PASSWORD_INPUT, password)
            return True
        except Exception as e:
            print(f"비밀번호 입력 중 오류 발생: {str(e)}")
            return False

    def clickUpdateButton(self):
        try:
            self._click(Loc.SETTINGS_UPDATE_BUTTON)
            WebDriverWait(self.driver, 10).until(
                EC.url_changes(self.driver.current_url)
            )
            return True
        except Exception as e:
            print(f"업데이트 버튼 클릭 중 오류 발생: {str(e)}")
            return False

    def updateSettings(self, image="", username="", bio="", email="", password=""):
        try:
            if image:
                self.enterImageUrl(image)
            if username:
                self.enterUsername(username)
            if bio:
                self.enterBio(bio)
            if email:
                self.enterEmail(email)
            if password:
                self.enterPassword(password)

            self.clickUpdateButton()
            return True
        except Exception as e:
            print(f"설정 업데이트 중 오류 발생: {str(e)}")
            return False

    def isSettingsPageLoaded(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(Loc.SETTINGS_UPDATE_BUTTON)
            )
            return True
        except Exception as e:
            print(f"설정 페이지 로드 확인 중 오류 발생: {str(e)}")
            return False

    def clearField(self, locator):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(locator)
            )
            element.clear()
            return True
        except Exception as e:
            print(f"필드 내용 지우기 중 오류 발생: {str(e)}")
            return False

    def clickLogoButton(self):
        try:
            self._click(Loc.SETTINGS_NAVBAR_BRAND)
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(Loc.SETTINGS_NAVBAR_BRAND)
            )
            return True
        except (TimeoutException, NoSuchElementException) as e:
            self._log_error(f"Follow 버튼 클릭에 실패했습니다: {str(e)}")
            return False