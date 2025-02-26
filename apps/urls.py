from django.urls import path

from apps.views import RegisterApiView, LoginApiView, UserUpdateView, BrandAPI, CategoryAPI, ProductAPI, \
    ProductImageAPIView, ProductUpdateAPIView, ProductDeleteAPIView, ReviewAPIView, SuplierDetailAPIView, \
    SuplierCreateAPIView, OrderListView, OrderDetailView, WishlistListCreateView, CommentListAPIView, CommentDetailView, \
    CartItemListCreateAPIView, CartItemDetailAPIView, DealAPIView

urlpatterns = [
    path("register", RegisterApiView.as_view(), name="register"),
    path("user/<int:pk>/update", UserUpdateView.as_view(), name='user-update'),
    path("product/<int:pk>/update", ProductUpdateAPIView.as_view(), name='product-update'),
    path("product/<int:pk>/delete", ProductDeleteAPIView.as_view(), name='product-delete'),
    path('wishlist/', WishlistListCreateView.as_view(), name='wishlist-list'),
    path('supplier/<int:pk>/', SuplierDetailAPIView.as_view(), name='supplier-detail'),
    path('cart/', CartItemListCreateAPIView.as_view(), name='cart-list-create'),
    path('cart/<int:pk>/', CartItemDetailAPIView.as_view(), name='cart-detail'),
    path('deal', DealAPIView.as_view(), name='deal-list'),
    path('comments/', CommentListAPIView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('orders', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='orders-detail'),
    path('supplier/', SuplierCreateAPIView.as_view(), name='supplier-create'),
    path("productimg/", ProductImageAPIView.as_view(), name='product-image'),
    path("review/", ReviewAPIView.as_view(), name='review'),
    path("brand/", BrandAPI.as_view(), name="brand"),
    path("category/", CategoryAPI.as_view(), name="category"),
    path("product/", ProductAPI.as_view(), name="product"),
    path("login/", LoginApiView.as_view(), name="login"),
]