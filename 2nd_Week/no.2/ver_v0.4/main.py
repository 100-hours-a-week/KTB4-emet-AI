#2.1
from fastapi import FastAPI
import uvicorn


# 2.5
from board_router import router as board_router

app = FastAPI()
app.include_router(board_router, tags=["boards"])

"""
# 미들웨어
@app.middleware("http")
async def process_time_middleare(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
"""
"""
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

"""

if __name__ == "__main__":
    uvicorn.run("main:app", reload = True)