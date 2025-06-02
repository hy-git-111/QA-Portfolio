import os
from pathlib import Path
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 기본 URL 설정 - 테스트 환경에 따라 변경 가능
BASE_URL = "http://localhost:4100"

# 브라우저 설정
BROWSER_TYPE = "chrome"  # 기본 브라우저 타입 (chrome, firefox, edge 등)
HEADLESS = False  # 헤드리스 모드 활성화 여부

# 타임아웃 설정
TIMEOUT = 10  # 기본 타임아웃 (초)
WAIT_SECONDS = 5  # 명시적 대기 시간 (초)
RETRY_COUNT = 3  # 재시도 횟수

# 스크린샷 설정
SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots")
TAKE_SCREENSHOT_ON_FAILURE = True  # 실패 시 스크린샷 촬영 여부

# 로깅 설정
LOG_LEVEL = "INFO"  # 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")

# ✅ WebDriver 자동 설치 및 생성 함수
def get_driver(headless=False, timeout=TIMEOUT):
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    from selenium import webdriver
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(timeout)
    driver.maximize_window()
    return driver

# 테스트 환경 설정
class TestEnvironment:
    @staticmethod
    def getLocalConfig():
        return {
            "baseUrl": "http://localhost:4100",
            "timeout": 10,
            "headless": False
        }

    @staticmethod
    def getDevConfig():
        return {
            "baseUrl": "https://dev.example.com",
            "timeout": 15,
            "headless": True
        }

    @staticmethod
    def getStagingConfig():
        return {
            "baseUrl": "https://staging.example.com",
            "timeout": 20,
            "headless": True
        }

# 테스트 데이터 설정
TEST_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# 디렉토리 생성 함수
def ensureDirectoryExists(dirPath):
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)

# 필요한 디렉토리 생성
ensureDirectoryExists(SCREENSHOT_DIR)
ensureDirectoryExists(LOG_DIR)
ensureDirectoryExists(TEST_DATA_DIR)

# 🔽 외부에서 import할 수 있도록 명시
__all__ = [
    "BASE_URL",
    "BROWSER_TYPE",
    "HEADLESS",
    "TIMEOUT",
    "WAIT_SECONDS",
    "RETRY_COUNT",
    "SCREENSHOT_DIR",
    "TAKE_SCREENSHOT_ON_FAILURE",
    "LOG_LEVEL",
    "LOG_DIR",
    "get_driver",  # ✅ 변경된 함수 이름 반영
    "TestEnvironment",
    "TEST_DATA_DIR"
]
