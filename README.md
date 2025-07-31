# 🏢 회의실 예약 관리 시스템

 [프로젝트 GitHub Repository](https://github.com/19SangHyun/meeting-room-reservation)

  [데모 URL링크](http://54.206.101.220:8000/)

##  프로젝트 개요
사내 회의실의 효율적인 예약과 관리를 위한 웹 애플리케이션입니다.  
Django를 기반으로 제작되었으며, 사용자 인증, 회의실 예약, 중복 방지 등의 기능을 제공합니다.  
Docker 기반으로 누구나 손쉽게 실행할 수 있도록 구성되었습니다.

---

##  주요 기능
- 사용자 회원가입 / 로그인
- 회의실 등록 (관리자 전용)
- 회의실 목록 조회
- 회의실 예약 / 예약 수정 / 예약 취소
- 중복 예약 방지 및 시간 유효성 검증

---

##  기술 스택
| 구분 | 기술 |
|------|------|
| Backend | Python 3.13.5, Django |
| Frontend | Django Template (HTML, CSS, Tailwind) |
| Database | SQLite (로컬) |
| 배포환경 | Docker, AWS EC2(Ubuntu) |

---

##  로컬 실행 방법 (Docker 기반)

### 1. Docker 설치
Docker가 설치되어 있지 않다면 아래 링크를 참고해 설치해 주세요.  
 [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

### 2. Docker 이미지 다운로드
```bash
docker pull kalokill/testproject:latest
```

### 3. 컨테이너 실행
```bash
docker run -d -p 8000:8000 kalokill/testproject:latest
```

### 4. 웹 브라우저에서 접속

실행 후 http://localhost:8000 로 접속하면 웹 애플리케이션을 이용할 수 있습니다.

### 5. 사용 시 주의사항

관리자 계정 ID : everspinadmin , password: everspin0000 입니다.
http://localhost:8000/admin (로컬) , http://54.206.101.220:8000/admin (웹배포) 관리자 페이지에서 회의실 생성 및 삭제 진행할 수 있습니다.

초기 로컬 환경에서는 회의실이 생성되어있지 않을 텐데, 관리자 계정으로 접속 후 생성할 수 있습니다.

테스트 프로젝트이므로 도메인 연결이나 https 인증, nginx 연결은 진행하지 않았습니다.

---

##  설계 내용 및 고민

### 1. 사용자 인증 및 권한
Django 기본 User 모델을 상속한 커스텀 유저 모델 사용

사용자 권한에 따라 관리자(admin) 여부 구분

관리자만 회의실 등록 및 삭제 가능

### 2. 예약 로직
예약 시점이 현재보다 과거인 경우 예약 불가

동일한 회의실의 동일 시간대 중복 예약 방지

예약 가능한 시간대만 선택할 수 있도록 검증

### 3. 관리자 기능
회의실 등록/삭제 기능 제공

예약 현황 조회 가능

향후 예약 승인 기능 및 통계 대시보드로 확장 가능

### 4. 프론트엔드 고려
Django Template 기반 HTML 구조

TailwindCSS로 간단한 반응형 UI 구성

자바스크립트는 최소화하여 학습 및 유지보수 용이

### 5. Docker 도입
로컬 환경과 배포 환경의 일관성 확보

의존성 격리 및 실행 단순화

비개발자도 이미지 실행만으로 바로 테스트 가능

---


##  향후 개선 사항
PostgreSQL 연동 및 배포 환경 데이터베이스 분리

관리자 전용 예약 통계 시각화 대시보드

예약 알림 (이메일, 푸시) 기능 추가

프론트엔드 React 등으로 리팩토링 가능성 고려
