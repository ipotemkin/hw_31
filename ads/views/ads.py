from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, UpdateView, DeleteView, ListView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from skyvito.settings import TOTAL_ON_PAGE
from ads.models import (
    Ad,
    AdModel,
    AdUpdateModel,
    ADO,
)

from ads.utils import smart_json_response, patch_shortcut, pretty_json_response, SmartPaginator


def ad_decoder(data):
    """converts user object into a dict"""

    return {
        "id": data.id,
        "name": data.name,
        "author_id": data.author_id,
        "author": data.author.username,
        "price": data.price,
        "description": data.description,
        "is_published": data.is_published,
        "category_id": data.category_id,
        "category": data.category.name,
        "image": data.image.url if data.image else "No picture yet"
    }


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

    return query


@method_decorator(csrf_exempt, name="dispatch")
class AdView(View):  # shows all ads and create an ad
    @staticmethod
    def get(request):  # GET ads/ad/
        """shows all ads, paginated if page number is present in query params"""

        query = build_query(request)
        obj_list = ADO.select_related("author", "category").filter(query).distinct()
        # obj_list = ADO.select_related("author", "category").filter(query).order_by('pk').distinct('pk')
        # obj_list = obj_list.order_by('-price')

        # if paginated
        if page_number := request.GET.get("page"):
            paginator = SmartPaginator(obj_list, TOTAL_ON_PAGE, schema=ad_decoder)
            return pretty_json_response(paginator.get_page(page_number))

        # if not paginated
        return smart_json_response(ad_decoder, obj_list)

    @staticmethod
    def post(request):  # POST ads/ad/
        """ads a new ad"""

        ad = ADO.create(**AdModel.parse_raw(request.body).dict())
        return pretty_json_response(ad_decoder(ad))
        # return smart_json_response(AdModel, ad)


# вариант с использованием класса  ListView и встроенного пагинатора
class AdListView(ListView):
    model = Ad
    paginate_by = TOTAL_ON_PAGE

    def get(self, request, *args, **kwargs):  # GET ads/ads/
        """shows all ads, paginated"""

        if query := build_query(request):
            self.queryset = (
                self.get_queryset()
                    .select_related("author", "category")
                    .filter(query)
                    .order_by('pk')
                    .distinct('pk')
                    # .order_by('-price')
            )
            # self.queryset = (
            #     self.get_queryset()
            #         .select_related("author", "category")
            #         .prefetch_related("location")
            #         .filter(query)
            # )
            # print('here')

        super().get(request, *args, **kwargs)  # to create context with a built-in paginator

        return smart_json_response(ad_decoder, self.get_context_data()["object_list"])


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs) -> JsonResponse:  # GET ads/ad/
        """shows an ad"""

        return pretty_json_response(ad_decoder(self.get_object()))
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
    def patch(request, pk):  # PATCH ads/ad/pk/update/
        """updates an ad"""

        obj = patch_shortcut(request, pk, model=Ad, schema=AdUpdateModel)
        return pretty_json_response(ad_decoder(obj))
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
class AdImageUpdateView(UpdateView):
    model = Ad
    fields = ["image"]

    def post(self, request, *args, **kwargs):  # POST ads/ad/pk/upload_image/
        """ads/updates an image for the specified ad"""

        self.object = self.get_object()
        self.object.image = request.FILES["image"]
        self.object.save()

        return smart_json_response(ad_decoder, self.object)


@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        """deletes an ad"""

        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdHTMLView(View):
    @staticmethod
    def get(request) -> HttpResponse:  # GET ads/ad/html/
        """shows all ads using an html template"""
        res_obj = ADO.filter(name__iregex=name) if (name := request.GET.get("name", None)) else ADO.all()
        return render(request, "ads_list.html", {"ads": res_obj})


# shows an ad using an html template
class AdHTMLDetailView(DetailView):  # GET ads/ad/html/pk/
    model = Ad
