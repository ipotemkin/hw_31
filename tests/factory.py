import factory.django

from ads.models import Ad, User, Cat


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("name")
    password = "qwerty123"


class CatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cat

    name = "Testing category"


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    name = "Testing advertisement"
    price = 1000
    author = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CatFactory)
