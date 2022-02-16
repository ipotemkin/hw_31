import json

from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from .models import Ad, Cat, AdModel, CatModel

from .utils import smart_json_response

# shortcuts
ADO = Ad.objects  # noqa
CATO = Cat.objects  # noqa


def index(request):  # noqa
    return JsonResponse({"status": "ok"})


@method_decorator(csrf_exempt, name="dispatch")
class AdView(View):
    @staticmethod
    def get(request):  # noqa
        return smart_json_response(AdModel, ADO.all())

    @staticmethod
    def post(request):
        ad = ADO.create(**AdModel.parse_raw(request.body).dict())
        return smart_json_response(AdModel, ad)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs) -> JsonResponse:
        return smart_json_response(AdModel, self.get_object())


@method_decorator(csrf_exempt, name="dispatch")
class AdHTTPJsonView(View):
    @staticmethod
    def get(request) -> HttpResponse:
        res_obj = ADO.filter(name__iregex=name) if (name := request.GET.get("name", None)) else ADO.all()
        s_dicts = [AdModel.from_orm(ad).dict(include={"pk", "name", "price"}) for ad in res_obj]

        # an attempt to serialize pydantic models
        # s_dicts = [{"item": AdModel.from_orm(ad)} for ad in res_obj]
        # s_dicts = AdsModel.from_orm(s_dicts)

        s = json.dumps(s_dicts, ensure_ascii=False, indent=2)
        return HttpResponse(s, content_type="text/plain; charset=utf-8")


@method_decorator(csrf_exempt, name="dispatch")
class AdHTTPView(View):
    @staticmethod
    def get(request) -> HttpResponse:
        res_obj = ADO.filter(name__iregex=name) if (name := request.GET.get("name", None)) else ADO.all()
        return render(request, "ads_list.html", {"ads": res_obj})


class AdHTTPDetailView(DetailView):
    model = Ad


class AdHTTPJsonDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs) -> HttpResponse:
        s = AdModel.from_orm(self.get_object()).json(ensure_ascii=False, indent="\t")
        return HttpResponse(s, content_type="text/plain; charset=utf-8")


@method_decorator(csrf_exempt, name="dispatch")
class CatView(View):
    @staticmethod
    def get(request) -> JsonResponse:  # noqa
        return smart_json_response(CatModel, CATO.all())

    @staticmethod
    def post(request) -> JsonResponse:
        cat = CATO.create(**CatModel.parse_raw(request.body).dict())
        return smart_json_response(CatModel, cat)


class CatDetailView(DetailView):
    model = Cat

    def get(self, request, *args, **kwargs) -> JsonResponse:
        return smart_json_response(CatModel, self.get_object())
