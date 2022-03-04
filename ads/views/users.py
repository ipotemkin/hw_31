from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import USERO, LOCO
from ads.serializers import LocSerializer, UserSerializer, UserCreateUpdateSerializer


class LocAPIViewSet(ModelViewSet):
    queryset = LOCO.all()
    serializer_class = LocSerializer


class UserListAPIView(ListAPIView):
    queryset = USERO.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]


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
