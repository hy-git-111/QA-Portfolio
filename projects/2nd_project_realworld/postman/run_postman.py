import os
import sys
import subprocess
import json
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

# --- 1. 환경 변수 로드 ---
print("\n--- 환경 변수 로드 ---")

# .env 경로를 명시적으로 지정 (postman/ → ../backend/.env)
env_path = Path(__file__).resolve().parent.parent / "backend" / ".env"
load_dotenv(dotenv_path=env_path)

# 컬렉션/환경변수 파일 경로 가져오기 (.env에서 읽음)
COLLECTION_PATH = os.getenv("COLLECTION_PATH")
ENVIRONMENT_PATH = os.getenv("ENVIRONMENT_PATH")
print("🔎 파일 존재 확인(3team_collection.json):", os.path.exists(COLLECTION_PATH))
print("🔎 파일 존재 확인(3team_environment.json):", os.path.exists(ENVIRONMENT_PATH))

# 환경 변수 누락 시 에러 종료
if not COLLECTION_PATH:
    print("❌ 오류: COLLECTION_PATH 환경변수가 없습니다.", file=sys.stderr)
    sys.exit(1)

if not ENVIRONMENT_PATH:
    print("❌ 오류: ENVIRONMENT_PATH 환경변수가 없습니다.", file=sys.stderr)
    sys.exit(1)

print("✅ 컬렉션 파일 경로:", COLLECTION_PATH)
print("✅ 환경변수 파일 경로:", ENVIRONMENT_PATH)

# --- 2. 리포트 저장 폴더 생성 ---
# 현재 실행 중인 파일 기준으로 postman/reports 경로 만들기
report_dir = Path(__file__).resolve().parent / "reports"
report_dir.mkdir(exist_ok=True)

# 리포트 파일명 생성 / 현재 날짜 추가 (%Y-%m-%d_%H:%M:%S)
now_str = datetime.now().strftime("%Y%m%d")
report_filename = report_dir / f"newman_report_{now_str}.html"
json_report_filename = report_dir / f"newman_report_{now_str}.json"

# --- 3. Newman 명령어 구성 ---
command = [
    "newman", "run", COLLECTION_PATH,
    "-e", ENVIRONMENT_PATH,
    "--reporters", "cli,html,json",
    "--reporter-html-export", str(report_filename),
    "--reporter-json-export", str(json_report_filename),
]

print("\n--- Newman 실행 시작 ---")

# --- 4. 글로벌 node 모듈 경로 지정 (html 리포터 사용 시 필요) ---
node_path = subprocess.check_output(["npm", "root", "-g"]).decode().strip()
new_env = os.environ.copy()
new_env["NODE_PATH"] = node_path

# --- 5. Newman 실행 ---
result = subprocess.run(command, env=new_env)

# --- 6. 결과 출력 및 리포트 열기 ---
print(f"\n--- Newman 완료 ---")
print(f"📄 리포트 저장 위치: {report_filename}")
print(f"📄 JSON 리포트 저장 위치: {json_report_filename}")
# subprocess.run(["open", str(report_filename)])  # macOS 기준: 리포트 파일 자동으로 열기

# --- 7. 종료 코드 처리 ---
# 리포트 처리
with open(json_report_filename, encoding="utf-8") as f:
    report_data = json.load(f)
    total = report_data.get("run", {}).get("stats", {}).get("requests", {}).get("total", 0)
    failures = len(report_data.get("run", {}).get("failures", []))
    success = total - failures

# 실패(리턴코드 0 아님) 시: 오류 출력 + 종료
if result.returncode != 0 or failures > 0:
    print(f"\n📊 [Newman 테스트 결과 요약]")
    print(f"✅ 전체 실행 요청 수   : {total}개")
    print(f"⭕️ 성공한 테스트 케이스 : {success}개")
    print(f"❌ 실패한 테스트 케이스 : {failures}개")
    # print(f"❌ [Newman] 실패한 테스트 케이스: {failures}개", file=sys.stderr)
    # print(f"⭕️ [Newman] 실패한 테스트 케이스: {failures}개", file=sys.stderr)
    sys.exit(result.returncode)

# 성공(리턴코드 0) 시: 통과 메시지 + 정상 종료
else:
    print("✅ [Newman] 테스트 결과: 전체 통과", file=sys.stderr)
    sys.exit(0)