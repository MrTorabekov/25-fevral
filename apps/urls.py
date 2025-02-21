from django.urls import path

from apps.views import RegisterApiView, LoginApiView, UserUpdateView, BrandAPI, CategoryAPI, ProductAPI

urlpatterns = [
    path("register/", RegisterApiView.as_view(), name="register"),
    path("user//<int:pk>/update", UserUpdateView.as_view(), name='user-update'),
    path("brand/", BrandAPI.as_view(), name="brand"),
    path("category/", CategoryAPI.as_view(), name="category"),
    path("product/", ProductAPI.as_view(), name="product"),
    path("login/", LoginApiView.as_view(), name="login"),
]