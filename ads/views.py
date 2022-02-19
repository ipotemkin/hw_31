import json
import time

from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, UpdateView, DeleteView, ListView, CreateView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404

from skyvito.settings import TOTAL_ON_PAGE
from .models import (
    Ad,
    Cat,
    AdModel,
    CatModel,
    AdUpdateModel,
    CatUpdateModel,
    ADO,
    CATO,
)

from .utils import smart_json_response, patch_shortcut, pretty_json_response, SmartPaginator

# shortcuts
# ADO = Ad.objects  # noqa
# CATO = Cat.objects  # noqa
# USERO = User.objects  # noqa
# LOCO = Location.objects  # noqa


def ad_encoder(data):
    """converts user object into a dict"""

    return {
        "id": data.id,
        "name": data.name,
        "author_id": data.author_id,
        "author": data.author.username,
        "price": data.price,
        "description": data.description,
        "address": data.address,
        "is_published": data.is_published,
        "category_id": data.category_id,
        "category": data.category.name
    }


def index(request):  # noqa
    return JsonResponse({"status": "ok"})


@method_decorator(csrf_exempt, name="dispatch")
class AdView(View):  # shows all ads and create an ad
    @staticmethod
    def get(request):  # ads/ad/
        """shows all ads, paginated if page number is present in query params"""

        obj_list = ADO.all()

        # if paginated
        if page_number := request.GET.get("page"):
            paginator = SmartPaginator(obj_list, TOTAL_ON_PAGE, schema=ad_encoder)
            return pretty_json_response(paginator.get_page(page_number))

        # if not paginated
        return smart_json_response(ad_encoder, obj_list.select_related("author", "category"))

    @staticmethod
    def post(request):
        """ads a new ad"""

        ad = ADO.create(**AdModel.parse_raw(request.body).dict())
        return pretty_json_response(ad_encoder(ad))
        # return smart_json_response(AdModel, ad)


# вариант с использованием класса  ListView и встроенного пагинатора
class AdListView(ListView):
    model = Ad
    paginate_by = TOTAL_ON_PAGE

    def get(self, request, *args, **kwargs):
        """shows all ads, paginated"""

        super().get(request, *args, **kwargs)
        return pretty_json_response(
            [ad_encoder(ad) for ad in self.get_context_data()["object_list"]]
        )
        # return smart_json_response(AdModel, self.get_context_data()["object_list"])


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs) -> JsonResponse:
        """shows an ad"""

        return pretty_json_response(ad_encoder(self.get_object()))
        # return smart_json_response(AdModel, self.get_object())

# вариант с UpdateView, но я считаю, что в нашем случае лучше просто взять View + метод update (см. код ниже)
# @method_decorator(csrf_exempt, name="dispatch")
# class AdUpdateView(UpdateView):
#     model = Ad
#     fields = ["name", "author", "price", "description", "address", "is_published", "category"]
#
#     def patch(self, request, *args, **kwargs):
#         updated_data = AdUpdateModel.parse_raw(request.body).dict(exclude_unset=True)
#         obj_query = ADO.filter(pk=kwargs["pk"])
#         obj_query.update(**updated_data)
#         return smart_json_response(AdModel, obj_query.first())


@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(View):

    @staticmethod
    def patch(request, pk):
        """updates an ad"""

        obj = patch_shortcut(request, pk, model=Ad, schema=AdUpdateModel)
        return pretty_json_response(ad_encoder(obj))
        # return smart_json_response(AdModel, obj)

        # # 1 --------------
        # # parses the body payload and validates with pydnatic
        # # t0 = time.perf_counter()
        # try:
        #     updated_data = AdUpdateModel.parse_raw(request.body).dict(exclude_unset=True)
        # except ValueError as e:
        #     return JsonResponse({"validation error": str(e)}, status=400)
        # # t1 = time.perf_counter()
        #
        # # gets the required record
        # obj_query = ADO.filter(pk=pk)
        # if not obj_query:
        #     raise Http404
        # # t2 = time.perf_counter()
        #
        # # updates the record in DB
        # try:
        #     obj_query.update(**updated_data)
        # except Exception as e:
        #     return JsonResponse({"error while updating in database": str(e)}, status=400)
        # # t3 = time.perf_counter()
        #
        # # print("update: 1 (parsing the payload): [%0.8fs]" % (t1 - t0))
        # # print("update: 2 (getting the record form db): [%0.8fs]" % (t2 - t1))
        # # print("update: 3 (updating the record in db): [%0.8fs]" % (t3 - t2))
        # # print("update: total: [%0.8fs]" % (t3 - t0))

        # 2 ------------

        # t0 = time.perf_counter()
        # try:
        #     updated_data = AdUpdateModel.parse_raw(request.body)
        # except ValueError as e:
        #     return JsonResponse({"validation error": str(e)}, status=400)
        # t1 = time.perf_counter()
        #
        # # gets the required record
        # obj = get_object_or_404(Ad, pk=pk)
        # t2 = time.perf_counter()
        #
        # # updates the record in DB
        # if updated_data.name:
        #     obj.name = updated_data.name
        # if updated_data.author:
        #     obj.author = updated_data.author
        # if updated_data.price:
        #     obj.price = updated_data.price
        # if updated_data.description:
        #     obj.description = updated_data.description
        # if updated_data.address:
        #     obj.address = updated_data.address
        # if updated_data.is_published:
        #     obj.is_published = updated_data.is_published
        # if updated_data.category:
        #     obj.category_id = updated_data.category
        #
        # try:
        #     obj.full_clean()
        # except ValueError as error:
        #     return JsonResponse(error.message_dict, status=422)
        # t3 = time.perf_counter()
        #
        # obj.save()
        # t4 = time.perf_counter()
        #
        # print("save: 1 (parsing the payload): [%0.8fs]" % (t1 - t0))
        # print("save: 2 (getting the record form db): [%0.8fs]" % (t2 - t1))
        # print("save: 3 (validating): [%0.8fs]" % (t3 - t2))
        # print("save: 4 (saving to db): [%0.8fs]" % (t4 - t3))
        # print("save: total: [%0.8fs]" % (t4 - t0))

        # выводы: БД, конечно, кэширует запросы, но если каждый раз запускать в разной последовательности,
        # то можно сделать вывод, что вариант с update быстрее. Мануал django тоже пишет, что update быстрее

        # return smart_json_response(AdModel, obj_query.first())


@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        """deletes an ad"""

        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdHTTPJsonView(View):
    @staticmethod
    def get(request) -> HttpResponse:
        """shows all ads as json using html"""

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
        """shows all ads using an html template"""
        res_obj = ADO.filter(name__iregex=name) if (name := request.GET.get("name", None)) else ADO.all()
        return render(request, "ads_list.html", {"ads": res_obj})


# shows an ad using an html template
class AdHTTPDetailView(DetailView):
    model = Ad


class AdHTTPJsonDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """shows a json response as html"""

        s = AdModel.from_orm(self.get_object()).json(ensure_ascii=False, indent="\t")
        return HttpResponse(s, content_type="text/plain; charset=utf-8")


# я не стал переделывать на ListView и CreateView, так как не вижу в этом никакой эффективности
@method_decorator(csrf_exempt, name="dispatch")
class CatView(View):
    @staticmethod
    def get(request) -> JsonResponse:  # noqa
        """shows all categories"""

        obj_list = CATO.all()

        # if paginated
        if page_number := request.GET.get("page"):
            paginator = SmartPaginator(obj_list, TOTAL_ON_PAGE, CatModel)
            return pretty_json_response(paginator.get_page(page_number))

        # if not paginated
        return smart_json_response(CatModel, obj_list)

    @staticmethod
    def post(request) -> JsonResponse:
        """creates a new category"""

        cat = CATO.create(**CatModel.parse_raw(request.body).dict())
        return smart_json_response(CatModel, cat)


# лучше было бы добавить patch в класс CatView, но поскольку просили другую ручку, то я сделал отдельный класс
@method_decorator(csrf_exempt, name="dispatch")
class CatUpdateView(View):

    @staticmethod
    def patch(request, pk) -> JsonResponse:
        """partially updates a category"""

        obj = patch_shortcut(request, pk, model=Cat, schema=CatUpdateModel)
        return smart_json_response(CatModel, obj)


class CatDetailView(DetailView):
    model = Cat

    def get(self, request, *args, **kwargs) -> JsonResponse:
        """shows a category"""

        return smart_json_response(CatModel, self.get_object())


@method_decorator(csrf_exempt, name="dispatch")
class CatDeleteView(DeleteView):
    model = Cat
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        """deletes a category"""

        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)
