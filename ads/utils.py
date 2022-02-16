from typing import Union

from django.http import JsonResponse


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
