from ads import views
from ads.views_lib import users
from django.urls import path


urlpatterns = [
    # ad
    path("ad/<int:pk>/update/", views.AdUpdateView.as_view(), name="ad_update"),
    path("ad/<int:pk>/delete/", views.AdDeleteView.as_view(), name="ad_delete"),
    path("ad/<int:pk>/upload_image/", views.AdImageUpdateView.as_view(), name="ad_upload_image"),
    path("ad/<int:pk>/", views.AdDetailView.as_view(), name="ad"),
    path("ad/", views.AdView.as_view(), name="ads_all"),
    path("ads/", views.AdListView.as_view(), name="ads_list"),
    # cat
    path("cat/<int:pk>/update/", views.CatUpdateView.as_view(), name="cat_update"),
    path("cat/<int:pk>/delete/", views.CatDeleteView.as_view(), name="cat_delete"),
    path("cat/<int:pk>/", views.CatDetailView.as_view(), name="cat"),
    path("cat/", views.CatView.as_view(), name="cats_all"),
    # user
    path("user/<int:pk>/update/", users.UserUpdateView.as_view(), name="user_update"),
    path("user/<int:pk>/delete/", users.UserDeleteView.as_view(), name="user_delete"),
    path("user/<int:pk>/", users.UserDetailView.as_view(), name="user"),
    path("user/create/", users.UserCreateView.as_view(), name="user_create"),
    path("user/", users.UserView.as_view(), name="users_all"),
    # additional urls
    path("ad/http-json/", views.AdHTTPJsonView.as_view(), name="ad_http_json"),
    path("ad/http-json/<int:pk>/", views.AdHTTPJsonDetailView.as_view(), name="ad_http_json_pk"),
    path("ad/http/", views.AdHTTPView.as_view(), name="ad_http"),
    path("ad/http/<int:pk>/", views.AdHTTPDetailView.as_view(), name="ad_http_detail"),
]
