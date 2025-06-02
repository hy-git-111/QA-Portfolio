import sys
import os
import pytest
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ✅ 하이픈(-) 포함된 경로도 임포트 가능하게 처리
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# config.py에서 설정 가져오기
from config.config import BASE_URL, TIMEOUT, get_driver

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture(scope="session")
def driver(request):
    driver = get_driver()

    def finalize():
        driver.quit()

    request.addfinalizer(finalize)
    return driver

@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, TIMEOUT)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        try:
            driver = item.funcargs.get("driver")
            if driver:
                screenshot_dir = os.path.join(os.getcwd(), "reports", "screenshots")
                os.makedirs(screenshot_dir, exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                test_name = item.name
                screenshot_path = os.path.join(screenshot_dir, f"{test_name}_{timestamp}.png")
                driver.save_screenshot(screenshot_path)
                print(f"Screenshot saved to: {screenshot_path}")
        except Exception as e:
            print(f"Failed to take screenshot: {e}")

@pytest.fixture
def navigate_to(driver, base_url):
    def _navigate_to(path=""):
        url = f"{base_url}/{path.lstrip('/')}"
        driver.get(url)
        return driver
    return _navigate_to
