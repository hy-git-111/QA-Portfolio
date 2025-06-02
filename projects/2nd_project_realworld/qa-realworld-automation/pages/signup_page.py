from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from locators.signup_locators import SignupPageLocators as Loc

class SignupPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:4100/register"
    
    def navigate(self):
        self.driver.get(self.url)
    
    def enterUsername(self, username):
        self._send_keys(Loc.SIGNUP_USERNAME_INPUT, username)
        return self
    
    def enterEmail(self, email):
        self._send_keys(Loc.SIGNUP_EMAIL_INPUT, email)
        return self
    
    def enterPassword(self, password):
        self._send_keys(Loc.SIGNUP_PASSWORD_INPUT, password)
        return self
    
    def clickSignUp(self):
        self._click(Loc.SIGNUP_SUBMIT_BUTTON)
        return self
    
    def signup(self, username, email, password):
        self.enterUsername(username)
        self.enterEmail(email)
        self.enterPassword(password)
        self.clickSignUp()
        return self
    
    def getErrorMessages(self):
        try:
            elements = self._find_elements(Loc.SIGNUP_ERROR_MESSAGES)
            return [e.text for e in elements]
        except Exception as e:
            self.logger.error(f"Failed to get error messages: {str(e)}")
            return []
    
    def isSignupSuccessful(self):
        try:
            return "/#/" in self.driver.current_url
        except Exception as e:
            self.logger.error(f"Error checking signup success: {str(e)}")
            return False
