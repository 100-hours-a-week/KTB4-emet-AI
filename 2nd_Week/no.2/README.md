# FastAPI로 커뮤니티 서비스의 백엔드 구현

## 버전 별 실행방법
---
```bash

# 가상환경 패키지 설치
uv add fastapi uvicorn sqlmodel httpx

# Ollama 설치 후
# Ollama 실행(모델: gemma4:e2b ) (ver0.2, ver0.3, ver0.4 요약 기능 사용 시)
ollama pull gemma4:e2b
ollama serve

# sql모델 패키지 설치 (ver0.3, ver0.4 실행시)
pip install fastapi sqlmodel uvicorn


# pwd --> .../2nd_Week/no.2
# 버전 {}
# uv run ver_v0.{}/main.py

uv run ver_v0.1/main.py
uv run ver_v0.2/main.py
uv run ver_v0.3/main.py
uv run ver_v0.4/main.py


#API 문서 자동 생성 : http://127.0.0.1:8000/docs
```

## 최종 버전(0.4) 프로젝트 설계도
ver0.4/    
├── main.py                # 메인   
├── board_router.py        # 라우터 (엔드포인트 정의)   
├── board_controller.py    # 게시글 컨트롤러   
├── ollama_controller.py   # ollama 컨트롤러(AI 요약)   
├── datatype.py            # 데이터 모델  
└── database.py            # DB 연결 설정   

## DB구 조

### Board 테이블 (board 테이블)
| 컬럼명       | 타입      | NULL 허용 | 기본값   | 제약조건        | 설명                    |
|-------------|---------|---------|--------|--------------|------------------------|
| `board_id`  | INTEGER | ❌       | 자동증가  | PRIMARY KEY  | 게시글 고유 ID           |
| `title`     | TEXT    | ❌       | -      | NOT NULL     | 게시글 제목              |
| `user_name` | TEXT    | ❌       | -      | NOT NULL     | 작성자 이름              |
| `content`   | TEXT    | ✅       | NULL   | -            | 게시글 내용              |
| `summary`   | TEXT    | ✅       | NULL   | -            | AI 요약 (요약 전 NULL)  |


## API  Endpoints
Base URL : `/boards`

| Method   | Endpoint               | Description       | Status Code |
|----------|------------------------|-------------------|-------------|
| `GET`    | `/boards`              | 전체 게시글 조회   | 200         |
| `GET`    | `/boards/{board_id}`   | 단일 게시글 조회   | 200         |
| `POST`   | `/boards`              | 게시글 생성        | 201         |
| `PATCH`  | `/boards/{board_id}`   | 게시글 수정        | 200         |
| `DELETE` | `/boards/{board_id}`   | 게시글 삭제        | 200         |
| `PATCH`  | `/boards/{board_id}/summary` | AI 요약 생성 | 200       |


## ⚠️ Error Handling

| Status Code | detail | 발생 상황 |
|-------------|--------|-----------|
| `400` | `invalid_board_id` | board_id ≤ 0 |
| `400` | `missing_required_fields` | title 또는 user_name 누락 |
| `400` | `board_id_error` | 삭제 결과 ID 불일치 |
| `400` | `can_not_be_summarized` | 요약 결과 없음 또는 요약 불가 |
| `404` | `no_boards_found` | 전체 게시글 없음  |
| `404` | `board_not_found` | 해당 ID 게시글 없음 |

