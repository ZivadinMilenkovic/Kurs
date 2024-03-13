from .. import model, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from sqlalchemy import desc

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.Post])
def get_posts(
    db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)
):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(model.Post).all()
    return posts


# for example if user want to create post he need to be login
# to see that user is login we need to add dependency get_user:Depends(oauth2.get_user)
@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    curr_user: int = Depends(oauth2.get_current_user),
):
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
    return new_post


@router.get("/latest", response_model=schemas.Post)
def get_latest_post(
    db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)
):
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
    new_post = db.query(model.Post).order_by(desc("created_at")).first()
    return new_post


@router.get("/{id}", response_model=schemas.Post)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    curr_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    curr_user: int = Depends(oauth2.get_current_user),
):
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


@router.patch("/{id}", response_model=schemas.Post)
def patch_posts(
    id: int,
    post: schemas.PostPatch,
    db: Session = Depends(get_db),
    curr_user: int = Depends(oauth2.get_current_user),
):
    pt_query = db.query(model.Post).filter(model.Post.id == id)
    if pt_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} didnt found"
        )
    pt_query.update(post.model_dump())
    db.commit()
    db.refresh(pt_query.first())
    return pt_query.first()


@router.put("/{id}", response_model=schemas.Post)
def upadate_posts(
    id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    curr_user: int = Depends(oauth2.get_current_user),
):
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
    up_query = db.query(model.Post).filter(model.Post.id == id)
    up_post = up_query.first()
    if up_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    up_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return up_query.first()
