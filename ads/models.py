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
    category = models.ForeignKey('Cat', on_delete=models.PROTECT, verbose_name="Категория")

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


class User(models.Model):
    username = models.CharField(max_length=30, null=True, blank=True, verbose_name="Имя пользователя")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"
        ordering = ["username"]


class Location(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="Локация")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Локации"
        verbose_name = "Локация"
        ordering = ["name"]


class AdModel(BaseModel):
    pk: Optional[int] = Field(alias="id")
    name: str
    author: str
    price: int
    description: Optional[str]
    address: str
    is_published: bool
    category: int = Field(alias="category_id")

    class Config:
        orm_mode = True


class AdUpdateModel(BaseModel):
    pk: Optional[int] = Field(alias="id")
    name: Optional[str]
    author: Optional[str]
    price: Optional[int]
    description: Optional[str]
    address: Optional[str]
    is_published: Optional[bool]
    category: Optional[int] = Field(alias="category_id")

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
