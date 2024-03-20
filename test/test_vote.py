import pytest
from app import model

@pytest.fixture()
def test_vote(session,test_posts,test_user):
    new_vote=model.Vote(post_id=test_posts[3].id,user_id=test_user['id'])
    session.add(new_vote)
    session.commit()

#only work if you try to like a post
def test_create_vote(authorized_client,test_posts):
    res = authorized_client.post("/vote/",json={
    "post_id": test_posts[3].id,
    "dir":1 })
    print(res.json())
    assert res.status_code==201

def test_create_vote_on_his_post(authorized_client,test_posts):
    res = authorized_client.post("/vote/",json={
    "post_id": test_posts[1].id,
    "dir":1 })
    print(res.json())
    assert res.status_code==409

def test_vote_twice_post(authorized_client,test_posts,test_vote):
    res = authorized_client.post("/vote/",json={"post_id":test_posts[3].id,"dir":1})
    assert res.status_code==409

def test_delete_vote(authorized_client,test_posts,test_vote):
    res = authorized_client.post("/vote/",json={"post_id":test_posts[3].id,"dir":0})
    assert res.status_code==201

def test_delete_vote_non_exist(authorized_client,test_posts):
    res = authorized_client.post("/vote/",json={"post_id":88888,"dir":0})
    assert res.status_code==404

def test_like_vote_non_exist(authorized_client,test_posts):
    res = authorized_client.post("/vote/",json={"post_id":88888,"dir":1})
    assert res.status_code==404

def test_vote_unauthorized_user(client,test_posts):
    res = client.post("/vote/",json={"post_id":88888,"dir":1})
    assert res.status_code==401

def test_delete_vote_unauthorized_user(client,test_posts):
    res = client.post("/vote/",json={"post_id":88888,"dir":0})
    assert res.status_code==401