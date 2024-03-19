from .. import model, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UsersBase, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = model.User(**user.model_dump())
    if (
        db.query(model.User.email).filter(model.User.email == new_user.email).first()
        != None
    ):
        raise HTTPException(status_code=status.HTTP_226_IM_USED)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    user = db.query(model.User).all()
    db.commit()
    return user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User who have id of {id}, does not existe",
        )
    db.commit()
    return user
