import pytest

from ads.models import SELO
# from tests.factory import AdFactory, UserFactory
from ads.serializers import AdSerializer


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


@pytest.mark.django_db
def test_selection_get_all(client, ad, user):
    selection = SELO.create(**{
        "name": "test collection",
        "owner": user,
        # "items": [1],
        "id": 1
    })
    selection.items.add(ad.id)

    expected_response = {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [{
            "name": "test collection",
                    # "owner": user.id,
                    # "items": [ad.id],
                    "id": 1
        }]
    }

    response = client.get(
        "/selections/",
    )

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_selection_get_one(client, ad, user):
    selection = SELO.create(**{
        "name": "test collection",
        "owner": user,
        # "items": [1],
        "id": 2
    })
    selection.items.add(ad.id)

    expected_response = {
        "name": "test collection",
        "owner": user.id,
        "items": [AdSerializer(ad).data],
        "id": 2
        }

    response = client.get(
        "/selections/2/",
    )

    assert response.status_code == 200
    assert response.data == expected_response


# @pytest.mark.django_db
# def test_selection_update(client, ad, user):
#     selection = SELO.create(**{
#         "name": "test collection",
#         "owner": user,
#         # "items": [1],
#         "id": 2
#     })
#     selection.items.add(ad.id)
#
#     expected_response = {
#         "name": "test collection",
#         "owner": user.id,
#         "items": [AdSerializer(ad).data],
#         "id": 2
#         }
#
#     response = client.get(
#         "/selections/2/",
#     )
#
#     assert response.status_code == 200
#     assert response.data == expected_response
