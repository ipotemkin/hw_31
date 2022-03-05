from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from ads.views import ads, users, categories, selections
from django.urls import path, include

router = DefaultRouter()  # SimpleRouter
router.register('cats', categories.CatAPIViewSet)
urlpatterns = [
    # ad
    path("ads/<int:pk>/update/", ads.AdUpdateAPIView.as_view()),
    path("ads/<int:pk>/delete/", ads.AdDeleteAPIView.as_view()),
    path("ads/<int:pk>/upload_image", ads.AdImageUpdateView.as_view()),
    path("ads/<int:pk>/", ads.AdAPIView.as_view()),
    path("ads/", ads.AdListCreateAPIView.as_view()),

    # categories & locations
    path("", include(router.urls)),

    # user
    path("users/create/", users.UserCreateAPIView.as_view(), name="api_users_create"),
    path("users/<int:pk>/delete/", users.UserDeleteAPIView.as_view(), name="api_users_delete"),
    path("users/<int:pk>/update/", users.UserUpdateAPIView.as_view(), name="api_users_update"),
    path("users/<int:pk>/", users.UserAPIView.as_view(), name="api_users"),
    path("users/token/refresh/", TokenRefreshView.as_view()),
    path("users/token/", TokenObtainPairView.as_view()),
    path("users/", users.UserListAPIView.as_view(), name="api_users_all"),

    # selections
    path("selections/create/", selections.SelectionCreateAPIView.as_view()),
    path("selections/<int:pk>/update/", selections.SelectionUpdateAPIView.as_view()),
    path("selections/<int:pk>/delete/", selections.SelectionDeleteAPIView.as_view()),
    path("selections/<int:pk>/", selections.SelectionAPIView.as_view()),
    path("selections/", selections.SelectionListAPIView.as_view()),

    # additional urls
    path("ads/html/<int:pk>/", ads.AdHTMLDetailView.as_view(), name="ad_http_detail"),
    path("ads/html/", ads.AdHTMLView.as_view(), name="ad_http"),
]

router.register('locations', users.LocAPIViewSet)
