from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse
import uvicorn

from datatype import Draft,Board,draft2board


app = FastAPI()
boards = list()
boards_number = int(0)

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

#글 작성
#클라이언트가 정상 작성했으면 글목록에 추가됨, 비정상 작성이면 반려됨
@app.post("/boards/create_board")
async def create_board(draft : Draft):
    try:
        global boards_number

        # 생성횟수가 int 넘어서 overflow한 경우 
        if boards_number < 0 or boards_number is None: 
            return JSONResponse({"message": "Failed to create board,boards over the creation limit"}, status_code = 500)
        elif draft.title == "" or draft.title is None: 
            return JSONResponse({"message": "Failed to create board,title is None"}, status_code = 400)
        elif draft.user_name == "" or draft.user_name is None: 
            return JSONResponse({"message": "Failed to create board,user_name is None"}, status_code = 400)
        
        boards_number += 1 
        board = draft2board(boards_number, draft)
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


#글 수정(board_id와 user_name는 변경 불가능)
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

#글 삭제
@app.delete("/boards/delete/{board_id}")
def remove_board(board_id : int):
    target_board = find_board(board_id)

    # 글목록에 글이 없는 경우 또는매칭되는 board_id 작성글이 없는경우
    if target_board is None:
        return JSONResponse({"message": f"{board_id} is not exist"}, status_code = 404)    
    
    boards.remove(target_board)
    
    return JSONResponse({"message": "Success to remove the board"})    






if __name__ == "__main__":
    uvicorn.run("main:app", reload = True)