import os
from dotenv import load_dotenv
load_dotenv()   # 👈 load environment first

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

# imports after env
from sqlite import models
from sqlite.database import engine, SessionLocal, Base
from . import schemas

# 👇 NOW create tables in the right DB (Postgres if DATABASE_URL is set)
Base.metadata.create_all(bind=engine)



load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",   # React dev server
    "http://localhost:5173",   # Vite dev server (if you switch later)
    "http://127.0.0.1:3000",   # some browsers use 127.0.0.1
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



#database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#helpoer to create JWT access token 
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow()+(expires_delta or timedelta(minutes=15))
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#create a hashing context - generate and verify bcrypt hashes
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

#helper to hash password
def get_password_hash(password):
    return pwd_context.hash(password)

#helper for password verification 
def verify_pasword(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

#helper to get current user
from fastapi.security import OAuth2PasswordBearer

# tell FastAPI that login happens at /token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "could not validate credentials",
        headers = {"www-Authenticate":"Bearer"}
    )

    try: 
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        
    except JWTError:
        raise credential_exception
    
    user = db.query(models.UserDB).filter(models.UserDB.username == username).first()
    if user is None:
        raise credential_exception
    return user 

@app.get("/")
def default_print():
    return {"message":"Hello Todo App"}

#login endpoint - will return jwt token 
@app.post("/token",response_model = schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #find the user by username
    user = db.query(models.UserDB).filter(models.UserDB.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid Credentials")
    
    #verify the password
    if not verify_pasword(form_data.password, user.hashed_password):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid Credentials")
    
    #create the JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data = {"sub":user.username},
        expires_delta=access_token_expires
    )
    return {"access_token":access_token, "token_type":"bearer"}

#signup endpoint
@app.post("/users/", response_model = schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.UserDB).filter(models.UserDB.username == user.username).first()
    if db_user:
        raise HTTPException(status_code = 400, detail = "Username already exists")
    
    hashed_pw = get_password_hash(user.password)
    new_user = models.UserDB(username = user.username, hashed_password = hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


#post route to add the list 
@app.post("/todos/")
@app.post("/todos/", response_model=schemas.TodoResponse)
def create_todo(
    todo: schemas.TodoCreate,
    db: Session = Depends(get_db),
    current_user: models.UserDB = Depends(get_current_user)
):
    db_todo = models.TodoDB(
        title=todo.title,
        completed=todo.completed,
        user_id=current_user.id
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


#get request to show the list of todos
@app.get("/todos/", response_model=list[schemas.TodoResponse])
def get_todos(
    db: Session = Depends(get_db),
    current_user: models.UserDB = Depends(get_current_user)
):
    return db.query(models.TodoDB).filter(models.TodoDB.user_id == current_user.id).all()


#get 1 specific todo from todos
@app.get("/todos/{todo_id}", response_model=schemas.TodoResponse)
def get_todo_by_id(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: models.UserDB = Depends(get_current_user)
):
    todo = db.query(models.TodoDB).filter(
        models.TodoDB.id == todo_id,
        models.TodoDB.user_id == current_user.id
    ).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    return todo


#if we want to update the todo 
@app.put("/todos/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(
    todo_id: int,
    updated_todo: schemas.TodoUpdate,
    db: Session = Depends(get_db),
    current_user: models.UserDB = Depends(get_current_user)
):
    todo = db.query(models.TodoDB).filter(
        models.TodoDB.id == todo_id,
        models.TodoDB.user_id == current_user.id
    ).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo Not Found")

    if updated_todo.title is not None:
        todo.title = updated_todo.title
    if updated_todo.completed is not None:
        todo.completed = updated_todo.completed

    db.commit()
    db.refresh(todo)
    return todo

#if we want to delete
@app.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: models.UserDB = Depends(get_current_user)
):
    todo = db.query(models.TodoDB).filter(
        models.TodoDB.id == todo_id,
        models.TodoDB.user_id == current_user.id
    ).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo Not Found")

    db.delete(todo)
    db.commit()
    return {"message": f"Todo {todo_id} deleted"}
