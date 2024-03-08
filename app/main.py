from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


# class Post extends BaseModel


class Post(BaseModel):
    title: str
    content: str
    publisshed: bool = True
    rating: Optional[int] = None


# conn=psycopg2.connect(host,database,user, password)
# psycopg2 retrund only value of field but doesnt retrun name of field
# RealDictCursor returns name of field
# we use cursor to execute sql statemnts
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


# full optional field that use int value, but if user type str vaule field will be empty
# when we use the path parameter id will always be a string and that's why we have to change it to int
# we have to ensure that it must be an integer and automatically converts it, if some early id that is not a string is entered, Greek is output
# default value (optional field) if the user does not enter data, this will be the value of that field
# complete optional field that receives an int but if the user does not enter it will be none (empty)


# def getone(id: int):
#     for post in my_posts:
#         if post['id']==id:
#             return post


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


# decorator, turns the function into a path, i.e. gives it a path
# this is the default path, if we put /login it means that this function will start if
# user goes to that domain
# how to start the server unicorn filename:pathname/root
# api uses json
# every time we make a change it is necessary to restart the server
# ctrl+c to stop the server and unicorn:app again
# that's why we use unicorn:app --reload
# only when we are in the development env we write reload
# with fetchall/fetchone(many or one post) we can use our sql


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


# we cannot put more decorators on one path
# but when it gets to the first one it stops looking at that path)
# We use #POST to create the data, GET to retrieve the data
# body takes all the fields from the body and converts it into a python dictionary (dict dictionary) which is stored in the payload
# def funname(methodname: dict:Body(...))
# in order to change the default status code , it is necessary to put the status code in decoration


@app.post("/posts", status_code=status.HTTP_201_CREATED)


# check if the data is valid
# store it in the paydeitc model with this, so we use dict to turn it into a dictionary
# this is the way we insert/post data and we need to commit data to save it


def create_posts(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """,
        (post.title, post.content, post.publisshed),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/latest")
def get_latest_post():
    
    cursor.execute(
        """SELECT * 
FROM posts 
WHERE created_at=(
    SELECT max(created_at) FROM posts
    )""")
    new_post = cursor.fetchone()
    return {"detail": new_post}


# in order to add something to the postman, enter the body and row and put the type json (post request)
# need to use '' for file names
# in order to ensure that we get validated data, we must create a scheme that ensures
# we use pydentic, it can be used outside fastapi
# crud (create,read,upadate,delete(post,get,put/patch,delete) for get,put,delete can/must be cortist eg: /posts/{id})
# id is the path parameter of the specified post whose data we want to get
# if the user enters an id that does not exist, it is necessary to predict this by giving him a 404 error code
# that's why we have to import response
# 404 can be put, but the status containing all http responses can be immortized
# respnse.status_code=status.HTTP_404_NOT_FOUND
# return{"message": f"post with id {id} was not found"}
# id need to be string


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    conn.commit()
    return {"data": post}


# post=getone(id)
# if not post:
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    post = cursor.fetchone()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    conn.commit()
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
def upadate_posts(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s,content = %s WHERE id = %s RETURNING *""",
        (
            post.title,
            post.content,
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



# in order to see the documentation, just type docs in the url and fastapi has a built-in swag that opens
# redoc can also be used


# postgras can create instance of detabase for each app indenpednetly
