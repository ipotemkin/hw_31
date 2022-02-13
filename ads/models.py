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


class Cat(models.Model):
    name = models.CharField(max_length=120, verbose_name="Категория")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Категории"
        verbose_name = "Категория"
        ordering = ["name"]
