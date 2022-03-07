from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ValidationError
from rest_framework import serializers

from ads.models import User, Ad, Cat, Location, LOCO, Selection


def check_false(value: bool):
    if value:
        raise ValidationError(
            'Needed False',
            params={'value': value},
        )


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = "__all__"

    def create(self, validated_data):
        if value := validated_data.get("is_published", False):
            raise ValidationError('is_published should be False', params={'value': value})
        return super().create(validated_data)


class AdCreateSerializer(AdSerializer):
    is_published = serializers.BooleanField(required=False, validators=[check_false])


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = "__all__"


class LocSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["name"]


class UserSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = User
        fields = "__all__"


def check_age(value: datetime.date):
    delta = relativedelta(datetime.utcnow().date(), value)
    if delta.years < 9:
        raise ValidationError(
            'Age should be more than 9 years',
            params={'value': value},
        )


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(validators=[check_age])
    locations = serializers.SlugRelatedField(
        required=False,
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = User
        fields = "__all__"

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

    def save(self):
        user = super().save()
        user.set_password(user.password)
        user.save()
        return user


# class UserCreateSerializer(UserCreateUpdateBaseSerializer):
#     birth_date = serializers.DateField(validators=[is_required_age])
#
#
# class UserUpdateSerializer(UserCreateUpdateBaseSerializer):
#     birth_date = serializers.DateField(validators=[is_required_age])


class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = "__all__"


class SelectionDetailSerializer(SelectionSerializer):
    items = AdSerializer(many=True)


class SelectionListSerializer(SelectionSerializer):
    class Meta(SelectionSerializer.Meta):
        fields = ["id", "name"]
