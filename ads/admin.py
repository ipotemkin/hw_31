from django.contrib import admin

# Register your models here.
from .models import Ad, Cat, User, Location


class AdAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'price', 'description')
    list_display_links = ('name', 'author')
    search_fields = ('name', 'author', 'description')


admin.site.register(Ad, AdAdmin)
admin.site.register(Cat)
admin.site.register(User)
admin.site.register(Location)
