from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, DeleteView
from django.views.decorators.csrf import csrf_exempt

from skyvito.settings import TOTAL_ON_PAGE
from ads.models import (
    Cat,
    CatModel,
    CatUpdateModel,
    CATO,
)

from ads.utils import smart_json_response, patch_shortcut, pretty_json_response, SmartPaginator


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
