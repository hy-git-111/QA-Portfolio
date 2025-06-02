import subprocess
from pathlib import Path

# 현재 스크립트 위치: backend/postman/
postman_dir = Path(__file__).resolve().parent

print("\n📥 [1] 컬렉션 다운로드 실행 중...")
subprocess.run(["python3", str(postman_dir / "fetch_collection.py")], check=True)

print("\n📥 [2] 환경변수 다운로드 실행 중...")
subprocess.run(["python3", str(postman_dir / "fetch_environment.py")], check=True)

input("\n✅ 위 두 파일이 정상 생성되었는지 확인하세요. 계속하려면 Enter 입력...")

print("\n🧪 [3] Newman 테스트 실행 시작...")
subprocess.run(["python3", str(postman_dir / "run_postman.py")])

print("\n🎉 전체 자동화 완료!")
