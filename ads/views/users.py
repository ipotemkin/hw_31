import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, CreateView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q
from rest_framework import serializers
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView

from skyvito.settings import TOTAL_ON_PAGE

from ads.models import User, UserModel, UserUpdateModel, USERO, LOCO, Location
from ads.utils import smart_json_response, patch_shortcut, pretty_json_response, update_from_dict, SmartPaginator


def user_decoder(data):
    """converts user object into a dict"""

    return {
        "id": data.id,
        "username": data.username,
        "first_name": data.first_name,
        "last_name": data.last_name,
        "role": data.role,
        "age": data.age,
        "locations": [loc.name for loc in data.locations.all()],
    }


def user_decoder_plus(data):
    """user+decoder + total_ads"""
    res = user_decoder(data)
    res["total_ads"] = data.total_ads
    return res


@method_decorator(csrf_exempt, name="dispatch")
class UserView(View):
    @staticmethod
    def get(request):  # GET ads/user/ # noqa
        """shows all users"""

        obj_list = USERO.all().prefetch_related("locations").annotate(
            total_ads=Count('ad__is_published', filter=Q(ad__is_published=True))
        ).order_by("username")

        # if paginated
        if page_number := request.GET.get("page"):
            paginator = SmartPaginator(obj_list, TOTAL_ON_PAGE, schema=user_decoder_plus)
            return pretty_json_response(paginator.get_page(page_number))

        # if not paginated
        return smart_json_response(user_decoder_plus, obj_list)
        # следующая строчка не работает, так как я не разобрался с many2many в pydantic
        # return smart_json_response(UserModel, USERO.all())

    @staticmethod
    def post(request):  # POST ads/user/
        """ads a new user"""

        user_data = json.loads(request.body)
        user = USERO.create(**UserModel.parse_obj(user_data).dict(exclude_unset=True))

        if locations := user_data.get("locations"):
            for loc in locations:
                loc_obj, _ = LOCO.get_or_create(name=loc)
                user.locations.add(loc_obj)
            user.full_clean()
            user.save()

        return pretty_json_response(user_decoder(user))


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):  # GET ads/user/pk/
        """shows a user"""

        return pretty_json_response(user_decoder(self.get_object()))
        # return smart_json_response(UserModel, self.get_object())


@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = User
    fields = ["username", "first_name", "last_name", "role", "age", "locations"]

    def post(self, request, *args, **kwargs):  # POST ads/user/create/
        super().post(request, *args, **kwargs)
        """ads a new user"""

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

        return pretty_json_response(user_decoder(user))


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(View):

    @staticmethod
    def patch(request, pk):  # PATCH ads/ad/pk/update/
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

        return pretty_json_response(user_decoder(user))

        # эти строчки можно будет использовать, когда я разберусь с pydantic
        # obj = patch_shortcut(request, pk, model=Ad, schema=AdUpdateModel)
        # return smart_json_response(AdModel, obj)


@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):  # DELETE ads/user/pk/delete/
        """deletes a user"""

        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)


class LocSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        # fields = "__all__"
        fields = ["name"]


class UserSerializer(serializers.ModelSerializer):
    # locations = LocSerializer(many=True)
    locations = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = User
        fields = "__all__"
        # exclude = ["locations"]


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    # locations = LocSerializer(many=True)
    locations = serializers.SlugRelatedField(
        required=False,
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = User
        fields = "__all__"
        # exclude = ["id"]  # , "locations"]

    # def is_valid(self, raise_exception=False):
    #     self._locations = self.initial_data.pop("locations")
    #     return super().is_valid(raise_exception=raise_exception)

    def _create_update_locations(self, user):
        if _locations := self.initial_data.get("locations"):
            user.locations.set([])
            for loc in _locations:
                loc_obj, _ = LOCO.get_or_create(name=loc)
                user.locations.add(loc_obj)
            user.save()
        return user

    def create(self, validated_data):
        user = super().create(validated_data)
        return self._create_update_locations(user)

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        return self._create_update_locations(user)


class UserListAPIView(ListAPIView):
    queryset = USERO.all()
    serializer_class = UserSerializer


class UserAPIView(RetrieveAPIView):
    queryset = USERO.all()
    serializer_class = UserSerializer


class UserCreateAPIView(CreateAPIView):
    queryset = USERO.all()
    serializer_class = UserCreateUpdateSerializer


class UserUpdateAPIView(UpdateAPIView):
    queryset = USERO.all()
    serializer_class = UserCreateUpdateSerializer


class UserDeleteAPIView(DestroyAPIView):
    queryset = USERO.all()
    serializer_class = UserSerializer
