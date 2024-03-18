from app import schemas
from app.main import app
from fastapi.testclient import TestClient
from app.schemas import UserOut
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db, Base
import pytest


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.datebase_username}:{settings.datebase_passoword}@{settings.datebase_hostname}/{settings.datebase_name}_test"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost5432/fastapi_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Test_sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = Test_sessionLocal()
    try:
        yield db
    finally:
        db.close() 

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = Test_sessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
        app.dependency_overrides[get_db] = override_get_db
        yield TestClient(app)


def test_root(client,session):
    res = client.get("/")
    print(res.json().get("message"))
    assert res.json().get("message") == "Welcom to my API"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "ziva@gmail.com", "password": "Zika123"}
    )
    print(res.json())
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "ziva@gmail.com"
    assert res.status_code == 201
