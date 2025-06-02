# Python 베이스 이미지 사용
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 전체 프로젝트 복사
COPY . .

# 기본 실행 명령 (파이프라인에서 override 가능)
CMD ["pytest", "qa-realworld-automation/tests", "--maxfail=1", "--disable-warnings", "-v"]