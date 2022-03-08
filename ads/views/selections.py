from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import SELO
from ads.permissions import IsOwner
from ads.serializers import SelectionSerializer, SelectionDetailSerializer, SelectionListSerializer


class SelectionViewSet(ModelViewSet):
    queryset = SELO.all()
    serializer_class = SelectionSerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = SelectionDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.serializer_class = SelectionListSerializer
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request.data["owner"] = request.user.id
        return super().create(request, *args, **kwargs)

    def get_permissions(self):
        permissions = []
        if self.action == "create":
            permissions = (IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            permissions = (IsAuthenticated & IsOwner,)
        return [permission() for permission in permissions]
