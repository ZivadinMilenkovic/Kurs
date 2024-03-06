from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
app=FastAPI()
# klasa Post nasledjuje BaseModel
#postavljamo vrstu podataka koji treba da se unese
#pravimo model
class Post(BaseModel):
    title: str
    content: str
    publisshed: bool = True #default value (opciono polje)ako korisnik ne unese podatke ovo ce biti vrednost tog polja
    rating: Optional[int]= None #potpuna opciono polje koje prima int ali ako ga korisnik ne unese onda ce biti none(prazno)
# kad koristimo path parametar id ce uvek biti string i zato moramo da ga promenimu int
# moramo da obezbedimo da mora da bude integer i automacki ga konvetuje, ako se unese neki ranom id koji nije string izlazi grska
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

@app.get('/') #decorator,pretvara funkciju u path tj daje joj putanju
# ovo je default path, ako stavimo /login znaci da ce se ova funkcia pokrenuti ako 
# korisnik ode na taj domen
def hello(): #funkcija
    return{"message":"Welcom to my API"}
# kako mi bi pokreniuli server unicorn filename:pathname/root
# api koristi json
#svaki put kada napravimo promenu potrebnoje restartovati sever
#ctrl+c kako bi se server zaustavio i ponovo unicorn:app
#zbog toga koristimo unicorn:app --reload
#samo kad smo u development env pisemo reload
@app.get("/posts")
def get_posts():
    return{"data":my_posts}
# nemozemo staviti vise dekoratora na jedan path(mozemo 
# ali kada stigne do prvog prestaje da gleda ta path)
#post man koristimo za manipulacija http reqestovima
#POST koristimo da kreiramo podatake,GET kako bi pokupili podatke

#body uzima sva polja iz bodyja i pretvara u pyton dictionary(dict dictionary) koji se cuva u payloadu
#def funname(metodname: dict:Body(...))
# kako bi promenili default status kod prmneli potrebno je staviti status kod u decoration
@app.post("/posts",status_code=status.HTTP_201_CREATED)
# provera da li su podaci validni
# ovim ga cuvamo u paydeitc modelu zato koristimo dict da ga prtvorimo u dictionary
def create_posts(post:Post):
    post_dict=post.dict()
    post_dict['id']=randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data":post_dict}

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return{"detail": post}

# kako bi dodali nesto u postmanu udjemo u body i row i stavimo vrstu json(post request)
#potrebno je koristiti '' za imena filodva
#kako bi obezbedili da dobijemo validene podatke moramo napraviti shamu koja obezbedjuje
#koristimo pydentic, moze se koristiti van fastapi
#crud (create,read,upadate,delete(post,get,put/patch,delete) za get,put,delete moze/mora da se kortist pr: /posts/{id})
# id je path paramtar odrednjeni post cije podatke zelimo da dobijemo
#ako korisnik u unese niki id koji nepostoji potrebno je to predvideti tako sto cemo mu izbaciti eror kod 404
#zbog toga moramo da iportujemo response
@app.get("/posts/{id}")
def get_post(id: int,response: Response ):
    post=getone(id)
    if not post:
        # moze se staviti 404 ali se moze imortovati status koji sadrzi sve http response
        # respnse.status_code=status.HTTP_404_NOT_FOUND
        # return{"message": f"post with id {id} was not found"}
        # moze i ovako
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
    return{"data":post}

# kada radimo delite ne treba da se vracti nikakve podatke
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # post=getone(id)
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    index=get_index_of_del_item()
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

#kako bi videli dokumentaciju samo u url-u ukucamo docs i fastapi ima ugradje swag koje se otvara
#takodje se moze koristiti redoc