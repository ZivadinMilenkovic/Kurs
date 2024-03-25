import datetime
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, text, ForeignKey,DateTime
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    type_of_post = Column(Integer, nullable=False,server_default="1")
    expire = Column(TIMESTAMP(timezone=True), nullable="True")
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False,default=datetime.datetime.utcnow()
    )
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Vote(Base):
    __tablename__ = "votes"

    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
