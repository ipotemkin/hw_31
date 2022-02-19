from typing import Optional
from pydantic import BaseModel, Field, Extra, constr
from django.db import models


class Ad(models.Model):
    name = models.CharField(max_length=100, verbose_name="Объявление")
    author = models.CharField(max_length=100, verbose_name="Автор")
    price = models.IntegerField(verbose_name="Цена")
    description = models.CharField(max_length=1000, verbose_name="Описание", null=True, blank=True)
    address = models.CharField(max_length=120, verbose_name="Адрес")
    is_published = models.BooleanField(default=False, verbose_name="Опубликован или нет")
    category = models.ForeignKey('Cat', on_delete=models.PROTECT, verbose_name="Категория")

    class Meta:
        verbose_name_plural = "Объявления"
        verbose_name = "Объявление"
        # ordering = ["-price"]

    def __str__(self):
        return self.name


class Cat(models.Model):
    name = models.CharField(max_length=120, verbose_name="Категория")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Категории"
        verbose_name = "Категория"
        # ordering = ["name"]


class Location(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="Локация")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Локации"
        verbose_name = "Локация"
        ordering = ["name"]


class User(models.Model):
    username = models.CharField(max_length=30, verbose_name="Имя пользователя в системе")
    first_name = models.CharField(max_length=20, null=True, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=20, null=True, blank=True, verbose_name="Фамилия")
    role = models.CharField(max_length=20, null=True, blank=True, verbose_name="Роль")
    age = models.SmallIntegerField(null=True, blank=True, verbose_name="Возраст")
    locations = models.ManyToManyField(Location)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"
        ordering = ["username"]


class BaseModelConfig(BaseModel):
    class Config:
        orm_mode = True
        extra = Extra.forbid


class AdModel(BaseModelConfig):
    pk: Optional[int] = Field(alias="id")
    name: str
    author: str
    price: int
    description: Optional[str]
    address: str
    is_published: bool = False
    category_id: int  # = Field(alias="category_id")


class AdUpdateModel(BaseModelConfig):
    name: Optional[str]
    author: Optional[str]
    price: Optional[int]
    description: Optional[str]
    address: Optional[str]
    is_published: Optional[bool]
    category_id: Optional[int]  # = Field(alias="category_id")


# an attempt to serialize pydantic models
# class AdsModel(BaseModel):
#     item: list[AdModel]
#
#     class Config:
#         orm_mode = True


class CatModel(BaseModelConfig):
    pk: Optional[int] = Field(alias="id")
    name: constr(max_length=120)


class CatUpdateModel(BaseModelConfig):
    name: Optional[constr(max_length=120)]


class UserModel(BaseModel):
    pk: Optional[int] = Field(alias="id")
    username: constr(max_length=30)
    first_name: Optional[constr(max_length=20)]
    last_name: Optional[constr(max_length=20)]
    role: Optional[constr(max_length=20)]
    age: Optional[int]
    # locations: models.Manager

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        # fields = {'locations': {'exclude': True}}
        json_encoders = {
            models.Manager: lambda x: list(x.all().values_list('name', flat=True)),
        }


class UserUpdateModel(BaseModelConfig):
    username: Optional[constr(max_length=30)]
    first_name: Optional[constr(max_length=20)]
    last_name: Optional[constr(max_length=20)]
    role: Optional[constr(max_length=20)]
    age: Optional[int]
    locations: Optional[list]

    class Config:
        fields = {'locations': {'exclude': True}}

# shortcuts
ADO = Ad.objects  # noqa
CATO = Cat.objects  # noqa
USERO = User.objects  # noqa
LOCO = Location.objects  # noqa
