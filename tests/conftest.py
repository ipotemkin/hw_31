from pytest_factoryboy import register
from tests.factory import UserFactory, AdFactory, CatFactory

pytest_plugins = "tests.fixtures"

register(UserFactory)
register(AdFactory)
register(CatFactory)
