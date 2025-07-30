# python 3.13 슬림 이미지 사용
FROM python:3.13-slim

# 작업 디렉토리 지정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 전체 복사
COPY . /app/

# 포트 노출 (Django 기본 8000)
EXPOSE 8000

# Django 개발 서버 실행 명령 (나중에 gunicorn으로 변경 가능)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
