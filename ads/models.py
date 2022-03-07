from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator

from ads.validators import check_domain


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

    role = models.CharField(max_length=5, choices=ROLES, default=USER, verbose_name="Роль")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    email = models.EmailField(
        null=True,
        blank=True,
        unique=True,
        validators=[check_domain],
        verbose_name="Email"
    )
    locations = models.ManyToManyField(Location)

    def __str__(self):
        return f"{self.username}: {self.email}"

    class Meta:
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"
        ordering = ["username"]


class Cat(models.Model):
    name = models.CharField(max_length=120, verbose_name="Категория")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Категории"
        verbose_name = "Категория"
        ordering = ["name"]


class Ad(models.Model):
    name = models.CharField(max_length=100, validators=[MinLengthValidator(10)], verbose_name="Объявление")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    price = models.PositiveIntegerField(verbose_name="Цена")
    description = models.CharField(max_length=1000, verbose_name="Описание", null=True, blank=True)
    is_published = models.BooleanField(default=False, verbose_name="Опубликован или нет")
    category = models.ForeignKey(Cat, on_delete=models.PROTECT, verbose_name="Категория")
    image = models.ImageField(upload_to="img/", null=True)

    class Meta:
        verbose_name_plural = "Объявления"
        verbose_name = "Объявление"
        ordering = ["-price"]

    def __str__(self):
        return self.name


class Selection(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор объявления")
    items = models.ManyToManyField(Ad)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Избранное"
        verbose_name = "Избранное"


# shortcuts
ADO = Ad.objects  # noqa
CATO = Cat.objects  # noqa
USERO = User.objects  # noqa
LOCO = Location.objects  # noqa
SELO = Selection.objects # noqa
