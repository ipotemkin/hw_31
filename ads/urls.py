from ads import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("ad/", views.AdView.as_view(), name="ads_all"),
    path("cat/", views.CatView.as_view(), name="cats_all"),
    path("ad/<int:pk>/", views.AdDetailView.as_view(), name="ad"),
    path("cat/<int:pk>/", views.CatDetailView.as_view(), name="cat"),
]
