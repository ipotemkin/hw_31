from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from ads.views import ads, users, categories, selections
from django.urls import path, include

router = DefaultRouter()  # SimpleRouter
router.register('cats', categories.CatAPIViewSet)
urlpatterns = [
    # ad
    # path("ad/<int:pk>/update/", ads.AdUpdateView.as_view(), name="ad_update"),
    # path("ad/<int:pk>/delete/", ads.AdDeleteView.as_view(), name="ad_delete"),
    # path("ad/<int:pk>/upload_image/", ads.AdImageUpdateView.as_view(), name="ad_upload_image"),
    # path("ad/<int:pk>/", ads.AdDetailView.as_view(), name="ad"),
    # path("ad/", ads.AdView.as_view(), name="ads_all"),
    # path("ads/", ads.AdListView.as_view(), name="ads_list"),  # just for a test to learn ListView
    path("ads/<int:pk>/", ads.AdAPIView.as_view()),
    path("ads/", ads.AdListCreateAPIView.as_view()),
    # path("ads/create/", ads.AdCreateAPIView.as_view()),
    path("ads/<int:pk>/update/", ads.AdUpdateAPIView.as_view()),
    path("ads/<int:pk>/delete/", ads.AdDeleteAPIView.as_view()),

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

    # tokens
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),

    # selections
    path("selections/create/", selections.SelectionCreateAPIView.as_view()),
    path("selections/<int:pk>/", selections.SelectionAPIView.as_view()),
    path("selections/", selections.SelectionListAPIView.as_view()),
    path("selections/<int:pk>/update/", selections.SelectionUpdateAPIView.as_view()),
    path("selections/<int:pk>/delete/", selections.SelectionDeleteAPIView.as_view()),

]

router.register('locations', users.LocAPIViewSet)
