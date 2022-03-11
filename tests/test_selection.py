import pytest

# from ads.models import ADO, CATO, USERO

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


# @pytest.mark.django_db
# def test_selection_create(client, user_token):
#     expected_response = {
#         "name": "test collection",
#         "owner": 5,
#         "items": [4],
#         "id": 1
#     }
#
#     data = {
#         "name": "test collection",
#         "owner": 5,
#         "items": [4]
#     }
#
#     CATO.create(**cat_d)
#     USERO.create(**user_d)
#     ADO.create(**new_ad, author_id=5, category_id=4)
#
#     response = client.post(
#         "/selections/",
#         data,
#         content_type="application/json",
#         HTTP_AUTHORIZATION="Bearer " + user_token
#     )
#
#     assert response.status_code == 201
#     assert response.data == expected_response


@pytest.mark.django_db
def test_selection_create(client, user_token, ad):
    token, user_id = user_token

    expected_response = {
        "name": "test collection",
        "owner": user_id,
        "items": [ad.id],
        "id": 1
    }

    data = {
        "name": "test collection",
        "items": [ad.id]
    }

    response = client.post(
        "/selections/",
        data,
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + token
    )

    assert response.status_code == 201
    assert response.data == expected_response
