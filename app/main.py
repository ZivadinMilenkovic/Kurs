from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
app=FastAPI()


# class Post extends BaseModel


class Post(BaseModel):
    title: str
    content: str
    publisshed: bool = True 
    rating: Optional[int]= None 


# full optional field that use int value, but if user type str vaule field will be empty 
# when we use the path parameter id will always be a string and that's why we have to change it to int
# we have to ensure that it must be an integer and automatically converts it, if some early id that is not a string is entered, Greek is output
# default value (optional field) if the user does not enter data, this will be the value of that field
# complete optional field that receives an int but if the user does not enter it then it will be none (empty)


def getone(id: int):
    for post in my_posts:
        if post['id']==id:
            return post
def get_index_of_del_item(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i
        

my_posts=[{"title":"post 1","content":"content of post 1","id": 1},
          {"title":"post 2","content":"content of post 2","id": 2}]


@app.get('/') 
def hello():
    return{"message":"Welcom to my API"}


#decorator, turns the function into a path, i.e. gives it a path
# this is the default path, if we put /login it means that this function will start if
# user goes to that domain
# how to start the server unicorn filename:pathname/root
# api uses json
# every time we make a change it is necessary to restart the server
#ctrl+c to stop the server and unicorn:app again
#that's why we use unicorn:app --reload
#only when we are in the development env we write reload


@app.get("/posts")
def get_posts():
    return{"data":my_posts}


# we cannot put more decorators on one path
# but when it gets to the first one it stops looking at that path)
# We use #post man to manipulate http requests
# We use #POST to create the data, GET to retrieve the data
# body takes all the fields from the body and converts it into a python dictionary (dict dictionary) which is stored in the payload
# def funname(methodname: dict:Body(...))
# in order to change the default status code prmneli, it is necessary to put the status code in decoration


@app.post("/posts",status_code=status.HTTP_201_CREATED)


# check if the data is valid
# we
#  store it in the paydeitc model with this, so we use dict to turn it into a dictionary


def create_posts(post:Post):
    post_dict=post.dict()
    post_dict['id']=randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data":post_dict}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return{"detail": post}


# in order to add something to the postman, enter the body and row and put the type json (post request)
#need to use '' for file names
#in order to ensure that we get validated data, we must create a scheme that ensures
#we use pydentic, it can be used outside fastapi
#crud (create,read,upadate,delete(post,get,put/patch,delete) for get,put,delete can/must be cortist eg: /posts/{id})
# id is the path parameter of the specified post whose data we want to get
#if the user enters an id that does not exist, it is necessary to predict this by giving him a 404 error code
#that's why we have to import response
# 404 can be put, but the status containing all http responses can be immortized
# respnse.status_code=status.HTTP_404_NOT_FOUND
# return{"message": f"post with id {id} was not found"}
# it can be like this


@app.get("/posts/{id}")
def get_post(id: int,response: Response ):
    post=getone(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
    return{"data":post}


# kada radimo delite ne treba da se vracti nikakve podatke
# post=getone(id)
# if not post:
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index=get_index_of_del_item(id)
    if index(id) == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
    my_posts.pop(index(id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def upadate_posts(id:int,post:Post): 
    index=get_index_of_del_item(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
    post_dict=post.dict()
    post_dict['id']=id
    my_posts[index] = post_dict
    return{"data": my_posts}


# in order to see the documentation, just type docs in the url and fastapi has a built-in swag that opens
# redoc can also be used