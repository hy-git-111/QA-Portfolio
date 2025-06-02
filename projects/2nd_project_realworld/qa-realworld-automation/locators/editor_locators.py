from selenium.webdriver.common.by import By

class EditorPageLocators:

    # 🧭 Navigation
    EDITOR_NAVBAR_BRAND = (By.CSS_SELECTOR, "a.navbar-brand")
    EDITOR_HOME_LINK = (By.CSS_SELECTOR, "a.nav-link[href='/']")
    EDITOR_NEW_POST_LINK = (By.CSS_SELECTOR, "a.nav-link[href='/editor']")
    EDITOR_SETTINGS_LINK = (By.CSS_SELECTOR, "a.nav-link[href='/settings']")
    EDITOR_PROFILE_LINK = (By.CSS_SELECTOR, "a.nav-link[href='/@1']")  # ⚠️ 하드코딩된 값
    EDITOR_PROFILE_LINK_DYNAMIC = (By.CSS_SELECTOR, "a.nav-link[href^='/@']")  # ✅ 동적 사용자 링크 대응
    EDITOR_USER_PIC = (By.CSS_SELECTOR, "img.user-pic")

    # 📝 Editor Form
    EDITOR_TITLE_INPUT = (By.CSS_SELECTOR, "input.form-control.form-control-lg[placeholder='Article Title']")
    EDITOR_ABOUT_INPUT = (By.CSS_SELECTOR, "input.form-control[placeholder='What\'s this article about?']")
    EDITOR_CONTENT_TEXTAREA = (By.CSS_SELECTOR, "textarea.form-control")  # placeholder 일치 생략 (버전 차이 대응)
    EDITOR_TAGS_INPUT = (By.CSS_SELECTOR, "input.form-control[placeholder='Enter tags']")
    EDITOR_TAG_LIST = (By.CSS_SELECTOR, "div.tag-list")

    # 🖱️ Action Buttons
    EDITOR_PUBLISH_BUTTON = (By.CSS_SELECTOR, "button.btn.btn-lg.pull-xs-right.btn-primary")
