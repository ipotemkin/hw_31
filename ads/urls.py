from ads.views import ads, users, categories
from django.urls import path

urlpatterns = [
    # ad
    path("ad/<int:pk>/update/", ads.AdUpdateView.as_view(), name="ad_update"),
    path("ad/<int:pk>/delete/", ads.AdDeleteView.as_view(), name="ad_delete"),
    path("ad/<int:pk>/upload_image/", ads.AdImageUpdateView.as_view(), name="ad_upload_image"),
    path("ad/<int:pk>/", ads.AdDetailView.as_view(), name="ad"),
    path("ad/", ads.AdView.as_view(), name="ads_all"),
    path("ads/", ads.AdListView.as_view(), name="ads_list"),

    # cat
    path("cat/<int:pk>/update/", categories.CatUpdateView.as_view(), name="cat_update"),
    path("cat/<int:pk>/delete/", categories.CatDeleteView.as_view(), name="cat_delete"),
    path("cat/<int:pk>/", categories.CatDetailView.as_view(), name="cat"),
    path("cat/", categories.CatView.as_view(), name="cats_all"),

    # user
    path("user/<int:pk>/update/", users.UserUpdateView.as_view(), name="user_update"),
    path("user/<int:pk>/delete/", users.UserDeleteView.as_view(), name="user_delete"),
    path("user/<int:pk>/", users.UserDetailView.as_view(), name="user"),
    path("user/create/", users.UserCreateView.as_view(), name="user_create"),
    path("user/", users.UserView.as_view(), name="users_all"),

    # additional urls
    path("ad/html/<int:pk>/", ads.AdHTMLDetailView.as_view(), name="ad_http_detail"),
    path("ad/html/", ads.AdHTMLView.as_view(), name="ad_http"),
]


