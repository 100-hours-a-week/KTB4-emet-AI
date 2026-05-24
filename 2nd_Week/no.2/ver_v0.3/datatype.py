from pydantic import BaseModel,Field
import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Session, create_engine

# 클라이언트가 작성한 글(인증전)
class Draft(BaseModel):
    title : str 
    user_name : str
    content : str | Optional[str]

#클라이언트가 작성한 글(인증됨)
# <DB> CREATE TABLE "bard"(....)
class Board(Draft, SQLModel, table = True):
    # <DB> Field () = pydantic 데이터 검증 기능 + SQLAlchemy 컬럼 설정
    # <DB> python상에서 None으로 생성하고 sqlmodel에서 생성할때 자동 id부여를 위해 설정
    board_id : int | None = Field(default = None, primary_key = True)
    summary : str | Optional[str] = Field(default = None)

    def set_summary(self, summary : str):
        self.summary = summary



def create_db_and_table(engine):
    # <DB> 실질적인 db와 테이블 생성
    SQLModel.metadata.create_all(engine)

# <DB>에서 board_id 자동생성하기에 조정
def draft2board(draft: Draft):
    return Board(title = draft.title, user_name =  draft.user_name, content = draft.content)
