import os
from dotenv import load_dotenv
from prompts.common import CONFIG_PROMPT, CONFTEST_PROMPT, REQUIREMENTS_PROMPT, PYTEST_INI_PROMPT
from ai_generate.claude_generate import generate_with_claude

load_dotenv()

PROMPT_LIST = [
    {
        "name": "config",
        "prompt": CONFIG_PROMPT,
        "output_path": "qa-realworld-automation/config/config.py"
    },
    {
        "name": "conftest",
        "prompt": CONFTEST_PROMPT,
        "output_path": "qa-realworld-automation/tests/conftest.py"
    },
    {
        "name": "requirements",
        "prompt": REQUIREMENTS_PROMPT,
        "output_path": "qa-realworld-automation/requirements.txt"
    },
    {
        "name": "pytest_ini",
        "prompt": PYTEST_INI_PROMPT,
        "output_path": "qa-realworld-automation/pytest.ini"
    },
]

def main():
    for task in PROMPT_LIST:
        print(f"\n🚀 Claude에게 '{task['name']}' 프롬프트 요청 중...\n")
        result = generate_with_claude(task["prompt"])
        print(f"✅ Claude 응답({task['name']}):\n\n{result[:300]}...\n")

        os.makedirs(os.path.dirname(task["output_path"]), exist_ok=True)
        with open(task["output_path"], "w", encoding="utf-8") as f:
            f.write(result)
        print(f"💾 저장 완료: {task['output_path']}")

if __name__ == "__main__":
    main()
