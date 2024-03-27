import pytest
from app import model, schemas


def test_get_all_posts_and_storys(authorized_client, test_posts):
    res = authorized_client.get("/posts/all")
    print(res.json())
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unathorized_user_get_all_his_posts_and_storys(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_athorized_user_get_all_his_posts_and_storys(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    assert res.status_code == 200


def test_user_get_all_posts_and_storys(client, test_posts):
    res = client.get("/posts/all")
    assert res.status_code == 401


def test_user_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/all/posts")
    assert res.status_code == 200


def test_user_get_all_story(authorized_client, test_posts):
    res = authorized_client.get("/posts/all/story")
    assert res.status_code == 200


def test_unathorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/all/posts")
    assert res.status_code == 401


def test_unathorized_user_get_all_story(client, test_posts):
    res = client.get("/posts/all/story")
    assert res.status_code == 401


def test_get_one_post_or_story(authorized_client, test_posts):
    res = authorized_client.get(
        f"/posts/{test_posts[0].id}",
    )
    print(res.json())
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert res.status_code == 200


def test_unauthorized_get_one_post_or_story(client, test_posts):
    res = client.get(
        f"/posts/{test_posts[2].id}",
    )
    print(res.json())
    assert res.status_code == 401


def test_get_one_post_or_story_that_not_exist(authorized_client, test_posts):
    res = authorized_client.get(
        "/posts/88888",
    )
    print(res.json())
    assert res.status_code == 404


@pytest.mark.parametrize(
    "title,content,type_of_post",
    [("ne_post", "TEST1", 1), ("ne_post2", "TEST2", 2), ("ne_post22", "TEST3", 1)],
)
def test_unauthorized_create_post(
    client, test_posts, session, title, content, type_of_post
):
    res = client.post(
        "/posts",
        json={"title": title, "content": content, "owner_id": test_posts[0].owner_id},
    )
    print(res.json())
    assert res.status_code == 401


@pytest.mark.parametrize(
    "title,content,type_of_post",
    [("ne_post", "TEST1", 1), ("ne_post2", "TEST2", 2), ("ne_post22", "TEST3", 1)],
)
def test_create_post(
    authorized_client, test_posts, session, title, content, type_of_post
):
    res = authorized_client.post(
        "/posts",
        json={
            "title": title,
            "content": content,
            "type_of_post": type_of_post,
            "owner_id": test_posts[0].owner_id,
        },
    )
    print(res.json())
    new_post = schemas.Post(**res.json())
    assert new_post.published == True
    assert new_post.title == title
    assert res.status_code == 201


def test_delete_one_post(authorized_client, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[0].id}",
    )
    # assert test_posts[0].id == None
    assert res.status_code == 204


def test_unauthorized_delete_one_post(client, test_posts):
    res = client.delete(
        f"/posts/{test_posts[0].id}",
    )
    assert res.status_code == 401


def test_delete_one_post_that_not_exist(authorized_client, test_posts):
    res = authorized_client.delete(
        f"/posts/88888",
    )
    # assert test_posts[0].id == None
    assert res.status_code == 404


def test_delete_one_post_not_owner(authorized_client, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[3].id}",
    )
    # assert test_posts[0].id == None
    assert res.status_code == 403


@pytest.mark.parametrize(
    "title,content", [("nwe", "TEST12"), ("new", "TEST22"), ("new2", "TEST32")]
)
def test_update_one_post(authorized_client, test_posts, title, content):
    res = authorized_client.put(
        f"/posts/{test_posts[0].id}",
        json={"title": title, "content": content, "owner_id": test_posts[0].owner_id},
    )
    update_post = schemas.Post(**res.json())
    assert update_post.title == title
    assert res.status_code == 200


def test_update_one_post_that_not_exist(authorized_client, test_posts):
    res = authorized_client.put(
        "/posts/8888",
        json={"title": "nwe", "content": "nwe", "owner_id": test_posts[0].owner_id},
    )
    assert res.status_code == 404


def test_update_one_post_that_not_exist(authorized_client, test_posts):
    res = authorized_client.put(
        f"/posts/{test_posts[3].id}",
        json={"title": "nwe", "content": "nwe", "owner_id": test_posts[0].owner_id},
    )
    assert res.status_code == 403


def test_unauthorized_update_one_post(client, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].id}",
        json={"title": "nwe", "content": "nwe", "owner_id": test_posts[0].owner_id},
    )
    assert res.status_code == 401


def test_post_patch_auth_user(authorized_client, test_posts):
    res = authorized_client.patch(
        f"/posts/{test_posts[0].id}", json={"title": "Ide gas"}
    )
    patch_post = schemas.Post(**res.json())
    assert patch_post.title == "Ide gas"


def test_post_patch_unauth_user(client, test_posts):
    res = client.patch(f"/posts/{test_posts[0].id}", json={"title": "Ide gas"})
    assert res.status_code == 401


def test_post_patch_non_exist(authorized_client, test_posts):
    res = authorized_client.patch("/posts/8888", json={"title": "Ide gas"})
    assert res.status_code == 404


def test_post_get_latest(authorized_client, test_posts):
    res = authorized_client.get("/posts/latest")
    latest_post = schemas.Post(**res.json())
    assert res.status_code == 200
