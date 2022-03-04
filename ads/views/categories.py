from django.db.models import Q
from rest_framework.viewsets import ModelViewSet

from ads.models import CATO
from ads.serializers import CatSerializer


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

        return super().list(request, *args, **kwargs)
