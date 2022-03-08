from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError


def method_permission_classes(classes):
    """to set different permissions on classes' methods"""

    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = classes
            # this call is needed for request permissions
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)
        return decorated_func
    return decorator


def check_domain(value: str) -> None:
    """domain rambler.ru forbidden"""

    domain = value.split("@")
    print(domain)
    if len(domain) < 2:
        return

    domain = domain[1].lower()
    if domain == "rambler.ru":
        raise ValidationError(
            'Domain rambler.ru forbidden',
            params={'value': value},
        )


def check_false(value: bool) -> None:
    """checks for false"""

    if value:
        raise ValidationError(
            'Needed False',
            params={'value': value},
        )


def check_age(value: datetime.date) -> None:
    """user's age should be > 9 years"""

    delta = relativedelta(datetime.utcnow().date(), value)
    if delta.years < 9:
        raise ValidationError(
            'Age should be more than 9 years',
            params={'value': value},
        )
