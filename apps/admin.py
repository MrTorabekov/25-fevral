from django.contrib import admin
from apps.models import User, Address, Brand, Category, Product, ProductImage,\
                       Supplier, Order, OrderItem, CartItem, Wishlist, Review, \
                       Comment, Deal

@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ('id', 'roles', 'first_name', 'last_name', 'email')

@admin.register(Address)
class Address(admin.ModelAdmin):
    list_display = ('id', 'address_line1', 'address_line2', 'city', 'state', 'zip_code', 'country')

@admin.register(Brand)
class Brand(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')

@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price', 'category', 'brand')


@admin.register(Wishlist)
class Wishlist(admin.ModelAdmin):
    list_display = ('id','user','product','created_at')

admin.site.register(Supplier)