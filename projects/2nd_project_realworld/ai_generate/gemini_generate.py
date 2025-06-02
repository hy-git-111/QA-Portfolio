# automation/gemini_generate.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

# 기존 환경변수가 있어도 강제로 덮어쓰기
load_dotenv(override=True)

# .env에서 GEMINI_API_KEY 값을 정확히 불러옴
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def generate_with_gemini(prompt: str, llm_payload="") -> str:
    """
    Gemini API를 사용하여 응답을 생성합니다.
    :param prompt: 프롬프트 문자열
    :param llm_payload: 이미 JSON으로 변환된 데이터
    :return: Gemini의 응답
    """
    try:
        # ✅ 최신 유료 모델 사용
        model = genai.GenerativeModel(
            "models/gemini-1.5-pro-latest",
            generation_config={
                "max_output_tokens": 8192,  # 최대 토큰 수를 8192로 설정
                "temperature": 0.2,         # 온도 설정
            }
        )

        if llm_payload.strip():
            full_content = f"{prompt}\n\n---\n\n{llm_payload}"
        else:
            full_content = prompt  # 구분자 넣지 않음

        response = model.generate_content(full_content)
        print(f"제미나이 호출 완료:{prompt}")
        return response.text.strip()
    except Exception as e:
        print("❌ Gemini 오류 발생:", e)
        return "# Gemini 오류로 생성 실패"