from django.urls import path

from apps.views import RegisterApiView, LoginApiView, UserUpdateView, BrandAPI, CategoryAPI, ProductAPI, \
    ProductImageAPIView, ProductUpdateAPIView, ProductDeleteAPIView, ReviewAPIView, SuplierDetailAPIView, \
    SuplierCreateAPIView,WishlistListCreateView
urlpatterns = [
    path("register", RegisterApiView.as_view(), name="register"),
    path("user/<int:pk>/update", UserUpdateView.as_view(), name='user-update'),
    path("product/<int:pk>/update", ProductUpdateAPIView.as_view(), name='product-update'),
    path("product/<int:pk>/delete", ProductDeleteAPIView.as_view(), name='product-delete'),
    path('supplier/<int:pk>/', SuplierDetailAPIView.as_view(), name='supplier-detail'),
    path('supplier/', SuplierCreateAPIView.as_view(), name='supplier-create'),
    path("productimg/", ProductImageAPIView.as_view(), name='product-image'),
    path("review/", ReviewAPIView.as_view(), name='review'),
    path("brand/", BrandAPI.as_view(), name="brand"),
    path("category/", CategoryAPI.as_view(), name="category"),
    path("product/", ProductAPI.as_view(), name="product"),
    path("login/", LoginApiView.as_view(), name="login"),
    path('wishlist/', WishlistListCreateView.as_view(), name='wishlist-list'),
]
