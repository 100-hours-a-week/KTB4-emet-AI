from pydantic import BaseModel,Field
import datetime

# 클라이언트가 작성한 글(인증전)
class Draft(BaseModel):
    title : str
    user_name : str
    content : str | None

# 클라이언트가 작성한 글(인증됨)
class Board(Draft, BaseModel):
    board_id : int
    summary : str | None = Field(default = None)

    def set_summary(self, summary : str):
        self.summary = summary








def draft2board(board_id : int , draft: Draft):
    return Board(board_id = board_id ,title = draft.title, user_name =  draft.user_name, content = draft.content)