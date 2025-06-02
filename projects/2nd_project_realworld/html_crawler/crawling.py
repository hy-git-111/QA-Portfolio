from selenium import webdriver
from selenium.webdriver.common.by import By
from html_crawler.html_base_page import BasePage
from file_manage import save_data_append
from html_crawler.user_data import USER_DATA
import time

class CrawlingPage(BasePage):
    # 로그인하는 함수
    def login(self, EMAIL: str, PASSWORD: str):
        self.click_element((By.CSS_SELECTOR, "a[href='/login']"))
        self.input_text((By.CSS_SELECTOR, "input[type='email'][placeholder='Email']"), EMAIL)
        self.input_text((By.CSS_SELECTOR, "input[type='password'][placeholder='Password']"), PASSWORD)
        self.click_element((By.CLASS_NAME, "btn-primary"))

    # 글 게시하는 함수
    def publish_article(self, title, description, article):
        self.input_text((By.CSS_SELECTOR, "input[type='text'][placeholder='Article Title']"), title)
        self.input_text((By.CSS_SELECTOR, "input[type='text'][placeholder='What's this article about?']"), description)
        self.input_text((By.CSS_SELECTOR, "textarea[placeholder='Write your article (in markdown)']"), article)

    # html body의 모든 태그를 반환하는 함수
    def get_html_tags(self):
        tags = self.driver.execute_script("""
            return (function getNodePath(node, depth = 0) {
                if (!node) return '';
                const indent = ' '.repeat(depth * 2);
                let result = '';

                if (node.nodeType === 1) {
                    result += indent + '<' + node.tagName.toLowerCase();
                    for (let i = 0; i < node.attributes.length; i++) {
                        const attr = node.attributes[i];
                        result += ' ' + attr.name + '="' + attr.value + '"';
                    }
                    result += '>' + '\\n';
                    for (let i = 0; i < node.childNodes.length; i++) {
                        result += getNodePath(node.childNodes[i], depth + 1);
                    }
                    result += indent + '</' + node.tagName.toLowerCase() + '>' + '\\n';
                } else if (node.nodeType === 3) {
                    const text = node.textContent.trim();
                    if (text) {
                        result += indent + '"' + text + '"' + '\\n';
                    }
                }
                return result;
            })(document.body);
        """)

        return tags

    # 로그인 이후 진입 가능한 페이지를 크롤링하여 반환하는 함수
    def capture_page(self, title, login_required, locator_1=None, locator_2=None, locator_3 = None): 
        url = "http://localhost:4100/"
        self.driver.get(url)

        if login_required == True:
            self.login(USER_DATA["email"], USER_DATA["password"])
            time.sleep(1)

        if locator_1:
            self.click_element(locator_1)
            self.wait_for_page_load()

            if locator_2:
                self.click_element(locator_2)
                self.wait_for_page_load()

                if locator_3:
                    self.publish_article("타이틀", "요약", "내용")
                    self.click_element(locator_3)
                    self.wait_for_page_load()

        html_data = f"<!-- {title} -->\n{self.get_html_tags()}"
        return html_data
    
def capture_page(title, login_required, locator_1=None, locator_2=None, locator_3=None):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    crawling = CrawlingPage(driver)

    try:
        html_data = crawling.capture_page(title, login_required, locator_1, locator_2, locator_3)
        filename = title + ".html"
        save_data_append(html_data, "html_data", filename)
    finally:
        driver.quit()