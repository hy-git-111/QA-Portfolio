# # automation/voting_judge.py

# # ✅ AI 비교 질문 생성기 (loop_tasks 기준 기반 + 역할별 체크리스트 + 설명 주석 + 카멜표기법 + 역할 충실도 + 연결 정확성 + 요소 일관성 + 기능별 명확성 + 함수 명확성 + fixture 범위 확인 + 실행 로그 명확성)
# def make_comparison_prompt(claude_code: str, gemini_code: str) -> tuple:
#     """
#     두 AI 모델이 생성한 코드를 비교하는 프롬프트를 생성하고, 코드와 평가 주석을 반환합니다.
    
#     :param claude_code: Claude가 생성한 코드
#     :param gemini_code: Gemini가 생성한 코드
#     :return: (merged_code, comment) 형태의 튜플
#     """
#     # 파일 이름을 코드의 첫 번째 라인이나 주석에서 추출 시도
#     file_name = ""
#     if claude_code.strip().startswith("#"):
#         # 첫 번째 주석 라인에서 파일명 추출 시도
#         first_line = claude_code.strip().split("\n")[0]
#         if "/" in first_line:
#             file_name = first_line.split("/")[-1]
#         else:
#             file_name = first_line
    
#     # 파일명에 따른 체크리스트 선택
#     checklist = ""
#     if "test_" in file_name:
#         checklist = """
# - assert 문이 명확하게 포함되어 있는가?
# - 반복 테스트 구조일 경우, parametrize를 적절히 사용하고 있는가?
# - try-except 구문이 포함되어 있는가?
# - 각 step마다 설명이 주석으로 포함되어 있는가?
# - PageObject를 import해서 재사용하고 있는가?
# - 테스트는 서로 독립적으로 구성되어 있는가?
# - 필요한 경우 명시적 대기를 사용하고 있는가?
# - 실패 시 로그 및 스크린샷 처리 로직이 포함되어 있는가?
# - 변수명, 함수명 등은 카멜 표기법(camelCase)으로 통일되어 있는가?
# - 테스트 함수명이 해당 테스트의 목적을 명확하게 설명하고 있는가?
# - 테스트 파일로서 검증 로직만 포함하고, 페이지 동작 구현은 포함하지 않는가?
# - PageObject, locator, fixture 등 공통 요소를 정확하게 import하고 있는가?
# - 프론트엔드 요소 선택자 및 주소 경로가 프로젝트 구조와 정확히 일치하는가?
# - conftest.py의 WebDriver fixture를 활용하고 있는가?
# - 테스트 대상 기능에 해당하는 PageObject 및 locator만 연결하고, 공통 요소(BasePage 등)는 중복 없이 일관되게 활용하고 있는가?
# - 다른 기능(예: 게시글 관련 요소)이 섞여 사용되고 있지 않은가?
# - 테스트 코드, locator, 페이지 객체 간의 기능 구분이 명확하고 구조가 충돌 없이 일관되게 구성되어 있는가?
# - 각 테스트는 실행 시 어떤 테스트가 성공/실패했는지 로그 또는 콘솔에 명확하게 출력되고 있는가?
#         """
#     elif "_page" in file_name:
#         checklist = """
# - BasePage를 상속하고 있는가?
# - 메서드가 명확하게 분리되어 있는가 (click, enter 등)?
# - locator를 외부 파일에서 import하여 사용하고 있는가?
# - load() 메서드가 포함되어 있는가?
# - 단일 책임 원칙에 따라 구성되어 있는가?
# - 명시적 대기(Explicit Wait)를 사용하는가?
# - 각 주요 동작과 구성에 대해 설명이 주석으로 포함되어 있는가?
# - 변수명과 메서드명은 카멜 표기법(camelCase)으로 작성되어 있는가?
# - 페이지 객체로서 동작 정의만 포함하고, 테스트 로직이나 설정은 포함되지 않는가?
# - locator, BasePage 등 공통 구성 요소를 정확하게 import하고 있는가?
# - 프론트엔드 요소 선택자와 URL 경로가 정확하게 일치하며, 중복 없이 재사용 가능한 구조로 작성되어 있는가?
# - 페이지가 맡고 있는 기능에 맞는 요소, 메서드만 포함되며 다른 기능과의 혼합 사용이 없는가?
#         """
#     elif "locator" in file_name:
#         checklist = """
# - 모든 locator가 상수로 선언되어 있는가?
# - By.ID 또는 CSS Selector를 사용하고 있는가?
# - 명확하고 일관된 명명법(camelCase)을 따르고 있는가?
# - 정의된 항목에 대해 설명이 주석으로 포함되어 있는가?
# - locator 정의만 포함하고, 실제 동작이나 테스트 코드는 포함되지 않는가?
# - 프론트엔드 요소의 구조 및 이름, 역할이 URL/화면 구성과 정확히 일치하며 재사용 가능하도록 구성되어 있는가?
# - locator 파일 간에 기능이 혼합되지 않고, 페이지별로 명확히 구분되어 있는가?
#         """
#     elif "conftest" in file_name:
#         checklist = """
# - 공통 fixture(WebDriver 등)가 명확하게 정의되어 있는가?
# - WebDriver 설정이 headless, implicit wait 등 실무 기준에 따라 구성되어 있는가?
# - 각 테스트가 이 fixture를 통해 드라이버를 재사용하도록 구성되어 있는가?
# - fixture가 적절한 범위(scope=function/module/session 등)로 선언되어 있는가?
# - 설정 외의 테스트 로직이나 페이지 객체는 포함되어 있지 않은가?
#         """
#     elif "config" in file_name:
#         checklist = """
# - BASE_URL, TIMEOUT, HEADLESS 설정이 포함되어 있는가?
# - 운영체제별 ChromeDriver 경로 설정이 자동화되어 있는가?
# - 다양한 운영체제(Windows/macOS/Linux)에서도 사용할 수 있도록 구성되어 있는가?
# - 주요 설정 항목에 대한 설명이 주석으로 포함되어 있는가?
# - 설정 변수들은 카멜 표기법(camelCase)을 따르고 있는가?
# - 설정값과 경로 정의만 포함하고, 실행 로직이나 테스트 코드는 포함되지 않는가?
#         """
#     else:
#         # 파일 유형을 파악할 수 없는 경우 기본 체크리스트
#         checklist = """
# - 코드가 명확하고 이해하기 쉬운가?
# - 변수명과 함수명이 카멜 표기법(camelCase)을 따르는가?
# - 주요 로직에 대한 주석이 포함되어 있는가?
# - 코드 구조가 일관되고 체계적인가?
# - 중복 코드 없이 재사용 가능한 구조로 설계되어 있는가?
#         """

#     prompt = f"""
# 모든 코드와 구성 요소는 카멜 표기법(camelCase)에 따라 명명되어야 하며, 역할에 맞는 구조와 명확한 이름으로 구성되어야 합니다.
# 각 파일은 자신의 역할에 충실해야 하며, 설정 파일은 설정만, 페이지는 동작만, 테스트는 검증만 포함되어야 합니다.
# 각 구성 요소는 서로 정확하게 연결되어야 하며, 공통 요소는 중복 없이 import하여 재사용되어야 합니다.
# 프론트엔드 구조와 요소, 주소 경로와의 일치성도 고려하여 구성의 정확성과 재사용성을 높여야 합니다.
# 테스트 파일은 conftest.py의 fixture를 활용하고, basePage, locator, PageObject와의 연결이 명확하게 구성되어야 하며, 전체 구조가 통일성을 유지해야 합니다.
# 모든 파일은 자신이 담당하는 기능 범위 내에서만 구성요소를 참조해야 하며, 다른 기능의 locator나 페이지 객체가 혼용되지 않아야 합니다.

# 다음 두 코드 중에서 어떤 것이 더 좋다고 생각하나요?
# 파일명: {file_name}

# [평가 체크리스트]
# {checklist}

# [Claude 코드]
# {claude_code}

# [Gemini 코드]
# {gemini_code}

# 각 항목에 대해 어떤 코드가 더 나은지 설명해주고, 최종적으로 어떤 코드를 선택할지 명시해줘.
#     """
    
#     # 여기에서는 실제 비교 판단 로직을 포함하지 않습니다.
#     # AI 루프 컨트롤러에서 다루는 것으로 가정합니다.
    
#     # 임시 반환값 (실제로는 AI 루프 컨트롤러에서 처리)
#     merged_code = claude_code  # 기본적으로 Claude 코드를 선택
#     comment = "# 판단 결과가 아직 반영되지 않았습니다."
    
#     return merged_code, comment


# # ✅ 병합 판단 결과를 명확한 주석으로 구성하는 함수
# def build_merge_comment(decision: str, reason: str) -> str:
#     """
#     병합 판단 결과를 명확한 주석으로 구성합니다.
    
#     :param decision: 선택 결정 ('Claude' 또는 'Gemini')
#     :param reason: 선택 이유
#     :return: 주석 형식의 병합 판단 결과
#     """
#     return f"# Claude 선택 결과: {decision}\n# 판단 이유:\n{reason.strip()}"