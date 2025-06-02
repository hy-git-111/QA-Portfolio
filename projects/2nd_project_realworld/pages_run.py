import os
import time
import importlib
from ai_generate.claude_generate import generate_with_claude
from prompts.library_context import COMMON_LIBRARY_CONTEXT  # ✅ Claude system 메시지용

PROMPT_DIR = "prompts/pages"
PAGE_OUTPUT_DIR = "qa-realworld-automation/pages"

prompt_files = [
    "base_prompt",     
    "article_prompt",
    "editor_prompt",
    "home_prompt",
    "login_prompt",
    "profile_prompt",
    "settings_prompt",
    "signup_prompt"
]

prompt_variable_map = {
    "base_prompt": "BASE_PAGE_PROMPT",        
    "article_prompt": "ARTICLE_PAGE_PROMPT",
    "editor_prompt": "EDITOR_PAGE_PROMPT",
    "home_prompt": "HOME_PAGE_PROMPT",
    "login_prompt": "LOGIN_PAGE_PROMPT",
    "profile_prompt": "PROFILE_PAGE_PROMPT",
    "settings_prompt": "SETTINGS_PAGE_PROMPT",
    "signup_prompt": "SIGNUP_PAGE_PROMPT"
}

def run_prompt_one_by_one():
    os.makedirs(PAGE_OUTPUT_DIR, exist_ok=True)  # ✅ 폴더 없을 경우 자동 생성

    for file_name in prompt_files:
        try:
            module_path = f"prompts.pages.{file_name}"
            prompt_var = prompt_variable_map[file_name]

            print(f"\n🚀 [시작] {file_name} Claude 호출 중...")
            module = importlib.import_module(module_path)
            prompt = getattr(module, prompt_var)

            result = generate_with_claude(
                prompt,
                log_name_hint=file_name.replace('_prompt', ''),
                system=COMMON_LIBRARY_CONTEXT  # ✅ Claude 구조 인식 시스템 메시지 전달
            )

            # ✅ base만 예외적으로 base_page.py로 저장
            if file_name == "base_prompt":
                output_file = "base_page.py"
            else:
                output_file = f"{file_name.replace('_prompt', '')}_page.py"

            output_path = os.path.join(PAGE_OUTPUT_DIR, output_file)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result)

            print(f"✅ [완료] {output_file} 저장됨\n")
            time.sleep(6)  # ✅ 호출 간 충분한 딜레이 (Rate Limit 방지)

        except Exception as e:
            print(f"❌ [에러] {file_name}: {str(e)}")
            continue

if __name__ == "__main__":
    run_prompt_one_by_one()
