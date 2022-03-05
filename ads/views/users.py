from django.db.models import Q
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

    def list(self, request, *args, **kwargs):
        """Добавлены функции для поиска по названию категории и сортировка"""

        if search := request.GET.getlist('search'):  # for searching in field name
            query = None
            for s in search:
                query = query | Q(username__icontains=s) if query else Q(username__icontains=s)
            self.queryset = self.queryset.filter(query)

        # if order := request.GET.get('ordering'):  # for sorting records retrieved
        #     self.queryset = self.queryset.order_by(order)

        return super().list(request, *args, **kwargs)


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
