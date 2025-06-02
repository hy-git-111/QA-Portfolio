from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators.login_locators import LoginPageLocators as Loc

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # 기본 URL은 로그인 페이지
        self.url = "http://localhost:4100/login"
    
    def navigate(self):
        # 로그인 페이지로 이동
        self.driver.get(self.url)
        return self
    
    def enterEmail(self, email):
        # 이메일 입력 필드에 이메일 입력
        try:
            self._send_keys(Loc.LOGIN_EMAIL_INPUT, email)
            return self
        except Exception as e:
            self.logger.error(f"이메일 입력 중 오류 발생: {str(e)}")
            raise
    
    def enterPassword(self, password):
        # 비밀번호 입력 필드에 비밀번호 입력
        try:
            self._send_keys(Loc.LOGIN_PASSWORD_INPUT, password)
            return self
        except Exception as e:
            self.logger.error(f"비밀번호 입력 중 오류 발생: {str(e)}")
            raise
    
    def clickSignIn(self):
        # 로그인 버튼 클릭
        try:
            self._click(Loc.LOGIN_SIGN_IN_BUTTON)
            return self
        except Exception as e:
            self.logger.error(f"로그인 버튼 클릭 중 오류 발생: {str(e)}")
            raise
    
    def login(self, email, password):
        # 로그인 전체 프로세스를 하나로 묶은 메서드
        try:
            self.enterEmail(email)
            self.enterPassword(password)
            self.clickSignIn()
            return self
        except Exception as e:
            self.logger.error(f"로그인 프로세스 중 오류 발생: {str(e)}")
            raise
    
    def getErrorMessages(self):
        # 로그인 실패 시 오류 메시지 리스트 반환
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(Loc.LOGIN_ERROR_MESSAGES)
            )
            elements = self._find_elements(Loc.LOGIN_ERROR_MESSAGES)
            return [e.text for e in elements]
        except Exception as e:
            self.logger.warning(f"오류 메시지 가져오기 실패: {str(e)}")
            return []
    
    def isLoggedIn(self):
        # 로그인 성공 여부 확인 (헤더에 사용자 아이콘이 표시되는지 확인)
        try:
            return self._is_element_visible(Loc.LOGIN_USER_PROFILE_ICON, timeout=5)
        except:
            return False
