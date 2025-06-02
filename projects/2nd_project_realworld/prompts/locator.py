# ✅ locator.py 생성용 프롬프트
LOCATOR_PROMPT = """
당신은 selenium + pytest 기반 QA 자동화 엔지니어입니다.
다음 우선순위 규칙에 따라 **모든 요소의 로케이터를 하나씩 추출해주세요.**
응답에는 코드만 출력하고, 어떤 설명이나 마크다운 서식도 포함하지 마세요.

# 서버 링크:
- 프론트엔드: https://github.com/gothinkster/react-redux-realworld-example-app
- 백엔드: https://github.com/gothinkster/node-express-realworld-example-app

# 우선순위 규칙:
- 1순위: ID
- 2순위: CSS Selector ('>' 사용 금지)
- 3순위: XPATH (ID, CSS가 불가능할 때만 사용) 

# 출력 형식:
- 아래 파이썬 형식으로 각 페이지별 로케이터를 정리해서 출력
- **클래스명은 반드시 PascalCase**로 작성 (예: LoginPage)
- **각 페이지의 모든 요소는 하나의 클래스 안에 통합**하여 작성 (중복 클래스 선언 금지)
- **변수명**은 반드시 **UPPER_SNAKE_CASE**로 작성하고, 페이지명을 접두어로 사용 (예: editorLoginInput)
- pagename = HTML 주석 내용 + "page" (예: editor page)
- HTML 코드를 분석했을때 주석과 페이지 명이 일치하지 않더라도 주석 내용을 페이지명으로 사용

# 예시코드:
```python
## [pagename]

from selenium.webdriver.common.by import By

class EditorPageLocators:
    editorLoginInput = (By.ID, "ID")
    editorEmailInput = (By.CSS_SELECTOR, "input[type='email'][placeholder='Email']")
    editorPasswordInput = (By.CSS_SELECTOR, "input[type='password'][placeholder='Password']")
    editorSubmitInput = (By.CLASS_NAME, "btn-primary")
```

아래는 HTML입니다:
"""


