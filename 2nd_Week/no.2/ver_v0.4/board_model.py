import httpx
from sqlmodel import SQLModel, Session, create_engine, select
from fastapi.encoders import jsonable_encoder
#.my datatype.py
from datatype import Board

sqlite_file_name = "databse.db"
engine = create_engine(f"sqlite:///:{sqlite_file_name}", echo = True)
SQLModel.metadata.create_all(engine)

# 글목록 조회
def get_boards():
    boards = None

    with Session(engine) as session:
        statement = select(Board)
        results = session.exec(statement)
        boards = results.all()

    return boards

# board_id로 글 조회
def get_board_by_board_id(board_id : int):
    board = None

    with Session(engine) as session:
        statement = select(Board).where(Board.board_id == board_id)
        results = session.exec(statement)
        # <DB> 찾는 값이 없는 경우 None 리턴
        board = results.one_or_none()

    return board 

# create_board(Draft) -> add_board(dict)
# 초안(draft)로 글 추가  
def add_board(board : Board):

    with Session(engine) as session:
        session.add(board)
        session.commit()
        session.refresh(board)

    return board

def update_board(board_id : int, title : str | None, content : str | None, summary : str | None):

    board = get_board_by_board_id(board_id)

    with Session(engine) as session:
        """
        statement = select(Board).where(Board.board_id == board_id)
        results = session.exec(statement)  
        board = results.one()
        """
        if board is None:
            return None
        else:
            if title is not None:     
                board.title = title
            if content is not None:
                board.content = content
            if summary is not None:
                board.summary = summary
            session.commit() 
    
    return board


def delete_board(board_id : int):

    board = get_board_by_board_id(board_id)
    
    with Session(engine) as session:
        """
        statement = select(Board).where(Board.board_id == board_id)
        results = session.exec(statement) 
        board = results.one()
        """
        # 이미 없는 board_id인 경우
        if board is None:
            board_id = -1
        else :
            session.delete(board)
            session.commit()

    return board_id