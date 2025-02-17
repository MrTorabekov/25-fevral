
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    role = [
            ('admin', 'Admin'),
            ('user', 'User'),
            ('customer', 'Customer')
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(_("username"), max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.IntegerField(max_length=15, null=True, blank=True)
    roles = models.CharField(max_length=50, choices=role, default='user')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name





class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)



class Brand(models.Model):
    name = models.CharField(max_length=255)



class Category(models.Model):
    CATEGORY_CHOICES = [
        ('mobile_accessory', 'Mobile Accessory'),
        ('electronics', 'Electronics'),
        ('smartphones', 'Smartphones'),
        ('modern_tech', 'Modern Tech'),
    ]
    name = models.CharField(max_length=255)
    # parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES)






class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()



class Supplier(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    verified = models.BooleanField(default=False)





class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)




class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()





class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)




class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)




class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=50, choices=[('visible', 'Visible'), ('hidden', 'Hidden')])
    created_at = models.DateTimeField(auto_now_add=True)




class Deal(models.Model):
    DISCOUNT_CHOICES = [
        ('no_discount', 'No Discount'),
        ('10%', '10%'),
        ('15%', '15%'),
        ('25%', '25%'),
        ('40%', '40%'),
    ]
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    phone_name = models.CharField(_('phone name'), max_length=30, blank=True)
    img = models.ImageField(_('image'))
    discount = models.CharField(max_length=20, choices=DISCOUNT_CHOICES, default='no_discount')
    discount_time = models.TimeField()

    def __str__(self):
        return str(self.discount_time)