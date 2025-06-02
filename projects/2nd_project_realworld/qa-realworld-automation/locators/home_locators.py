from selenium.webdriver.common.by import By

class HomePageLocators:
    # ───── 네비게이션 바 ─────
    NAVBAR_BRAND = (By.CSS_SELECTOR, ".navbar-brand")
    NAVBAR_NAV = (By.CSS_SELECTOR, ".navbar-nav")
    NAV_HOME_LINK = (By.CSS_SELECTOR, ".nav-item:nth-child(1) .nav-link")
    NAV_NEW_POST_LINK = (By.CSS_SELECTOR, ".nav-item:nth-child(2) .nav-link")
    NAV_SETTINGS_LINK = (By.CSS_SELECTOR, ".nav-item:nth-child(3) .nav-link")
    NAV_USER_LINK = (By.CSS_SELECTOR, ".nav-item:nth-child(4) .nav-link")
    NAV_USER_PIC = (By.CSS_SELECTOR, ".user-pic")

    HOME_NAVBAR = (By.CSS_SELECTOR, "nav.navbar.navbar-light")
    HOME_NAVBAR_BRAND = (By.CSS_SELECTOR, "a.navbar-brand")
    HOME_NAV_HOME_LINK = (By.CSS_SELECTOR, "ul.nav.navbar-nav.pull-xs-right li.nav-item:nth-child(1) a.nav-link")
    HOME_NAV_NEW_POST_LINK = (By.CSS_SELECTOR, "ul.nav.navbar-nav.pull-xs-right li.nav-item:nth-child(2) a.nav-link")
    HOME_NAV_SETTINGS_LINK = (By.CSS_SELECTOR, "ul.nav.navbar-nav.pull-xs-right li.nav-item:nth-child(3) a.nav-link")
    HOME_NAV_USER_LINK = (By.CSS_SELECTOR, "ul.nav.navbar-nav.pull-xs-right li.nav-item:nth-child(4) a.nav-link")
    HOME_NAV_USER_PIC = (By.CSS_SELECTOR, "img.user-pic")
    HOME_NAV_LOGIN = (By.CSS_SELECTOR, "a.nav-link[href='/login']")

    # ───── 피드 탭 영역 ─────
    TAB_YOUR_FEED = (By.CSS_SELECTOR, ".nav-link.active")
    TAB_GLOBAL_FEED = (By.CSS_SELECTOR, ".nav-item:nth-child(2) .nav-link:not(.active)")
    HOME_FEED_TOGGLE = (By.CSS_SELECTOR, "div.feed-toggle")
    HOME_YOUR_FEED_LINK = (By.CSS_SELECTOR, "ul.nav.nav-pills.outline-active li.nav-item:nth-child(1) a.nav-link")
    HOME_GLOBAL_FEED_LINK = (By.CSS_SELECTOR, "ul.nav.nav-pills.outline-active li.nav-item:nth-child(2) a.nav-link")

    # ───── 기사 목록 / 프리뷰 ─────
    ARTICLE_PREVIEW = (By.CSS_SELECTOR, ".article-preview")
    HOME_ARTICLE_PREVIEW = (By.CSS_SELECTOR, "div.article-preview")
    HOME_ARTICLE_META = (By.CSS_SELECTOR, "div.article-meta")
    HOME_ARTICLE_AUTHOR_IMG = (By.CSS_SELECTOR, "div.article-meta a img")
    HOME_ARTICLE_AUTHOR_LINK = (By.CSS_SELECTOR, "div.article-meta div.info a.author")
    HOME_ARTICLE_DATE = (By.CSS_SELECTOR, "div.article-meta div.info span.date")
    HOME_ARTICLE_LIKE_COUNT = (By.CSS_SELECTOR, "div.article-meta div.pull-xs-right button.btn")
    HOME_ARTICLE_LIKE_HART = (By.CSS_SELECTOR, "div.article-meta div.pull-xs-right button.btn i.ion-heart")
    HOME_ARTICLE_PREVIEW_LINK = (By.CSS_SELECTOR, "a.preview-link")
    HOME_ARTICLE_TITLE = (By.CSS_SELECTOR, "a.preview-link h1")
    HOME_ARTICLE_DESCRIPTION = (By.CSS_SELECTOR, "a.preview-link p")
    HOME_ARTICLE_READ_MORE = (By.CSS_SELECTOR, "a.preview-link span")
    HOME_READ_MORE_SPAN = (By.CSS_SELECTOR, "span:contains('Read more...')")

    # ───── 태그 관련 ─────
    TAG_LIST = (By.CSS_SELECTOR, ".tag-list")
    HOME_TAG_LIST = (By.CSS_SELECTOR, "ul.tag-list")
    HOME_TAG_PILL = (By.CSS_SELECTOR, "li.tag-default.tag-pill.tag-outline")
    HOME_ARTICLE_TAG_LIST = (By.CSS_SELECTOR, "a.preview-link ul.tag-list")
    HOME_ARTICLE_TAG = (By.CSS_SELECTOR, "a.preview-link ul.tag-list li.tag-default")

    # ───── 사이드바 태그 ─────
    SIDEBAR = (By.CSS_SELECTOR, ".sidebar")
    POPULAR_TAGS_TEXT = (By.CSS_SELECTOR, ".sidebar p")
    HOME_SIDEBAR = (By.CSS_SELECTOR, "div.sidebar")
    HOME_POPULAR_TAGS_TEXT = (By.CSS_SELECTOR, "p:contains('Popular Tags')")
    HOME_POPULAR_TAGS_HEADER = (By.CSS_SELECTOR, "div.sidebar p")
    HOME_POPULAR_TAGS_LIST = (By.CSS_SELECTOR, "div.sidebar div.tag-list")
    HOME_POPULAR_TAG = (By.CSS_SELECTOR, "div.sidebar div.tag-list a.tag-default")
    HOME_POPULAR_TAG_PILL = (By.CSS_SELECTOR, "a.tag-default.tag-pill")

    # ───── 페이지 전체 레이아웃 ─────
    ROOT = (By.ID, "root")
    CONTAINER = (By.CSS_SELECTOR, ".container.page")
    HOME_PAGINATION = (By.CSS_SELECTOR, "ul.pagination")
    HOME_PAGE_ITEM = (By.CSS_SELECTOR, "li.page-item")
    HOME_PAGE_LINK = (By.CSS_SELECTOR, "a.page-link")

    # ───── 추가 항목 ─────
    HOME_ARTICLE_HEART_ICON = (By.CSS_SELECTOR, "i.ion-heart")

    # ───── XPath 기반 동적 태그 선택자 (텍스트로 특정 태그 클릭 시 사용) ─────
    HOME_POPULAR_TAG_BY_TEXT = (By.XPATH, "//div[@class='tag-list']//a[text()='{}']")
