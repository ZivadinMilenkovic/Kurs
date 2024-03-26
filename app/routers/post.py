from datetime import timedelta, datetime, timezone

import pytz
from .. import model, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from sqlalchemy import desc, func, or_, and_

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/all/story", response_model=List[schemas.Post])
def get_all_story(
    db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)
):
    posts = (
        db.query(model.Post)
        .filter(
            model.Post.expire > datetime.now(tz=timezone.utc),
            model.Post.type_of_post == schemas.TypeEnum.story,
        )
        .all()
    )
    return posts


@router.get("/all/posts", response_model=List[schemas.Post])
def get_all_posts(
    db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)
):
    posts = (
        db.query(model.Post)
        .filter(model.Post.type_of_post == schemas.TypeEnum.post)
        .all()
    )
    return posts


@router.get("/", response_model=List[schemas.Post])
def get_all_posts_and_story_of_spec_user(
    db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)
):
    posts = (
        db.query(model.Post)
        .filter(
            and_(
                model.Post.owner_id == curr_user.id,
                or_(
                    model.Post.expire > datetime.now(tz=timezone.utc),
                    model.Post.expire == None,
                ),
            )
        )
        .all()
    )
    return posts


@router.get("/all", response_model=List[schemas.Post])
def get_all_story_and_posts(
    db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)
):
    posts = (
        db.query(model.Post)
        .filter(
            or_(
                model.Post.expire > datetime.now(tz=timezone.utc),
                model.Post.expire == None,
            )
        )
        .all()
    )
    return posts


@router.get("/", response_model=List[schemas.Post])
def get_all_story(
    db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)
):
    posts = (
        db.query(model.Post)
        .filter(
            or_(
                model.Post.expire > datetime.now(tz=timezone.utc),
                model.Post.expire == None,
            )
        )
        .all()
    )
    return posts


@router.get("/query", response_model=List[schemas.PostOut])
def get_query(
    db: Session = Depends(get_db),
    curr_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    offset: int = 0,
    search: Optional[str] = "",
):

    results = (
        db.query(model.Post, func.count(model.Vote.post_id).label("votes"))
        .join(model.Vote, model.Vote.post_id == model.Post.id, isouter=True)
        .filter(
            and_(
                model.Post.title.contains(search),
                or_(
                    model.Post.expire > datetime.now(tz=timezone.utc),
                    model.Post.expire == None,
                ),
            )
        )
        .group_by(model.Post.id)
        .limit(limit)
        .offset(offset)
        .all()
    )
    return results


@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    curr_user: int = Depends(oauth2.get_current_user),
):
    x = datetime.now(tz=timezone.utc) + timedelta(minutes=1)

    if post.type_of_post == schemas.TypeEnum.story:
        post.expire = x

    new_post = model.Post(**post.model_dump(), owner_id=curr_user.id)
    # if new_post.type_of_post == 1:
    #     new_post.type_of_post = "post"
    # else:
    #     new_post.type_of_post = "story"
    #     new_post.expire = x
    print(datetime.now(pytz.utc))
    db.add(new_post)
    db.commit()

    return new_post


@router.get("/latest", response_model=schemas.Post)
def get_latest_post(
    db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)
):

    new_post = db.query(model.Post).order_by(desc("created_at")).first()
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    curr_user: int = Depends(oauth2.get_current_user),
):

    post = (
        db.query(model.Post, func.count(model.Vote.post_id).label("votes"))
        .join(model.Vote, model.Vote.post_id == model.Post.id, isouter=True)
        .filter(
            and_(
                model.Post.id == id,
                or_(
                    model.Post.expire > datetime.now(tz=timezone.utc),
                    model.Post.expire == None,
                ),
            )
        )
        .group_by(model.Post.id)
        .first()
    )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    if post.Post.owner_id != curr_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to performe requested auction",
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    curr_user: int = Depends(oauth2.get_current_user),
):

    post = db.query(model.Post).filter(
        and_(
            model.Post.id == id,
            or_(
                model.Post.expire > datetime.now(tz=timezone.utc),
                model.Post.expire == None,
            ),
        )
    )
    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    if post.first().owner_id != curr_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to performe requested auction",
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
    pt_query = db.query(model.Post).filter(
        and_(
            model.Post.id == id,
            or_(
                model.Post.expire > datetime.now(tz=timezone.utc),
                model.Post.expire == None,
            ),
        )
    )
    if pt_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} didnt found"
        )
    if pt_query.first().owner_id != curr_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to performe requested auction",
        )
    pt_query.update(post.model_dump())
    db.commit()
    db.refresh(pt_query.first())
    return pt_query.first()


@router.put("/{id}", response_model=schemas.Post)
def upadate_posts(
    id: int,
    post: schemas.PostBase,
    db: Session = Depends(get_db),
    curr_user: int = Depends(oauth2.get_current_user),
):
    up_query = db.query(model.Post).filter(
        and_(
            model.Post.id == id,
            or_(
                model.Post.expire > datetime.now(tz=timezone.utc),
                model.Post.expire == None,
            ),
        )
    )
    up_post = up_query.first()
    if up_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    if up_post.owner_id != curr_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to performe requested auction",
        )
    up_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return up_query.first()
