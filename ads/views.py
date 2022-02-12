from typing import Optional, Union
from pydantic import BaseModel, Field
import json

from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from .models import Ad, Cat


# shortcuts
ADO = Ad.objects
CATO = Cat.objects


def pretty_json_response(json_data: Union[dict, list[dict]]) -> JsonResponse:
    """
    a shortcut to JsonResponse with json dumps parameters
    """

    return JsonResponse(
        json_data,
        safe=False,
        json_dumps_params={"ensure_ascii": False, "indent": 2}  # чтобы вывести кириллицу в браузере + отступы
    )


class AdModel(BaseModel):
    pk: Optional[int] = Field(alias="id")
    name: str
    author: str
    price: int
    description: str
    address: str
    is_published: bool

    class Config:
        orm_mode = True


# an attempt to serialize pydantic models
# class AdsModel(BaseModel):
#     item: list[AdModel]
#
#     class Config:
#         orm_mode = True


class CatModel(BaseModel):
    pk: Optional[int] = Field(alias="id")
    name: str

    class Config:
        orm_mode = True


def index(request):
    return JsonResponse({"status": "ok"})


@method_decorator(csrf_exempt, name='dispatch')
class AdView(View):
    @staticmethod
    def get(request):
        return pretty_json_response([AdModel.from_orm(ad).dict() for ad in ADO.all()])

    @staticmethod
    def post(request):
        ad = ADO.create(**AdModel.parse_raw(request.body).dict())
        return pretty_json_response(AdModel.from_orm(ad).dict())


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs) -> JsonResponse:
        ad = self.get_object()
        return pretty_json_response(AdModel.from_orm(ad).dict())


@method_decorator(csrf_exempt, name='dispatch')
class AdHTTPJsonView(View):
    @staticmethod
    def get(request) -> HttpResponse:
        res_obj = ADO.filter(name=name) if (name := request.GET.get("name", None)) else ADO.all()
        s_dicts = [AdModel.from_orm(ad).dict(include={"pk", "name", "price"}) for ad in res_obj]

        # an attempt to serialize pydantic models
        # s_dicts = [{"item": AdModel.from_orm(ad)} for ad in res_obj]
        # s_dicts = AdsModel.from_orm(s_dicts)

        s = json.dumps(s_dicts, ensure_ascii=False, indent=2)
        return HttpResponse(s, content_type='text/plain; charset=utf-8')


@method_decorator(csrf_exempt, name='dispatch')
class AdHTTPView(View):
    @staticmethod
    def get(request) -> HttpResponse:
        res_obj = ADO.filter(name=name) if (name := request.GET.get("name", None)) else ADO.all()
        return render(request, 'ads_list.html', {"ads": res_obj})


class AdHTTPJsonDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs) -> HttpResponse:
        s = AdModel.from_orm(self.get_object()).json(ensure_ascii=False, indent='\t')
        return HttpResponse(s, content_type='text/plain; charset=utf-8')


@method_decorator(csrf_exempt, name='dispatch')
class CatView(View):
    @staticmethod
    def get(request) -> JsonResponse:
        return pretty_json_response([CatModel.from_orm(cat).dict() for cat in CATO.all()])

    @staticmethod
    def post(request) -> JsonResponse:
        cat = CATO.create(**CatModel.parse_raw(request.body).dict())
        return pretty_json_response(CatModel.from_orm(cat).dict())


class CatDetailView(DetailView):
    model = Cat

    def get(self, request, *args, **kwargs) -> JsonResponse:
        cat = self.get_object()
        return pretty_json_response(CatModel.from_orm(cat).dict())
