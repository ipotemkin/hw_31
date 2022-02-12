from django.contrib import admin

# Register your models here.
from .models import Ad, Cat

admin.site.register(Ad)
admin.site.register(Cat)
