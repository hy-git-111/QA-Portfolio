import os
import anthropic
from dotenv import load_dotenv
from datetime import datetime
from prompts.library_context import COMMON_LIBRARY_CONTEXT

# ✅ .env 파일 로드
load_dotenv(override=True)

# ✅ 로그 디렉토리 생성
LOG_DIR = "logs/claude_responses"
os.makedirs(LOG_DIR, exist_ok=True)

def generate_with_claude(
    prompt: str,
    llm_payload: str = "",
    log_name_hint: str = "claude",
    system: str = COMMON_LIBRARY_CONTEXT  # ✅ 추가된 부분
) -> str:
    """
    Claude API를 사용하여 프롬프트 기반 응답을 생성하고 응답을 로그로 저장합니다.
    """
    full_content = f"{prompt}\n\n---\n\n{llm_payload}" if llm_payload.strip() else prompt

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    try:
        message = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=8000,
            temperature=0.2,
            system=system,  # ✅ system 메시지를 인자로 주입
            messages=[{"role": "user", "content": full_content}]
        )
        print("✅ Claude 호출 완료")
        response_text = message.content[0].text.strip() if message.content else "# ⚠️ Claude 응답 없음"
    except Exception as e:
        print("❌ Claude 호출 중 오류:", e)
        response_text = f"# ❌ Claude 오류 발생: {str(e)}"

    # ✅ 응답 로그 저장
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{log_name_hint}_{timestamp}.txt"
    filepath = os.path.join(LOG_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as log_file:
        log_file.write(response_text)

    return response_text
