from typing import Union

from django.http import JsonResponse, Http404


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
    except ValueError as e:
        return JsonResponse({"validation error": str(e)}, status=400)

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
