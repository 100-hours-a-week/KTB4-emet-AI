from pydantic import BaseModel
from typing import Optional
from sqlmodel import SQLModel, Field

# 클라이언트가 작성한 글(초안)
class Draft(BaseModel):
    title : str 
    user_name : str
    content : str | Optional[str]

#서버가 저장한 글(최종본)
class Board(Draft, SQLModel, table = True):
    board_id : int | None = Field(default = None, primary_key = True)
    summary : str | Optional[str] = Field(default = None)

    def set_summary(self, summary : str):
        self.summary = summary

def draft2board(draft: Draft):
    return Board(title = draft.title, user_name =  draft.user_name, content = draft.content)
