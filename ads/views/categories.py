from django.db.models import Q
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ads.models import Cat, CATO


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = "__all__"


class CatAPIViewSet(ModelViewSet):
    queryset = CATO.all()
    serializer_class = CatSerializer

    def list(self, request, *args, **kwargs):
        """Добавлены функции для поиска по названию категории и сортировка"""

        if search := request.GET.getlist('search'):  # for searching in field name
            query = None
            for s in search:
                query = query | Q(name__icontains=s) if query else Q(name__icontains=s)
            self.queryset = self.queryset.filter(query)

        if order := request.GET.get('ordering'):  # for sorting records retrieved
            self.queryset = self.queryset.order_by(order)

        # return Response(self.serializer_class(self.queryset, many=True).data)
        return super().list(request, *args, **kwargs)

        # page = self.paginate_queryset(self.queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        #
        # serializer = self.get_serializer(self.queryset, many=True)
        # return Response(serializer.data)

