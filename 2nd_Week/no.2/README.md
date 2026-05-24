## 버전 별 실행방법
---
```bash

# Ollama 실행(모델: gemma4:e2b ) (ver0.2, ver0.3, ver0.4 요약 기능 사용 시)
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
| `404` | `no_boards_found` | 게시글 없음 (전체 조회) |
| `404` | `board_not_found` | 해당 ID 게시글 없음 |

