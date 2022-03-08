from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import USERO, LOCO
from ads.permissions import IsAdmin, IsSelf
from ads.serializers import LocSerializer, UserSerializer, UserCreateUpdateSerializer


class LocAPIViewSet(ModelViewSet):
    """locations' views"""

    queryset = LOCO.all()
    serializer_class = LocSerializer


class UserViewSet(ModelViewSet):
    """users' views"""

    queryset = USERO.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        """Добавлены функции для поиска по названию категории и сортировка"""

        if search := request.GET.getlist('search'):  # for searching in field name
            query = None
            for s in search:
                query = query | Q(username__icontains=s) if query else Q(username__icontains=s)
            self.queryset = self.queryset.filter(query)

        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """creates a user and adds/creates his location(s)"""

        self.serializer_class = UserCreateUpdateSerializer
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """partially updates a user and adds/creates his location(s)"""

        self.serializer_class = UserCreateUpdateSerializer
        return super().update(request, *args, **kwargs)

    def get_permissions(self):
        """sets permissions for users' views"""

        permissions = []
        if self.action in ("update", "partial_update", "destroy"):
            permissions = (IsAuthenticated & (IsAdmin | IsSelf),)
        return [permission() for permission in permissions]
