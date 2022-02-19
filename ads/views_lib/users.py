import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, CreateView, DeleteView
from django.views.decorators.csrf import csrf_exempt

from skyvito.settings import TOTAL_ON_PAGE
from ads.models import User, UserModel, UserUpdateModel, USERO, LOCO
from ads.utils import smart_json_response, patch_shortcut, pretty_json_response, SmartPaginator, update_from_dict


def user_encoder(data):
    """converts user object into a dict"""

    return {
        "id": data.id,
        "username": data.username,
        "first_name": data.first_name,
        "last_name": data.last_name,
        "role": data.role,
        "age": data.age,
        "locations": [loc.name for loc in data.locations.all()]
        # "locations": [{"name": loc.name} for loc in data.locations.all()]
    }


@method_decorator(csrf_exempt, name="dispatch")
class UserView(View):
    @staticmethod
    def get(request):  # noqa
        """shows all users"""

        return pretty_json_response([
            user_encoder(user) for user in USERO.all()
        ])
        # return smart_json_response(UserModel, USERO.all())

    @staticmethod
    def post(request):  # ads/ad/pk
        """ads a new user"""

        # ad = ADO.create(**AdModel.parse_raw(request.body).dict())
        # return smart_json_response(AdModel, ad)

        user_data = json.loads(request.body)

        # user = User(**UserModel.parse_obj(user_data).dict(exclude_unset=True))
        user = USERO.create(**UserModel.parse_obj(user_data).dict(exclude_unset=True))

        if locations := user_data.get("locations"):
            for loc in locations:
                loc_obj, _ = LOCO.get_or_create(name=loc)
                user.locations.add(loc_obj)
            user.full_clean()
            user.save()

        return pretty_json_response(user_encoder(user))


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(View):

    @staticmethod
    def patch(request, pk):  # ads/ad/pk/update
        """updates a user"""

        # обновляем все поля, кроме locations (я не смог это реализовать в pydantic – эти поля будем писать отдельно)
        user = patch_shortcut(request, pk, model=User, schema=UserUpdateModel)

        # обновляем поля locations, если они есть в payload
        if locations := json.loads(request.body).get("locations"):
            user.locations.set([])  # обнуляем locations
            for loc in locations:
                loc_obj, _ = LOCO.get_or_create(name=loc)
                user.locations.add(loc_obj)
            user.full_clean()
            user.save()

        return pretty_json_response(user_encoder(user))

        # эти строчки можно будет использовать, когда я разберусь с pydantic
        # obj = patch_shortcut(request, pk, model=Ad, schema=AdUpdateModel)
        # return smart_json_response(AdModel, obj)


@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = User
    fields = ["username", "first_name", "last_name", "role", "age", "locations"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        """ads a new user"""

        # ad = ADO.create(**AdModel.parse_raw(request.body).dict())
        # return smart_json_response(AdModel, ad)

        user_data = json.loads(request.body)

        user = User()

        update_from_dict(user_data, user)
        user.full_clean()
        user.save()

        for loc in user_data["locations"]:
            loc_obj, _ = LOCO.get_or_create(name=loc)
            user.locations.add(loc_obj)

        user.full_clean()
        user.save()

        return pretty_json_response(user_encoder(user))


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs) -> JsonResponse:
        """shows a user"""

        return pretty_json_response(user_encoder(self.get_object()))
        # return smart_json_response(UserModel, self.get_object())


@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        """deletes a user"""

        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)
