from rest_framework.routers import DefaultRouter

from ads.views import ads, users, categories
from django.urls import path, include

router = DefaultRouter()  # SimpleRouter
router.register('cats', categories.CatAPIViewSet)
router.register('locations', users.LocAPIViewSet)

urlpatterns = [
    # ad
    path("ad/<int:pk>/update/", ads.AdUpdateView.as_view(), name="ad_update"),
    path("ad/<int:pk>/delete/", ads.AdDeleteView.as_view(), name="ad_delete"),
    path("ad/<int:pk>/upload_image/", ads.AdImageUpdateView.as_view(), name="ad_upload_image"),
    path("ad/<int:pk>/", ads.AdDetailView.as_view(), name="ad"),
    path("ad/", ads.AdView.as_view(), name="ads_all"),
    path("ads/", ads.AdListView.as_view(), name="ads_list"),  # just for a test to learn ListView

    # categories & locations
    path("", include(router.urls)),

    # user
    path("users/create/", users.UserCreateAPIView.as_view(), name="api_users_create"),
    path("users/<int:pk>/delete/", users.UserDeleteAPIView.as_view(), name="api_users_delete"),
    path("users/<int:pk>/update/", users.UserUpdateAPIView.as_view(), name="api_users_update"),
    path("users/", users.UserListAPIView.as_view(), name="api_users_all"),
    path("users/<int:pk>/", users.UserAPIView.as_view(), name="api_users"),

    # additional urls
    path("ad/html/<int:pk>/", ads.AdHTMLDetailView.as_view(), name="ad_http_detail"),
    path("ad/html/", ads.AdHTMLView.as_view(), name="ad_http"),
]


