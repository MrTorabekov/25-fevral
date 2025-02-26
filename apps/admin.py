from django.contrib import admin
from apps.models import User, Address, Brand, Category, Product, ProductImage,\
                       Supplier, Order, OrderItem, CartItem, Wishlist, Review, \
                       Comment, Deal

admin.site.register(User)

admin.site.register(Address)

admin.site.register(Brand)

admin.site.register(Category)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "price", "stock")

admin.site.register(ProductImage)

admin.site.register(Review)

admin.site.register(Wishlist)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_price", "status")

admin.site.register(Comment)

admin.site.register(Deal)

admin.site.register(OrderItem)

admin.site.register(CartItem)