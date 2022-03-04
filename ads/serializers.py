from rest_framework import serializers

from ads.models import User, Ad


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["pk", "username"]
        # fields = "__all__"


class AdSerializer(serializers.ModelSerializer):
    # author = AuthorSerializer()

    class Meta:
        model = Ad
        fields = "__all__"
