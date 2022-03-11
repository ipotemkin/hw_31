import pytest


@pytest.fixture()
@pytest.mark.django_db
def user_token(client, django_user_model):
    username = "james"
    password = "james"

    user = django_user_model.objects.create_user(
        username=username,
        password=password
    )

    response = client.post(
        "/users/token/",
        {"username": username, "password": password},
        format="json"
    )

    return response.data["access"], user.id
