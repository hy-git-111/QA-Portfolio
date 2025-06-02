import os, requests, json
from pathlib import Path
from dotenv import load_dotenv

# 1. .env 파일 경로를 명시적으로 설정 (현재 스크립트 기준 상위 backend 폴더에 위치)
env_path = Path(__file__).resolve().parent.parent / "backend" / ".env"
load_dotenv(dotenv_path=env_path)

# .env에서 API 키와 UID 로드
load_dotenv(dotenv_path=".env")
API_KEY = os.getenv("POSTMAN_API_KEY")
ENVIRONMENT_UID = os.getenv("ENVIRONMENT_UID")

if not API_KEY or not ENVIRONMENT_UID:
    raise ValueError("필수 환경 변수가 누락되었습니다.")

print(f"\n→ UID로 환경변수 가져오기: {ENVIRONMENT_UID}")

# 환경변수 요청 코드
print("--- 환경변수 다운로드 시작 ---")
res = requests.get(
    f"https://api.getpostman.com/environments/{ENVIRONMENT_UID}",
    headers={"X-Api-Key": API_KEY}
)

print(f"📦 응답 상태 코드: {res.status_code}")
res.raise_for_status()

# JSON 응답 파싱
data = res.json()
print(f"📄 JSON 키 목록: {list(data.keys())}")

# 활성화된 값만 필터링 (비활성화된 변수 제거)
filtered_values = [v for v in data['environment']['values'] if v.get('enabled') == True]
data['environment']['values'] = filtered_values

# 파일 저장 
output_path = os.path.join(os.path.dirname(__file__), "3team_environment.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✔️ 환경변수 JSON 파일 저장 완료: {output_path}")

# # create_environment 함수의 values 인수로 전달될 딕셔너리 예시

# # 예시 1: 기본적인 문자열 값들
# # (가장 흔하게 사용되는 형태입니다)
# env_values_example_1 = {
#     "baseUrl": "http://localhost:8080/api/v1", # API 기본 URL
#     "token": "your_generated_auth_token",     # 인증 토큰 값
#     "username": "test_user_01",               # 사용자 이름
#     "password": "a_secure_password_123",      # 사용자 비밀번호
#     "apiKey": "aBcDeFgHiJkLmNoPqRsTuVwXyZ",    # API 키
#     "resourcePath": "/items/{{itemId}}"       # 다른 환경 변수나 경로 일부도 문자열로 저장 가능
# }
# # -> Postman에는 'baseUrl'="http://...", 'token'="your_..." 등으로 저장됩니다.


# # 예시 2: 숫자 값을 포함하는 경우
# # (Python에서는 정수/실수이지만, Postman에서는 문자열로 저장됩니다)
# env_values_example_2 = {
#     "port": 8000,              # 정수 (Python int)
#     "timeoutSeconds": 45.5,    # 실수 (Python float)
#     "userId": 98765,           # ID 값 (정수 형태가 편리할 때)
#     "maxRetries": 3            # 시도 횟수 등
# }
# # -> Postman에는 'port'="8000", 'timeoutSeconds'="45.5", 'userId'="98765" 등으로 저장됩니다.
# #    Postman에서 이 변수들을 사용할 때는 문자열 "8000" 등으로 사용됩니다.


# # 예시 3: 불리언(True/False) 값을 포함하는 경우
# # (Python에서는 불리언이지만, Postman에서는 'True' 또는 'False' 문자열로 저장됩니다)
# env_values_example_3 = {
#     "featureFlagA": True,      # Python True
#     "isDebugMode": False       # Python False
# }
# # -> Postman에는 'featureFlagA'="True", 'isDebugMode'="False" 등으로 저장됩니다.


# # 예시 4: 값이 비어있는 경우
# env_values_example_4 = {
#     "temporaryToken": "",      # 빈 문자열
#     "optionalParam": None      # None 값 (str(None) -> "None" 문자열로 저장됨)
# }
# # -> Postman에는 'temporaryToken'="", 'optionalParam'="None" 등으로 저장됩니다.
# #    None을 저장해야 하는 특별한 경우가 아니라면 보통 빈 문자열 ''을 사용하는 것이 더 일반적입니다.


# # 실제 사용할 때는 이 예시들을 조합하여 하나의 딕셔너리를 만듭니다.
# # 코드의 main 블록에서 사용된 예시는 문자열 값 위주로 구성되어 있습니다.
# # 아래는 실제 Postman 환경 생성 시 하나의 values 딕셔너리로 전달할 수 있는 형태입니다.
# full_environment_values = {
#     "baseUrl": "http://localhost:3000",
#     "token": "",
#     "username": "test_user",
#     "password": "test_password",
#     "userId": 101,             # 정수 값
#     "apiTimeout": 60,          # 정수 값
#     "enableCaching": True,     # 불리언 값
#     "notes": "로컬 개발 환경 설정" # 설명 등의 문자열 값
# }

# # 이 full_environment_values 딕셔너리를 create_environment 함수에 전달합니다.
# # env_uid = create_environment(
# #     name="RealWorld-Local-Extended",
# #     values=full_environment_values
# # )