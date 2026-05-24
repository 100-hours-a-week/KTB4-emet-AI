#2.1
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse
import uvicorn
import httpx
import json
# 2.2
import asyncio
from ollama import AsyncClient
# 2.3
from sqlmodel import SQLModel, Session, create_engine, select
from fastapi.encoders import jsonable_encoder

#.my datatype.py
from datatype import Draft, Board, create_db_and_table, draft2board

# local에 설치된 gemma4_e4b url -> 상수
URL= "http://localhost:11434/v1/chat/completions"
AI_MODEL = "gemma4:e2b"

app = FastAPI()

# 글목록
#boards = list()
# 고유 글 식별자
#boards_id_number = int(0)
# <DB> db 파일
sqlite_file_name = "databse.db"    
# <DB> db와 네트워크 연결을 유지하는 engine(엔진) 생성, echo: sql 어떤상태인지 print() 
engine = create_engine(f"sqlite:///:{sqlite_file_name}", echo = True)

# 글목록에서 특정 글 찾기 -> DB 사용잇 async 사용(선택)
def find_board(board_id : int):
    try:
        with Session(engine) as session:
            statement = select(Board).where(Board.board_id == board_id)
            # <DB> 테이블 Board 선핵해서 상태 정보 print() 
            results = session.exec(statement)
            # <DB> 가져온 테이블 정보를 Board 객체 list 형태로 리턴  
            board = results.one()
            # 딕셔너리 리스트로 변환
            board_json = board.model_dump()

        return board_json
    except Exception as e:
        print(e)
    return None
    

# 메인화면
@app.get("/")
async def home():
    return JSONResponse({"message": "Hello, This is Emet's site"})

# 글목록확인
@app.get("/boards")
async def get_boards(request : Request):
    boards_json = ""
    try:
        # <DB> SELECT * FROM Board 
         # <DB> session = Session(engine) 은 엔진(연결) 1개로 통해 만들 수 있는 여러 통로 개념  
        with Session(engine) as session:
            statement = select(Board)
            # <DB> 테이블 Board 선핵해서 상태 정보 print() 
            results = session.exec(statement)
            # <DB> 가져온 테이블 정보를 Board 객체 list 형태로 리턴  
            boards = results.all()
            # 딕셔너리 리스트로 변환
            boards_json = [board.model_dump() for board in boards]    
        
        return JSONResponse({"message": boards_json})
    except Exception as e:
        print(e)
        return JSONResponse({"message": f"Failed to get board,{e}"}, status_code = 400)

# 글 작성
# 클라이언트가 정상 작성했으면 글목록에 추가됨, 비정상 작성이면 반려됨
@app.post("/boards/create_board")
async def create_board(draft : Draft):
    board = None
    try:   
        board = draft2board(draft)
        
        # <DB> boards.append(board) 대체
        with Session(engine) as session:
            # <DB> 에 변경사항 추가
            session.add(board)
            # <DB> 에 추가한 변경사항 저장
            session.commit()
            # <DB> 명시적 새로고침, 현재 seesion 종료이후 board_id 확인가능해짐
            session.refresh(board)
        return JSONResponse({"message": f"Success to create board:{board.board_id}"})  
    
    except Exception as e:
        print(e)
        return JSONResponse({"message": f"Failed to create board,{e}"}, status_code = 500)
    
# 글목록에서 특정 글 상세 확인
@app.get("/boards/get/{board_id}")
async def get_board(board_id : int):    
    target_board = find_board(board_id)
    
    if target_board is None:
        return JSONResponse({"message": f"board_id:{board_id} is not exist"}, status_code = 404)

    return target_board


# 글 수정(board_id와 user_name는 변경 불가능)
@app.patch("/boards/patch/{board_id}")
def update_board(board_id : int, title : str, content : str):
    try:
        # <DB> SELECT * FROM Board 
        # <DB> session = Session(engine) 은 엔진(연결) 1개로 통해 만들 수 있는 여러 통로 개념  
        with Session(engine) as session:
            statement = select(Board).where(Board.board_id == board_id)
            # <DB> 테이블 Board 선핵해서 상태 정보 print() 
            results = session.exec(statement)
            # <DB> 가져온 테이블 정보를 Board 객체 형태로 리턴  
            board = results.one()
            # 글목록에 글이 없는 경우 또는 매칭되는 board_id 작성글이 없는경우
            if board is None:
                return JSONResponse({"message": f"{board_id} is not exist"}, status_code = 404)
            # <DB> 객체 정보 수정
            board.title = title
            board.content = content
            # <DB>에 객체 수정 정보 전달
            session.commit()
        return JSONResponse({"message": f"Success to update the board:{board_id}"})    
    except Exception as e:
        print(e)
        return JSONResponse({"message": f"{board_id} is not exist\n{e}"}, status_code = 400)     

# 글 삭제
@app.delete("/boards/delete/{board_id}")
def remove_board(board_id : int):
    try:
        # <DB> SELECT * FROM Board 
        # <DB> session = Session(engine) 은 엔진(연결) 1개로 통해 만들 수 있는 여러 통로 개념  
        with Session(engine) as session:
            statement = select(Board).where(Board.board_id == board_id)
            # <DB> 테이블 Board 선핵해서 상태 정보 print() 
            results = session.exec(statement)
            # <DB> 가져온 테이블 정보를 Board 객체 형태로 리턴  
            board = results.one()
            # 글목록에 글이 없는 경우 또는매칭되는 board_id 작성글이 없는경우
            if board is None:
                return JSONResponse({"message": f"{board_id} is not exist"}, status_code = 404)
            # <DB> 개체 삭제
            session.delete(board)
            # <DB>에 개체 삭제 정보 전달
            session.commit()
        return JSONResponse({"message": f"Success to remove the board:{board_id}"})    
    except Exception as e:
        print(e)
        return JSONResponse({"message": f"{board_id} is not exist\n{e}"}, status_code = 400) 
    
 
def create_requset_ai(content : str):   
    payload = {
	    "model": AI_MODEL,
	    "messages": [
            {"role": "system", "content": "당신은 친절한 AI 어시스턴트입니다."
		    },
	        {"role": "user", "content": f"{content}에 대해 없앨 내용 없애고 원래 내용보다 짧게 설명해줘.단답형도 가능해, 내용 이해가 불가능거나 너무 짧으면 절대 아무말도 답변 하지마"
            }
        ],
        "stream": True
    }
    response_summary = ""
    try: 
        with httpx.Client(timeout = 60.0) as client:
            response = client.send(client.build_request("POST",URL, json = payload), stream = True )
            # response가 iterable한지 __iter__ 속성여부로 파악
            # 1줄씩 iter 진행    
            for line in response.iter_lines():
                if line and line.startswith("data: "):
                    data_str = line[6:]
                    if data_str.strip() == "[DONE]":
                        break
                    if '"content":' in data_str:
                        data_json = json.loads(data_str)
                        chunk = data_json["choices"][0]["delta"]["content"]
                        #print(f"chunk: {chunk}", end = "",flush=True)
                        response_summary += chunk
        print(response_summary)
    except Exception as e:
        print(e)
    
    return response_summary
    
    

# 글의 내용 요약
@app.post("/boards/get/{board_id}/create/summary")
def create_summary(board_id: int):
    target_board = find_board(board_id)
    if target_board is None:
        return JSONResponse({"message": f"board_id:{board_id} is not exist"}, status_code = 404)
    ## 비동기 실행
    ## summary = asyncio.run(create_requset_ai(target_board.content))
    ## 동기실행
    summary = create_requset_ai(target_board['content'])

    if summary is None or summary == "요약 불가능" or summary == "":
        summary = None
        return JSONResponse({"message": f"Board ID:{board_id} can't create summary"}, status_code = 400)
    
    try:
        with Session(engine) as session:
            statement = select(Board).where(Board.board_id == board_id)
            # <DB> 테이블 Board 선핵해서 상태 정보 print() 
            results = session.exec(statement)
            # <DB> 가져온 테이블 정보를 Board 객체 형태로 리턴  
            board = results.one()
            # 요약하는동안 글목록에 글이 없는 경우 또는 매칭되는 board_id 작성글이 없는경우
            if board is None:
                return JSONResponse({"message": f"board:{board_id} is not exist"}, status_code = 404)
            # 요약하는 동안 글 내용이 바뀐경우
            if board.content.strip() != target_board['content'].strip():
                return JSONResponse({"message": f"board:{board_id}' content was changed, please confirm the content and retry."}, status_code = 400)
            # <DB> 객체 정보 수정
            board.summary = summary
            # <DB>에 객체 수정 정보 전달
            session.commit()
        return JSONResponse({"message": f"Success to update summary in the board:{board_id}\n{summary}"})    
    except Exception as e:
        print(e)
        return JSONResponse({"message": f"{e}"}, status_code = 400)



if __name__ == "__main__":
    # <DB> 실질적인 db와 테이블 생성
    create_db_and_table(engine)
    uvicorn.run("main:app", reload = True)