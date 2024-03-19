from app import model, schemas
from app.main import app
from fastapi.testclient import TestClient
from app.schemas import UserOut
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db, Base
from app.oauth2 import create_access_token
import pytest

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.datebase_username}:{settings.datebase_passoword}@{settings.datebase_hostname}/{settings.datebase_name}_test"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost5432/fastapi_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Test_sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = Test_sessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email": "ziva@gmail.com", "password": "Zika123"}
    res = client.post("/users/",json=user_data)

    assert res.status_code == 201
    new_user=res.json()
    new_user['password']=user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "ziva2@gmail.com", "password": "Zika123"}
    res = client.post("/users/",json=user_data)

    assert res.status_code == 201
    new_user=res.json()
    new_user['password']=user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client,token):
    client.headers= {**client.headers, "authorization": f"Bearer {token}"}
    return client
    
# Pravi se postovi za testiranje i automatski se prave i test korisnici
@pytest.fixture
def test_posts(test_user, session,test_user2):
    posts_data = [
        {
            "title": "first title",
            "content": "firsto content",
            "owner_id": test_user['id'],
        },
        {
            "title": "second title",
            "content": "second content",
            "owner_id": test_user['id'],
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": test_user2['id'],
        },
        {
            "title": "thirdd title",
            "content": "thirdd content",
            "owner_id": test_user2['id'],
        }
    ]

    def create_post_model(post):
        return model.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()
    posts = session.query(model.Post).all()

    return posts