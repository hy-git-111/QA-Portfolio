import os, requests, json
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 경로를 명시적으로 설정 (현재 스크립트 기준 상위 backend 폴더에 위치)
env_path = Path(__file__).resolve().parent.parent / "backend" / ".env"
load_dotenv(dotenv_path=env_path)

# 환경변수 값 로드
COLLECTION_PATH = os.getenv("COLLECTION_PATH")
API_KEY = os.getenv("POSTMAN_API_KEY")
COLLECTION_UID = os.getenv("COLLECTION_UID")

# 3. 필수 환경변수 누락 시 실행 중단
if not API_KEY or not COLLECTION_UID:
    raise ValueError("필수 환경 변수가 누락되었습니다.")

print(f"\n→ UID로 컬렉션 가져오기: {COLLECTION_UID}")

# 컬렉션 요청 코드
print("--- 컬렉션 다운로드 시작 ---")
res = requests.get(
    f"https://api.getpostman.com/collections/{COLLECTION_UID}",
    headers={"X-Api-Key": API_KEY}
)

print(f"📦 응답 상태 코드: {res.status_code}")
res.raise_for_status()
data = res.json()
print("📄 JSON 키 목록:", list(data.keys()))

collection_data = data["collection"]

# 파일 저장 
output_path = os.path.join(os.path.dirname(__file__), "3team_collection.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(collection_data, f, ensure_ascii=False, indent=2)

print(f"✔️ 컬렉션 JSON 파일 저장 완료: {output_path}")