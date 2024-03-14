from fastapi import FastAPI
from . import model
from .database import engine, SessionLocal
from .routers import user, post, auth, vote

# makes new table that we define in model

model.Base.metadata.create_all(bind=engine)

# declaring type of crypting algorithm

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def hello():
    return {"message": "Welcom to my API"}
