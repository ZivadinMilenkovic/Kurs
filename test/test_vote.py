
def test_create_vote(authorized_client,test_posts):
    res = authorized_client.post("/vote/",json={
    "post_id": test_posts[3].id,
    "dir":1 })
    print(res.json())
    assert res.status_code==201