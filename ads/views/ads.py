from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import Ad, ADO
from ads.permissions import IsAdmin, IsAuthor
from ads.serializers import AdSerializer, AdCreateSerializer


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
        """shows all ads using an HTML template"""

        res_obj = ADO.filter(name__iregex=name) if (name := request.GET.get("name", None)) else ADO.all()
        return render(request, "ads_list.html", {"ads": res_obj})


# shows an ad using an html template
class AdHTMLDetailView(DetailView):  # GET ads/html/pk/
    """shows an ad with the specified pk using an HTML template"""

    model = Ad


class AdViewSet(ModelViewSet):
    """views for ads"""

    queryset = ADO.all()
    serializer_class = AdSerializer

    def list(self, request, *args, **kwargs):
        """shows a list of ads"""

        if query := build_query(request):
            self.queryset = (
                self.get_queryset()
                    .select_related("author", "category")
                    .filter(query)
                    .distinct()
            )
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """creates an ad"""

        self.serializer_class = AdCreateSerializer
        return super().create(request, *args, **kwargs)

    def get_permissions(self):
        """sets permissions for ads' views"""

        permissions = []
        if self.action == "retrieve":
            permissions = (IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            permissions = (IsAuthenticated & (IsAdmin | IsAuthor),)
        return [permission() for permission in permissions]
