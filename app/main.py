from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import model
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import desc
from .database import get_db


# makes new table that we define in model

model.Base.metadata.create_all(bind=engine)
app = FastAPI()


# class Post extends BaseModel

class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="postgres",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("database connection wasa succesfull")
        break
    except Exception as error:
        print("connecting to database fail")
        print("Error", error)
        time.sleep(2)


def getone(id: int):
    for post in my_posts:
        if post['id']==id:
            return post


def get_index_of_del_item(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


my_posts = [
    {"title": "post 1", "content": "content of post 1", "id": 1},
    {"title": "post 2", "content": "content of post 2", "id": 2},
]


@app.get("/")
def hello():
    return {"message": "Welcom to my API"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(model.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """,
    #     (post.title, post.content, post.publisshed),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = model.Post(
    #     title=post.title, content=post.content, published=post.published
    # )
    new_post = model.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/latest")
def get_latest_post(db: Session = Depends(get_db)):
    #     cursor.execute(
    #         """SELECT *
    # FROM posts
    # WHERE created_at=(
    #     SELECT max(created_at) FROM posts
    #     )"""
    #     )
    #     new_post = cursor.fetchone()
    # new_post=db.query(model.Post).from_statement(text( """SELECT *
    #  FROM posts
    #  WHERE created_at=(
    #      SELECT max(created_at) FROM posts
    #      )""")).first()
    new_post=db.query(model.Post).order_by(desc('created_at')).first()
    return {"detail": new_post}


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # post = cursor.fetchone()
    # conn.commit()
    post = db.query(model.Post).filter(model.Post.id == id)
    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.patch("/posts/{id}")
def patch_posts(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s WHERE id = %s RETURNING *""",
        (
            post.title,
            str(id),
        ),
    )
    up_post = cursor.fetchone()
    if up_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    conn.commit()
    return {"data": up_post}


@app.put("/posts/{id}")
def upadate_posts(id: int, post: Post,db: Session=Depends(get_db)):
    # cursor.execute(
    #     """UPDATE posts SET title = %s,content = %s WHERE id = %s RETURNING *""",
    #     (
    #         post.title,
    #         post.content,
    #         str(id),
    #     ),
    # )
    # up_post = cursor.fetchone()
    # conn.commit()
    up_query=db.query(model.Post).filter(model.Post.id==id)
    up_post=up_query.first()
    if up_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    up_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return {"data": up_query.first()}
