from ads import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("ad/", views.AdView.as_view(), name="ads_all"),
    path("cat/", views.CatView.as_view(), name="cats_all"),
    path("ad/<int:pk>/", views.AdDetailView.as_view(), name="ad"),
    path("cat/<int:pk>/", views.CatDetailView.as_view(), name="cat"),
    path("ad/http-json/", views.AdHTTPJsonView.as_view(), name="ad_http_json"),
    path("ad/http-json/<int:pk>/", views.AdHTTPJsonDetailView.as_view(), name="ad_http_json_pk"),
    path("ad/http/", views.AdHTTPView.as_view(), name="ad_http"),
    path("ad/http/detail/<int:pk>/", views.AdHTTPDetailView.as_view(), name="ad_http_detail"),
]
