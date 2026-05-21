from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse
import uvicorn

from datatype import Draft,Board,draft2board


app = FastAPI()
boards = list()
boards_number = int(0)

# 메인화면
@app.get("/")
async def home():
    return JSONResponse({"message": "Hello, This is Emet's site"})

#글 작성
#클라이언트가 정상 작성했으면 글목록에 추가됨, 비정상 작성이면 반려됨
@app.post("/board")
async def create_board(draft : Draft):
    try:
        global boards_number
        # 생성횟수가 int 넘어서 overflow 한경우 
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

# 글목록확인
@app.get("/get_boards")
async def get_board(request : Request):
    # 작성된 글이 없는 경우
    if len(boards) <= 0 :
        return JSONResponse({"message": f"Boards has no board"}, status_code = 404)
    
    return boards


# 글목록에서 특정 글 상세 확인
@app.get("/get_boards/{board_id}/")
async def get_board(board_id : int):
    # 작성된 글이 없는 경우
    if len(boards) <= 0 :
        return JSONResponse({"message": f"Boards has no board"}, status_code = 404)
    
    target_board = next((b for b in boards if b.board_id == board_id), None)

    # 매칭되는 board_id 작성글이 없는경우
    if target_board is None:
        return JSONResponse({"message": f"{board_id} is not exist"}, status_code = 404)    

    return target_board

'''
#글 수정
@app.put("/put/boards/{board_id}")
def modify_board(board):
     print()
#글 삭제
@app.delete("/delete_board/{board_id}")
def delete_board(board):
     boards.remove(board)
'''





if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)