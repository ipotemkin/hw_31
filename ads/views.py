from typing import Optional
from pydantic import BaseModel, Field

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView
from django.views.decorators.csrf import csrf_exempt

from .models import Ad, Cat


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
        return JsonResponse(
            [AdModel.from_orm(ad).dict() for ad in Ad.objects.all()],
            safe=False,
        )

    @staticmethod
    def post(request):
        ad = Ad.objects.create(**AdModel.parse_raw(request.body).dict())
        return JsonResponse(AdModel.from_orm(ad).dict())


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        return JsonResponse(AdModel.from_orm(ad).dict())


@method_decorator(csrf_exempt, name='dispatch')
class CatView(View):
    @staticmethod
    def get(request):
        return JsonResponse(
            [CatModel.from_orm(cat).dict() for cat in Cat.objects.all()],
            safe=False
        )

    @staticmethod
    def post(request):
        cat = Cat.objects.create(**CatModel.parse_raw(request.body).dict())
        return JsonResponse(CatModel.from_orm(cat).dict())


class CatDetailView(DetailView):
    model = Cat

    def get(self, request, *args, **kwargs):
        cat = self.get_object()
        return JsonResponse(CatModel.from_orm(cat).dict())
