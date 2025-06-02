import os
import time
import logging
from PIL import Image, ImageChops
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

class BasePage:
    """
    모든 페이지 객체의 기본이 되는 클래스
    공통 메서드와 속성을 정의합니다.
    """
    
    def __init__(self, driver, timeout=10):
        """
        BasePage 생성자
        :param driver: Selenium WebDriver 인스턴스
        :param timeout: 요소 대기 시간(초)
        """
        self.driver = driver
        self.timeout = timeout
        # 로깅 설정
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def _find_element(self, locator):
        """
        단일 요소를 찾아 반환합니다.
        요소가 나타날 때까지 명시적으로 대기합니다.
        """
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            self.logger.error(f"요소를 찾을 수 없습니다: {locator}")
            raise
    
    def _find_elements(self, locator):
        """
        여러 요소를 찾아 리스트로 반환합니다.
        요소들이 나타날 때까지 명시적으로 대기합니다.
        """
        try:
            elements = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            return elements
        except TimeoutException:
            self.logger.error(f"요소들을 찾을 수 없습니다: {locator}")
            return []
    
    def _click(self, locator):
        """
        요소를 클릭합니다.
        요소가 클릭 가능할 때까지 명시적으로 대기합니다.
        """
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
        except (TimeoutException, ElementClickInterceptedException) as e:
            self.logger.error(f"요소를 클릭할 수 없습니다: {locator}, 오류: {str(e)}")
            raise
    
    def _send_keys(self, locator, text):
        """
        요소에 텍스트를 입력합니다.
        요소가 나타날 때까지 명시적으로 대기합니다.
        """
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
            element.clear()  # 기존 텍스트 삭제
            element.send_keys(text)
        except TimeoutException:
            self.logger.error(f"요소에 텍스트를 입력할 수 없습니다: {locator}")
            raise
    
    def _get_text(self, locator):
        """
        요소의 텍스트를 반환합니다.
        요소가 나타날 때까지 명시적으로 대기합니다.
        """
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element.text
        except TimeoutException:
            self.logger.error(f"요소의 텍스트를 가져올 수 없습니다: {locator}")
            return ""
    
    def get_page_title(self):
        """
        현재 페이지의 제목을 반환합니다.
        """
        return self.driver.title
    
    def get_current_url(self):
        """
        현재 페이지의 URL을 반환합니다.
        """
        return self.driver.current_url
    
    def is_element_visible(self, locator):
        """
        요소가 화면에 보이는지 확인합니다.
        """
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator):
        """
        요소가 DOM에 존재하는지 확인합니다.
        """
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_url_contains(self, url_part):
        """
        URL에 특정 문자열이 포함될 때까지 대기합니다.
        """
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.url_contains(url_part)
            )
            return True
        except TimeoutException:
            self.logger.error(f"URL에 '{url_part}'가 포함되지 않습니다.")
            return False

    def screen_diff(self, locator, func_name, image_name, action, msg=""):
        """
        요소의 액션 전후 스크린샷을 비교해 화면에 변화가 있었는지 반환합니다.
        
        :param locator: 대상 요소의 로케이터
        :param func_name: 기능명 또는 테스트 케이스명 (파일명 구분용)
        :param image_name: 비교 대상 이름 (파일명 구분용)
        :param action: "click" 또는 "send"
        :param msg: send_keys 시 입력할 텍스트 (기본값 "")
        :return: 화면 변화가 있으면 True, 없으면 False
        """
        screenshot_dir = "reports/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)

        before_path = os.path.join(screenshot_dir, f"{func_name}_{image_name}_before.png")
        after_path = os.path.join(screenshot_dir, f"{func_name}_{image_name}_after.png")

        time.sleep(2)
        self.driver.save_screenshot(before_path)

        if action == "click":
            self._click(locator)
        elif action == "send":
            self._send_keys(locator, msg)
        else:
            self.logger.warning(f"[스크린샷] 지원되지 않는 액션: {action}")
            return False

        time.sleep(2)
        self.driver.save_screenshot(after_path)

        try:
            before = Image.open(before_path)
            after = Image.open(after_path)
            diff = ImageChops.difference(before, after)
            has_diff = diff.getbbox() is not None
            self.logger.info(f"[스크린샷] 화면 변화 감지 결과: {'변화 있음' if has_diff else '변화 없음'}")
            return has_diff
        except Exception as e:
            self.logger.error(f"[스크린샷] 비교 실패: {e}")
            return False
