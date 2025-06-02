from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        # self.wait = WebDriverWait(driver, 10)    

    def click_element(self, locator):
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator)).click()
        except Exception as e:
            print(e)

    def input_text(self, locator, text):
        try:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))
            element.clear()
            element.send_keys(text)    
        except Exception as e:
            print(e)
    
    def wait_for_page_load(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )