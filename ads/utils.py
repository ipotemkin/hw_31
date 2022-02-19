from typing import Union

from pydantic import BaseModel

from django.http import JsonResponse, Http404
from django.core.paginator import Paginator
from django.core.exceptions import BadRequest


def pretty_json_response(json_data: Union[dict, list[dict]]) -> JsonResponse:
    """
    a shortcut to JsonResponse with json dumps parameters
    """

    return JsonResponse(
        json_data,
        safe=False,
        json_dumps_params={
            "ensure_ascii": False,
            "indent": 2,
        },  # чтобы вывести кириллицу в браузере + отступы
    )


def smart_json_response(model, data: Union[dict, list]) -> JsonResponse:
    """
    jsonifies according to the specified model, understands lists and standalone objects,
    uses json_dumps_params={'ensure_ascii': False, 'indent': 2}
    """

    lst = False
    try:
        len(data)
    except TypeError:
        lst = True
    finally:
        return JsonResponse(
            model.from_orm(data).dict() if lst else [model.from_orm(obj).dict() for obj in data],
            safe=False,
            json_dumps_params={'ensure_ascii': False, 'indent': 2}
        )


def patch_shortcut(request, pk, model, schema):
    """
    updates a record with the specified pk

    :param request: HttpRequest object
    :param pk: the record's id
    :param model: database model
    :param schema: pydantic model to update data
    :param schema: pydantic model
    """

    # parses the body payload and validates with pydantic
    try:
        updated_data = schema.parse_raw(request.body).dict(exclude_unset=True)
    except (ValueError, AttributeError) as e:
        raise BadRequest(e)
        # return JsonResponse({"validation error": str(e)}, status=400)

    # gets the required record
    obj_query = model.objects.filter(pk=pk)
    if not obj_query:
        raise Http404

    # updates the record in DB
    try:
        obj_query.update(**updated_data)
    except Exception as e:
        return JsonResponse({"error while updating in database": str(e)}, status=400)

    return obj_query.first()


# TODO to delete on release
def format_paginated_response(object_lst, page_obj):
    """deprecated after SmartPaginator"""

    return {
        "items": object_lst,
        "total": page_obj.paginator.count,
        "per_page": page_obj.paginator.per_page,
        "num_pages": page_obj.paginator.num_pages
    }


# TODO to delete on release
def get_paginated_response(object_list, per_page, page_number, schema):
    """deprecated after SmartPaginator"""

    paginator = Paginator(object_list, per_page)
    page_obj = paginator.get_page(page_number)
    page_obj_list = [schema.from_orm(ad).dict() for ad in page_obj]
    return format_paginated_response(page_obj_list, page_obj)


class SmartPaginator(Paginator):
    """
    Ads to Django Paginator a specified output format, based on a specified pydantic schema
    """

    def __init__(self, object_list, per_page: int, schema):
        super().__init__(object_list, per_page)
        self.schema = schema
        self.page_obj_list = None

    def _format_response(self):
        if self.page_obj_list:
            return {
                "items": self.page_obj_list,
                "total": self.count,
                "per_page": self.per_page,
                "num_pages": self.num_pages
            }
        return None

    def get_page(self, number):
        page_obj = super().get_page(number)
        self.page_obj_list = [self.schema.from_orm(item).dict() for item in page_obj]
        return self._format_response()


def update_from_dict(source: dict, target):
    for key, value in source.items():
        try:
            if value:
                target.__dict__[key] = value
        except AttributeError:
            continue
    # return target
