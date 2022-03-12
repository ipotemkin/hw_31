import pytest


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
