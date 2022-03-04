from typing import Optional

from django.contrib.auth.models import AbstractUser
from pydantic import BaseModel, Field, Extra
from django.db import models


class Ad(models.Model):
    name = models.CharField(max_length=100, verbose_name="Объявление")
    author = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="Автор")
    price = models.PositiveIntegerField(verbose_name="Цена")
    description = models.CharField(max_length=1000, verbose_name="Описание", null=True, blank=True)
    is_published = models.BooleanField(default=False, verbose_name="Опубликован или нет")
    category = models.ForeignKey('Cat', on_delete=models.PROTECT, verbose_name="Категория")
    image = models.ImageField(upload_to="img/", null=True)

    class Meta:
        verbose_name_plural = "Объявления"
        verbose_name = "Объявление"
        ordering = ["-price"]

    def __str__(self):
        return self.name


class Cat(models.Model):
    name = models.CharField(max_length=120, verbose_name="Категория")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Категории"
        verbose_name = "Категория"
        ordering = ["name"]


class Location(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="Локация")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Локации"
        verbose_name = "Локация"
        ordering = ["name"]


class User(AbstractUser):

    USER = "user"
    ADMIN = "admin"

    ROLES = [(USER, "Пользователь"), (ADMIN, "Администратор")]

# class User(models.Model):
#     username = models.CharField(max_length=30, verbose_name="Имя пользователя в системе")
#     first_name = models.CharField(max_length=20, null=True, blank=True, verbose_name="Имя")
#     last_name = models.CharField(max_length=20, null=True, blank=True, verbose_name="Фамилия")

    role = models.CharField(max_length=5, choices=ROLES, default=USER, verbose_name="Роль")
    age = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Возраст")
    locations = models.ManyToManyField(Location)

    def __str__(self):
        return self.username

    # def save(self, *args, **kwargs):
    #     self.set_password(self.password)
    #     super().save()

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
    author_id: int = Field(alias="author_id")
    price: int
    description: Optional[str]
    is_published: bool = False
    category_id: int  # = Field(alias="category_id")


class AdUpdateModel(BaseModelConfig):
    name: Optional[str]
    author_id: Optional[int]
    price: Optional[int]
    description: Optional[str]
    is_published: Optional[bool]
    category_id: Optional[int]  # = Field(alias="category_id")

# shortcuts
ADO = Ad.objects  # noqa
CATO = Cat.objects  # noqa
USERO = User.objects  # noqa
LOCO = Location.objects  # noqa
