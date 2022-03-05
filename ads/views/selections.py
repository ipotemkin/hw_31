from rest_framework.generics import (
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListAPIView,
    CreateAPIView
)

from rest_framework.permissions import IsAuthenticated
from ads.models import SELO
from ads.permissions import SelectionUpdateDeletePermission
from ads.serializers import SelectionSerializer, SelectionDetailSerializer, SelectionListSerializer


class SelectionAPIView(RetrieveAPIView):
    queryset = SELO.all()
    serializer_class = SelectionDetailSerializer


class SelectionListAPIView(ListAPIView):
    queryset = SELO.all()
    serializer_class = SelectionListSerializer


class SelectionCreateAPIView(CreateAPIView):
    queryset = SELO.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.data['owner'] = request.user.id
        return super().post(request, *args, **kwargs)


class SelectionUpdateAPIView(UpdateAPIView):
    queryset = SELO.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated, SelectionUpdateDeletePermission]


class SelectionDeleteAPIView(DestroyAPIView):
    queryset = SELO.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated, SelectionUpdateDeletePermission]
