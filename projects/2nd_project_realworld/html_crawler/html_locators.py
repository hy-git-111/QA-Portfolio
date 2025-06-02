from selenium.webdriver.common.by import By

CRAWLING_LOCATORS = [
    ("login", False, (By.CSS_SELECTOR, "a[href='/login']")),    # Home > Login
    ("signup", False, (By.CSS_SELECTOR, "a[href='/login']"), (By.CSS_SELECTOR, "a.nav-link[href='/register']")),    # Home > Login > Sign up

    ("home", True, None), # Home > Login > YourFeed
    ("home", True, (By.XPATH, "//a[normalize-space()='Global Feed']")),  # Home > Login > Global Feed
    ("editor", True, (By.CSS_SELECTOR, "a[href='/editor']")),    # Home > Login > New Post
    ("settings", True, (By.CSS_SELECTOR, "a[href='/settings']")),    # Home > Login > Settings
    ("settings", True, (By.CSS_SELECTOR, "a[href^='/@']"), (By.CLASS_NAME, "btn-outline-secondary")),  # Home > Login > MyPage > Edit Profile

    ("profile", True, (By.CSS_SELECTOR, "a[href^='/@']")),     # Home > Login > MyPage
    ("profile", True, (By.CSS_SELECTOR, "a[href^='/@']"), (By.CSS_SELECTOR, "a[href$='favorites']")),   # Home > Login > MyPage > Favorited Articles
    
    ("article", True, None, (By.CSS_SELECTOR, "a[href='/editor']"), (By.CLASS_NAME, "btn-primary")),    # Home > Login > New Post > Publish > Written Article
    ("article", True, (By.CLASS_NAME, "article-preview")),    # Home > Login > YourFeed > Article
    ("article",True, (By.CSS_SELECTOR, "a[href^='/@']"), (By.CLASS_NAME, "article-preview")),    # Home > Login > MyPage > Article
]