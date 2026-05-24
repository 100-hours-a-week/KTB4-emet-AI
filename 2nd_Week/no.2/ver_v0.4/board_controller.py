from fastapi import HTTPException
import board_model

from datatype import Draft, draft2board
from ollama_controller import content2summary

def get_boards():
    boards = board_model.get_boards()
    if not boards:
        raise HTTPException(status_code = 404, detail = "no_boards_found")
    
    return {"data": boards} 
    
def get_board(board_id : int):
    if board_id <= 0:
        raise HTTPException(status_code = 400, detail = "invalid_board_id")
        
    board = board_model.get_board_by_board_id(board_id)
    if not board:
        raise HTTPException(status_code = 404, detail = "board_not_found")
    
    return {"data": board}

def create_board(draft : Draft):

    if not draft.title or not draft.user_name:
        raise HTTPException(status_code = 400, detail = "missing_required_fields")

    new_board = draft2board(draft)
    board_model.add_board(new_board)

    return {"data": new_board}

def update_board(board_id : int, title : str, content : str | None):

    if board_id <= 0:
        raise HTTPException(status_code = 400, detail = "invalid_board_id")
    if not board_id or not title:
        raise HTTPException(status_code = 400, detail = "missing_required_fields")
    
    board = board_model.update_board(board_id, title, content, None)
    if board is None:
        raise HTTPException(status_code = 404, detail = "board_not_found")

    return {"data": board}

def delete_board(board_id : int):
    
    delete_board_id = board_model.delete_board(board_id)

    if delete_board_id == -1 :
        raise HTTPException(status_code = 404, detail = "board_not_found")
    elif delete_board_id != board_id:
        raise HTTPException(status_code = 400, detail = "board_id_error")
    
    return {"data": f"{board_id}"}

def update_summary(board_id : int):
    print(-1)
    if board_id <= 0:
        raise HTTPException(status_code = 400, detail = "invalid_board_id")
    print(0)
    board = board_model.get_board_by_board_id(board_id)
    print(1)
    if not board:
        raise HTTPException(status_code = 404, detail = "board_not_found")
    print(2)
    content_need_summary = board.content
    summary = content2summary(content_need_summary)
    print(3)
    if summary is None or summary == "요약 불가능" or summary == "":
        raise HTTPException(status_code = 400, detail = "can_not_be_summarized")
    print(4)
    board = board_model.update_board(board_id, None, None, summary)
    print(5)
    return board