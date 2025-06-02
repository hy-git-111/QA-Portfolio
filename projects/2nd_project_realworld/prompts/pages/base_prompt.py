from prompts.common_pages import COMMON_PAGE_CONTEXT

BASE_PAGE_PROMPT = COMMON_PAGE_CONTEXT + """

🎯 목표:
- 모든 페이지에서 공통으로 상속받는 BasePage 클래스를 생성해주세요.
- 이 클래스는 qa-realworld-automation/pages/base_page.py에 위치합니다.

📌 구현 요구 사항:
- Selenium WebDriver를 생성자에서 받고, self.driver와 self.timeout으로 저장합니다.
- timeout 기본값은 10초입니다.
- WebDriverWait을 활용하여 요소가 나타날 때까지 기다리는 명시적 대기 기반으로 메서드를 구현해주세요.
- 다음 메서드를 포함해주세요:

  - _click(locator): 요소가 클릭 가능할 때까지 기다렸다가 클릭
  - _send_keys(locator, text): 요소가 나타날 때까지 기다렸다가 텍스트 입력
  - _get_text(locator): 요소가 나타날 때까지 기다려 텍스트 반환
  - _find_element(locator): 요소가 나타날 때까지 기다려 단일 요소 반환
  - _find_elements(locator): 요소들이 모두 나타날 때까지 기다려 리스트 반환
  - get_page_title(): 현재 페이지 제목 반환
  - get_current_url(): 현재 URL 반환

📐 작성 규칙:
- 모든 메서드는 try-except 블록으로 예외 처리를 포함해야 합니다.
- 실패 시 어떤 locator에서 실패했는지 출력하거나 기본 에러 로그를 남겨야 합니다.
- WebDriverWait은 self.timeout 값을 기반으로 동작해야 합니다.
- 각 메서드에는 한 줄 이상의 간단한 설명 주석을 작성해주세요.
- 클래스명은 PascalCase(BasePage), 함수명은 camelCase로 작성해주세요.
- 출력은 Python 코드만 작성하고, 설명은 반드시 코드 내 주석으로만 작성해주세요.
"""