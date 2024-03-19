from .. import model, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import desc

router = APIRouter(prefix="/vote", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(
    vote: schemas.Vote,
    curr_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    
    post_owner=db.query(model.Post).filter(model.Post.id==vote.post_id, model.Post.owner_id==curr_user.id).first()
    print(post_owner)
    post = db.query(model.Post).filter(model.Post.id == vote.post_id).first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post was not found",
        )

    post_query = db.query(model.Vote).filter(
        model.Vote.post_id == vote.post_id, model.Vote.user_id == curr_user.id
    )
    found_post = post_query.first()
    if vote.dir == 1:
        if found_post != None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {curr_user.id} already vote on post {vote.post_id}",
            )
        post_owner=db.query(model.Post).filter(model.Post.id==vote.post_id, model.Post.owner_id==curr_user.id).first()
        if post_owner != None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"This is your post",
            )
        new_vote = model.Vote(post_id=vote.post_id, user_id=curr_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": "You vote"}
    else:
        if found_post == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {curr_user.id} not vote on post {vote.post_id}",
            )
        post_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "You delete a vote"}
