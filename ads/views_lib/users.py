import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, CreateView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Sum, Q

from skyvito.settings import TOTAL_ON_PAGE

from ads.models import User, UserModel, UserUpdateModel, USERO, LOCO
from ads.utils import smart_json_response, patch_shortcut, pretty_json_response, update_from_dict, SmartPaginator


def user_encoder(data):
    """converts user object into a dict"""

    return {
        "id": data.id,
        "username": data.username,
        "first_name": data.first_name,
        "last_name": data.last_name,
        "role": data.role,
        "age": data.age,
        "locations": [loc.name for loc in data.locations.all()],
        # "total_ads": data.total_ads
        # "locations": [{"name": loc.name} for loc in data.locations.all()]
    }


def user_encoder_plus(data):
    """converts user object into a dict"""
    res = user_encoder(data)
    res["total_ads"] = data.total_ads
    return res


@method_decorator(csrf_exempt, name="dispatch")
class UserView(View):
    @staticmethod
    def get(request):  # GET ads/user/ # noqa
        """shows all users"""

        obj_list = USERO.all().prefetch_related("locations").annotate(
            total_ads=Count('ad__is_published', filter=Q(ad__is_published=True))
        )
        # .order_by("-total_ads")

        # if paginated
        if page_number := request.GET.get("page"):
            paginator = SmartPaginator(obj_list, TOTAL_ON_PAGE, schema=user_encoder_plus)
            return pretty_json_response(paginator.get_page(page_number))

        # if not paginated
        return smart_json_response(user_encoder_plus, obj_list)
        # следующая строчка не работает, так как я не разобрался с many2many в pydantic
        # return smart_json_response(UserModel, USERO.all())

    @staticmethod
    def post(request):  # POST ads/user/pk
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


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):  # ads/user/pk/
        """shows a user"""

        return pretty_json_response(user_encoder(self.get_object()))
        # return smart_json_response(UserModel, self.get_object())


@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = User
    fields = ["username", "first_name", "last_name", "role", "age", "locations"]

    def post(self, request, *args, **kwargs):  # ads/user/create/
        super().post(request, *args, **kwargs)
        """ads a new user"""

        # ad = ADO.create(**AdModel.parse_raw(request.body).dict())
        # return smart_json_response(AdModel, ad)

        user_data = json.loads(request.body)

        user = User()
        update_from_dict(user_data, user)
        user.full_clean()
        user.save()

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
    def patch(request, pk):  # ads/ad/pk/update/
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
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):  # ads/user/pk/delete/
        """deletes a user"""

        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)
