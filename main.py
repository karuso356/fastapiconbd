from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, select
from typing import Optional, List
from db import engine, create_db_and_tables, SessionDep  # <--- importamos aquí

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API corriendo en EC2 🚀 con RDS PostgreSQL"}


@app.get("/check-db")
def check_db(session:SessionDep):
    result = session.exec(select(User)).first()
    return{"db_status":result}


# -------- MODELOS --------
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/users/", response_model=User)
def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

@app.get("/users/", response_model=List[User])
def list_users():
    with Session(engine) as session:
        return session.exec(select(User)).all()


@app.post("/books/", response_model=Book)
def create_book(book: Book):
    with Session(engine) as session:
        session.add(book)
        session.commit()
        session.refresh(book)
        return book

@app.get("/books/", response_model=List[Book])
def list_books():
    with Session(engine) as session:

        return session.exec(select(Book)).all()
