from django.db import models


class Ad(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.CharField(max_length=1000)
    address = models.CharField(max_length=120)
    is_published = models.BooleanField(default=False)


class Cat(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Категории"
        verbose_name = "Категория"
        ordering = ["name"]
