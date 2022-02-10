from ads import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    # path("<int:pk>/", views.get_car, name="car_by_pk"),
    # path("search/", views.search, name="cars_search"),
]
