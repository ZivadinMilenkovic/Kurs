import pytest
from app import schemas
import pytest
from jose import jwt
from app.config import settings


def test_root(client):
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


def test_login_user(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_user = schemas.Token(**res.json())
    payload = jwt.decode(
        login_user.access_token, settings.secret_key, algorithms=[settings.algorihm]
    )
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_user.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email,password,status",
    [
        ("wrong", "wrong", 403),
        ("ziva@gmail.com", "jhsjfa", 403),
        (";jfgdj;", "Zika123", 403),
        (None, "Zika123", 422),
        ("ziva@gmail.com", None, 422),
    ],
)
def test_incorect_login(client, email, password, status):
    res = client.put("/login", data={"username": email, "password": password})

    assert res.status_code == status
    # assert res.json().get('detail')=="Invalid Credentials"