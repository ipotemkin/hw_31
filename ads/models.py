from typing import Optional
from pydantic import BaseModel, Field
from django.db import models


class Ad(models.Model):
    name = models.CharField(max_length=100, verbose_name="Объявление")
    author = models.CharField(max_length=100, verbose_name="Автор")
    price = models.IntegerField(verbose_name="Цена")
    description = models.CharField(max_length=1000, verbose_name="Описание", null=True, blank=True)
    address = models.CharField(max_length=120, verbose_name="Адрес")
    is_published = models.BooleanField(default=False, verbose_name="Опубликован или нет")
    category_id = models.ForeignKey('Cat', on_delete=models.PROTECT, verbose_name="Категория")

    class Meta:
        verbose_name_plural = "Объявления"
        verbose_name = "Объявление"
        ordering = ["pk"]

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


class User(models.Model):
    pass


class Location(models.Model):
    pass


class AdModel(BaseModel):
    pk: Optional[int] = Field(alias="id")
    name: str
    author: str
    price: int
    description: Optional[str]
    address: str
    is_published: bool
    category_id: int = Field(alias="category_id_id")

    class Config:
        orm_mode = True


# an attempt to serialize pydantic models
# class AdsModel(BaseModel):
#     item: list[AdModel]
#
#     class Config:
#         orm_mode = True


class CatModel(BaseModel):
    pk: Optional[int] = Field(alias="id")
    name: str

    class Config:
        orm_mode = True
