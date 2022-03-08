# from rest_framework.generics import (
#     RetrieveAPIView,
#     UpdateAPIView,
#     DestroyAPIView,
#     ListAPIView,
#     CreateAPIView
# )

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import SELO
from ads.permissions import IsOwner
from ads.serializers import SelectionSerializer, SelectionDetailSerializer, SelectionListSerializer
from ads.validators import method_permission_classes

# class SelectionAPIView(RetrieveAPIView):
#     queryset = SELO.all()
#     serializer_class = SelectionDetailSerializer


# class SelectionListAPIView(ListAPIView):
#     queryset = SELO.all()
#     serializer_class = SelectionListSerializer


# class SelectionCreateAPIView(CreateAPIView):
#     queryset = SELO.all()
#     serializer_class = SelectionSerializer
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, *args, **kwargs):
#         request.data['owner'] = request.user.id
#         return super().post(request, *args, **kwargs)


# class SelectionUpdateAPIView(UpdateAPIView):
#     queryset = SELO.all()
#     serializer_class = SelectionSerializer
#     permission_classes = [IsAuthenticated, IsOwner]
#
#
# class SelectionDeleteAPIView(DestroyAPIView):
#     queryset = SELO.all()
#     serializer_class = SelectionSerializer
#     permission_classes = [IsAuthenticated, IsOwner]


class SelectionViewSet(ModelViewSet):
    queryset = SELO.all()
    serializer_class = SelectionSerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = SelectionDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.serializer_class = SelectionListSerializer
        return super().list(request, *args, **kwargs)

    # @method_permission_classes([IsAuthenticated])
    def create(self, request, *args, **kwargs):
        request.data['owner'] = request.user.id
        return super().create(request, *args, **kwargs)

    # @method_permission_classes([IsAuthenticated, IsOwner])
    # def update(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)
    #
    # @method_permission_classes([IsAuthenticated, IsOwner])
    # def destroy(self, request, *args, **kwargs):
    #     return super().destroy(request, *args, **kwargs)

    def get_permissions(self):
        permissions = []
        if self.action == "create":
            permissions = (IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            permissions = (IsAuthenticated & IsOwner,)
        return [permission() for permission in permissions]
