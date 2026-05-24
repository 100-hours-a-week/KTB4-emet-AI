from fastapi import APIRouter
import board_controller
from datatype import Draft

router = APIRouter(prefix = "/boards")

@router.get("")
def get_boards():
    return board_controller.get_boards()

@router.get("/{board_id}")
def get_board(board_id : int):
    return board_controller.get_board(board_id)

@router.post("", status_code = 201)
def create_board(draft : Draft):
    return board_controller.create_board(draft)

@router.patch("/{board_id}")
def update_board(board_id : int, title : str, content : str | None):
    return board_controller.update_board(board_id, title, content)

@router.delete("/{board_id}")
def delete_board(board_id : int):
    return board_controller.delete_board(board_id)

@router.patch("/{board_id}/summary")
def update_summary(board_id : int):
    print(-2)
    return board_controller.update_summary(board_id)