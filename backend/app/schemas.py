from pydantic import BaseModel

#shape of data your api expects or returns
# schemas.py
# Request model (client sends this)
class TodoCreate(BaseModel):
    title: str
    completed: bool = False

# Response model (server sends this back)
class TodoResponse(TodoCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True   # important: allows SQLAlchemy -> Pydantic conversion



class UserCreate(BaseModel):
    username : str
    password: str 

class UserOut(BaseModel):
    id : int 
    username: str 

    #will work with pythin objects also - as this wont return dict
    class config:
        orm_mode = True 

class Token(BaseModel):
    access_token: str 
    token_type: str 

class TokenData(BaseModel):
    username: str | None = None 

from typing import Optional

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None
