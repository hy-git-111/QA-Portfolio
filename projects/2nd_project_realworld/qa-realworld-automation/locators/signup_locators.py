from selenium.webdriver.common.by import By

class SignupPageLocators:
    # ───── 네비게이션 바 ─────
    SIGNUP_NAVBAR_BRAND = (By.CSS_SELECTOR, "a.navbar-brand")
    SIGNUP_HOME_LINK = (By.CSS_SELECTOR, "a.nav-link[href='/']")
    SIGNUP_SIGNIN_LINK = (By.CSS_SELECTOR, "a.nav-link[href='/login']")
    SIGNUP_SIGNUP_LINK = (By.CSS_SELECTOR, "a.nav-link[href='/register']")

    # ───── 회원가입 폼 헤더 및 링크 ─────
    SIGNUP_HEADER = (By.CSS_SELECTOR, "h1.text-xs-center")
    SIGNUP_HAVE_ACCOUNT_LINK = (By.CSS_SELECTOR, "p.text-xs-center a")

    # ───── 입력 필드 ─────
    SIGNUP_USERNAME_INPUT = (By.CSS_SELECTOR, "input[type='text'][placeholder='Username']")
    SIGNUP_EMAIL_INPUT = (By.CSS_SELECTOR, "input[type='email'][placeholder='Email']")
    SIGNUP_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password'][placeholder='Password']")

    # ───── 제출 버튼 ─────
    SIGNUP_SUBMIT_BUTTON = (By.CSS_SELECTOR, "button.btn-primary[type='submit']")

    # ───── 에러 메시지 (추가됨) ─────
    SIGNUP_ERROR_MESSAGES = (By.CSS_SELECTOR, ".error-messages li")
