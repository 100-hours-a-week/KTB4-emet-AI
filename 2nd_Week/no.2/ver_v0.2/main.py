from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse
import uvicorn
import httpx
import json

import asyncio
from ollama import AsyncClient

from datatype import Draft,Board,draft2board

# local에 설치된 gemma4_e4b url -> 상수
URL= "http://localhost:11434/v1/chat/completions"
AI_MODEL = "gemma4:e2b"

app = FastAPI()
# 글목록
boards = list()
# 고유 글 식별자
boards_id_number = int(0)

# 글목록에서 특정 글 찾기 -> DB 사용잇 async 사용
def find_board(board_id : int):
    global boards
    # 작성된 글이 없는 경우
    if len(boards) <= 0:
        return None
    return next((b for b in boards if b.board_id == board_id), None)

# 메인화면
@app.get("/")
async def home():
    return JSONResponse({"message": "Hello, This is Emet's site"})

# 글목록확인
@app.get("/boards")
async def get_board(request : Request):
    # 문제가 생긴 글목록인 경우
    if len(boards) < 0 :
        return JSONResponse({"message": f"Boards has no board"}, status_code = 404)
    
    # 작성된 글이 없는 경우에도 빈공간 뛰움
    return boards

# 글 작성
# 클라이언트가 정상 작성했으면 글목록에 추가됨, 비정상 작성이면 반려됨
@app.post("/boards/create_board")
async def create_board(draft : Draft):
    try:
        global boards_id_number

        # 생성횟수가 int 넘어서 overflow한 경우 
        if boards_id_number < 0 or boards_id_number is None: 
            return JSONResponse({"message": "Failed to create board,boards over the creation limit"}, status_code = 500)
        # 제목이 없는 경우
        elif draft.title == "" or draft.title is None: 
            return JSONResponse({"message": "Failed to create board,title is None"}, status_code = 400)
        # 유저 이름이 없는 경우
        elif draft.user_name == "" or draft.user_name is None: 
            return JSONResponse({"message": "Failed to create board,user_name is None"}, status_code = 403)
        
        boards_id_number += 1 
        board = draft2board(boards_id_number, draft)
        boards.append(board)
        return JSONResponse({"message": "Success to create board"})
    
    except Exception as e:
        print(e)
        return JSONResponse({"message": f"Failed to create board,{e}"}, status_code = 500)

# 글목록에서 특정 글 상세 확인
@app.get("/boards/get/{board_id}")
async def get_board(board_id : int):    
    target_board = find_board(board_id)

    # 글목록에 글이 없는 경우 또는매칭되는 board_id 작성글이 없는경우
    if target_board is None:
        return JSONResponse({"message": "the board is not exist"}, status_code = 404)    

    return target_board


# 글 수정(board_id와 user_name는 변경 불가능)
@app.patch("/boards/patch/{board_id}")
def update_board(board_id : int, title : str, content : str):
    target_board : Board
    target_board = find_board(board_id)

    # 글목록에 글이 없는 경우 또는매칭되는 board_id 작성글이 없는경우
    if target_board is None:
        return JSONResponse({"message": f"{board_id} is not exist"}, status_code = 404)    
    try:
        target_board.title = title
        target_board.content = content
    
    except Exception as e:
        print(e)
        return JSONResponse({"message": f"Failed to update board,{e}"}, status_code = 500)

    return JSONResponse({"message": "Success to updat the board"})     

# 글 삭제
@app.delete("/boards/delete/{board_id}")
def remove_board(board_id : int):
    target_board = find_board(board_id)

    # 글목록에 글이 없는 경우 또는매칭되는 board_id 작성글이 없는경우
    if target_board is None:
        return JSONResponse({"message": f"{board_id} is not exist"}, status_code = 404)    
    
    boards.remove(target_board)
    
    return JSONResponse({"message": "Success to remove the board"})    

"""
## 비동기 -> 동기가 되면 비동기 해보자
async def create_requset_ai(content : str):   
    payload = {
	    "model": AI_MODEL,
	    "messages": [
            # ??
		    {"role": "system", "content": "당신은 친절한 AI 어시스턴트입니다."
		    },
            # ??하지만, 내용을 이해할 수 없는 경우, 빈 공백인 경우에는 요약이 불가능하기때문에 반드시 \"요약 불가능\"이라고만 답변해줘.\n
	        {"role": "user", "content": f" {content}\n 앞의 내용을 요약해줘. "
            }
        ],
        "stream": "True"
    }
    client = httpx.AsyncClient(timeout = 60.0)
    response_summary = ""
    try:    
        async with await client.send(client.build_request("POST",URL, json = payload), stream = True ) as response:
            for line in response.iter_lines():
                if line and line.startswith("data: "):
                    data_str = line[6:]
                    if data_str.strip() == "[DONE]":
                        break
                    if '"content":' in data_str:
                        data_json = json.loads(data_str)
                        print(data_json["choices"][0]["data"]["content"], end = "",flush=True)

        response_json = response.json()
        # 응답의 content값만 추출
        response_summary = response_json["choices"][0]["message"]["content"]
        
    except Exception as e:
        print(e)

    if response_summary is not None or  response_summary != "":
        return response_summary
    else:
        return None
"""
def create_requset_ai(content : str):   
    payload = {
	    "model": AI_MODEL,
	    "messages": [
            {"role": "system", "content": "당신은 친절한 AI 어시스턴트입니다."
		    },
	        {"role": "user", "content": f"{content}에 대해 짧게 설명해줘."
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
                print(line)
                if line and line.startswith("data: "):
                    data_str = line[6:]
                    if data_str.strip() == "[DONE]":
                        break
                    if '"content":' in data_str:
                        data_json = json.loads(data_str)
                        chunk = data_json["choices"][0]["delta"]["content"]
                        print(f"chunk: {chunk}", end = "",flush=True)
                        response_summary += chunk
    
    except Exception as e:
        print(e)

    print(response_summary)
    return response_summary
    
    

# 글의 내용 요약
@app.post("/boards/get/{board_id}/create/summary")
def create_summary(board_id: int):
    
    target_board = find_board(board_id)
    # 글목록에 글이 없는 경우 또는매칭되는 board_id 작성글이 없는경우
    if target_board is None:
        return JSONResponse({"message": f"{board_id} is not exist"}, status_code = 404)    
    ## 비동기 실행
    ## summary = asyncio.run(create_requset_ai(target_board.content))
    ## 동기실행
    summary = create_requset_ai(target_board.content)

    if summary is None or summary == "요약 불가능" or summary == "":
        summary = None
        return JSONResponse({"message": f"Board ID:{board_id} can't create summary"}, status_code = 400)
        
    target_board.set_summary(summary)

    return summary




if __name__ == "__main__":
    uvicorn.run("main:app", reload = True)