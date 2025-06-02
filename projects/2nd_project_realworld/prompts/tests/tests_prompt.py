TESTS_PROMPT = """
다음 조건에 맞춰 Python + Selenium 기반의 Pytest 테스트 코드를 작성해주세요.
테스트 코드의 개수는 반드시 JSON 형식의 테스트케이스와 동일해야 합니다.
테스트 내용은 무조건 JSON 형식의 테스트 케이스 내용과 일치해야 합니다.
테스트는 모두 독립적이며 POM 구조를 따릅니다.

✅ 저장 위치: qa-realworld-automation/tests/test_pages.py  
✅ 각 테스트에 명확한 docstring 및 간단한 한글 주석 포함  
✅ config.py, conftest.py, locator.py, base_page.py, page object는 이미 존재 (재작성 금지)  
✅ **공통코드와 로케이터는 import**해서 사용  
- 로케이터 예시: from locators.login_locators import LoginPageLocators as Loc
- 모든 요소는 Loc.XXX 형식으로 사용하고 클래스 내부에 직접 정의하지 마세요
- conftest: fixture, WAIT_SECONDS와 재시도 횟수인 RETRY_COUNT 등의 설정을 포함 
- config: 스크린샷/로그/테스트 데이터 디렉토리 생성 함수 포함 > ensureDirectoryExists(SCREENSHOT_DIR), ensureDirectoryExists(LOG_DIR), ensureDirectoryExists(TEST_DATA_DIR)
- pytest.ini: markers = smoke, regression, data_required, data_not_required
- requirements.txt: selenium, webdriver-manager, pytest-xdist, pytest-rerunfailures 등
- logger.py: setup_logger()

✅ 테스트 데이터:
- qa-realworld-automation/data/test_data.json  
- 각 테스트는 고유 데이터 사용

✅ 검증: 기본 assert 사용, 복잡한 경우 helper 함수 사용  
✅ 오류 처리: try-except 사용, 테스트 실패 시 conftest.py의 pytestRuntestMakereport() 훅 사용
✅ *사전 조건*에 *데이터 세팅* 필요 시: @pytest.mark.dataRequired  
✅ *사전 조건*에 *데이터 세팅* 필요 없을 시: @pytest.mark.dataNotRequired  
✅ 그대로 실행 가능해야 함
✅ 클래스명은 json 형식의 테스트 케이스 내용을 고려하여 작성

✅ 각 pageObject에 있는 함수 목록
- article_page: getTitle(), getAuthor(), getBody(), addComment(), getComments(), deleteCommentByIndex(), _log_error()
- editor_page: enterTitle(), enterDescription(), enterBody(), enterTags(), clickPublishButton(), writeEditor()
- home_page: getNavigateUserName(), clickYourFeedTab(), clickGlobalFeedTab(), clickTag(), getArticleTitles(), isArticleVisible(), getTagList(), isPageLoaded()
- Login_page: navigate(), enterEmail(), enterPassword(), clickSignIn(), login(), getErrorMessages(), isLoggedIn()
- profile_page: getUsername(), getUserBio(), clickFollowButton(), clickUnfollowButton(), isFollowing(), _log_error()
- settings_page: enterImageUrl(), enterUsername(), enterBio(), enterEmail(), enterPassword(), clickUpdateButton(), updateSettings(), isSettingsPageLoaded(), clearField()
- signup_page : navigate(), enterUsername(), enterEmail(), enterPassword(), clickSignUp(), signup(), getErrorMessages(), isSignupSuccessful()
- base_page: get_page_title(), get_current_url(), is_element_visible(), is_element_present(), wait_for_url_contains(), screen_diff()
✅ screen_diff()는 기대결과 확인 시 필요한 경우에만 사용

# 예시 코드:
```python
def loadTestData():
    data_file_path = os.path.join(config.TEST_DATA_DIR, "test_data.json")
    with open(data_file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

logger = setup_logger(__name__)

class TestAuth:
    @pytest.mark.data_not_required
    def testSuccessfulSignup(self, driver):
        try:
            # 테스트 데이터 로드
            testData = loadTestData()["normalSignin"]

            # 회원가입 페이지 접속 및 회원가입 진행
            signupPage = SignupPage(driver)
            signupPage.navigate()
            signupPage.signup(testData["user_name"], testData["email"], testData["password"])
            
            # 홈페이지로 리디렉션 확인
            homePage = HomePage(driver)
            
            # 1. URL 확인
            currentUrl = driver.wait_for_url_contains("home")
            assert currentUrl.endswith('/'), f"홈페이지로 리디렉션되지 않았습니다. 현재 URL: {currentUrl}"

            isChanged = signupPage.screen_diff(
                locator=Loc.SIGNIN_BUTTON,        # 클릭 대상 버튼
                funcName="test_login",           # 파일명 구분용 기능 이름
                imageName="signin_click",        # 파일명 구분용 이미지 이름
                action="click"                    # 클릭 액션
            )

            # 결과 확인
            assert isChanged is True, "로그인 버튼 클릭 후 화면 변화가 감지되지 않았습니다."
            logger.info(f"✅ {inspect.currentframe().f_code.co_name} 로그인 테스트 성공")
        except Exception as e:
            pytest.fail(f"회원가입 성공 테스트 실패: {str(e)}")
            logger.warning(f"❗ {inspect.currentframe().f_code.co_name} : {e}")
            raise
```

다음은 JSON 형식의 테스트케이스 입니다.:
"""
