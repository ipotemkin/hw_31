import pytest

from ads.models import ADO, CATO, USERO

new_ad = {
        "name": "Testing advertisement",
        "price": 1000,
}

auth_cat_id = {
    "author_id": 1,
    "category_id": 1
}

auth_cat = {
    "author": 1,
    "category": 1
}

new_ad_ext = {
    "is_published": False,
    "description": None,
    "image": None,
    "id": 1
}

# new_ad_with_auth_cat_id = {**new_ad, **auth_cat_id, **new_ad_ext}
new_ad_with_auth_cat = {**new_ad, **auth_cat, **new_ad_ext}

expected_ad_list_response = {
    "count": 1,
    "next": None,
    "previous": None,
    "results": [new_ad_with_auth_cat]
}

user_d = {"username": "Test user", "password": "password"}
cat_d = {"name": "Goods"}


@pytest.mark.django_db
def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


@pytest.mark.django_db
def test_ad_get_all(client):
    CATO.create(**cat_d)
    USERO.create(**user_d)
    ADO.create(**new_ad, author_id=1, category_id=1)
    response = client.get("/ads/")
    assert response.status_code == 200
    assert response.json() == expected_ad_list_response


@pytest.mark.django_db
def test_ad_get_one(client, user_token):
    CATO.create(**cat_d)
    USERO.create(**user_d)
    ADO.create(**new_ad, author_id=2, category_id=2)
    response = client.get(
        "/ads/2/",
        HTTP_AUTHORIZATION="Bearer " + user_token

    )
    assert response.status_code == 200
    new_ad_with_auth_cat["author"] = new_ad_with_auth_cat["category"] = new_ad_with_auth_cat["id"] = 2
    assert response.json() == new_ad_with_auth_cat


@pytest.mark.django_db
def test_ad_create(client):
    CATO.create(**cat_d)
    USERO.create(**user_d)
    data = dict(**new_ad, author=4, category=3)
    response = client.post(
        "/ads/",
        data,
        content_type="application/json"
    )
    assert response.status_code == 201
    new_ad_with_auth_cat["author"] = 4
    new_ad_with_auth_cat["category"] = new_ad_with_auth_cat["id"] = 3
    assert response.json() == new_ad_with_auth_cat
    assert response.json() == new_ad_with_auth_cat

