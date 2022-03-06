from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from rest_framework.generics import (
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListCreateAPIView
)

from rest_framework.permissions import IsAuthenticated
from ads.models import Ad, ADO
from ads.permissions import AdUpdateDeletePermission
from ads.serializers import AdSerializer


def index(request):  # noqa
    return JsonResponse({"status": "ok"})


def build_query(request):
    """builds a query with the specified query params"""

    query = Q()
    if search_cat := request.GET.get('cat'):  # for filtering by category_id
        query |= Q(category_id=search_cat)

    if search := request.GET.get('text'):
        query &= Q(name__icontains=search)

    if search_loc := request.GET.get('location'):
        query &= Q(author__locations__name__icontains=search_loc)

    if search_price_from := request.GET.get('price_from'):
        query &= Q(price__gte=search_price_from)

    if search_price_to := request.GET.get('price_to'):
        query &= Q(price__lte=search_price_to)

    if username := request.GET.get('username'):
        query &= Q(author__username__icontains=username)

    return query


class AdAPIView(RetrieveAPIView):
    queryset = ADO.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]


class AdListCreateAPIView(ListCreateAPIView):
    queryset = ADO.all()
    serializer_class = AdSerializer

    def get(self, request, *args, **kwargs):
        if query := build_query(request):
            self.queryset = (
                self.get_queryset()
                    .select_related("author", "category")
                    .filter(query)
                    .distinct()
            )
        return super().get(request, *args, **kwargs)


class AdUpdateAPIView(UpdateAPIView):
    queryset = ADO.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated, AdUpdateDeletePermission]


class AdDeleteAPIView(DestroyAPIView):
    queryset = ADO.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated, AdUpdateDeletePermission]


@method_decorator(csrf_exempt, name="dispatch")
class AdImageUpdateView(UpdateView):
    model = Ad
    fields = ["image"]

    def post(self, request, *args, **kwargs):  # POST ads/pk/upload_image/
        """ads/updates an image for the specified ad"""

        obj = self.get_object()
        obj.image = request.FILES["image"]
        obj.save()
        return JsonResponse(AdSerializer(obj).data)


@method_decorator(csrf_exempt, name="dispatch")
class AdHTMLView(View):
    @staticmethod
    def get(request) -> HttpResponse:  # GET ads/html/
        """shows all ads using an html template"""
        res_obj = ADO.filter(name__iregex=name) if (name := request.GET.get("name", None)) else ADO.all()
        return render(request, "ads_list.html", {"ads": res_obj})


# shows an ad using an html template
class AdHTMLDetailView(DetailView):  # GET ads/html/pk/
    model = Ad
