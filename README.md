# Practice Project (Public)

업무 흐름을 예시로 보여주는 **연습용 프로젝트**입니다.  
상업적 제안/판매 목적이 아니라, 화면 구성과 데이터 흐름을 참고하기 위한 샘플입니다.

## 구성
- `landing_page/` : 연습용 1페이지 HTML (정적)
- `api/` : 피드백 수집 API (FastAPI + SQLite)

## 랜딩 페이지 보기
가장 간단한 방법:
- `landing_page/index.html`을 브라우저로 직접 열기

로컬 서버로 보기:
```
cd landing_page
python -m http.server 5500
```
브라우저에서 `http://localhost:5500` 접속

## API 실행 (로컬)
```
cd api
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --env-file .env
```

## API 실행 (Docker)
```
cd api
docker compose up --build
```

## 환경 변수
`.env.example`을 복사해 `.env`로 만들고 필요한 값을 수정합니다.
```
APP_NAME=Practice Feedback API
LOG_LEVEL=INFO
SQLITE_PATH=./data/feedback.db
ALLOWED_ORIGINS=http://localhost:5500,http://127.0.0.1:5500
RATE_LIMIT_PER_MINUTE=30
NOTIFY_MODE=console
WEBHOOK_URL=
```

## API 엔드포인트
- `GET /health` : 헬스체크
- `POST /api/feedback` : 피드백 등록

### 피드백 등록 예시
```
curl -X POST http://localhost:8000/api/feedback \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"홍길동\",\"email\":\"test@example.com\",\"phone\":\"010-1234-5678\",\"organization\":\"연습팀\",\"message\":\"연습용 피드백입니다.\",\"source_url\":\"http://localhost\"}"
```

## 피드백 확인
피드백은 SQLite DB에 저장됩니다.
- 위치: `api/data/feedback.db`
- DB Browser for SQLite 등으로 확인 가능

## 주의
- `.env`, `data/feedback.db`, `__pycache__`, `.venv`는 Git에 포함하지 않습니다.
