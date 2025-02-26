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
    phone_number = models.CharField(max_length=30, unique=True)
    roles = models.CharField(max_length=50, choices=role, default='user')
    updated_at = models.DateTimeField(auto_now=True)

    def str(self):
        return self.first_name

class Address(models.Model):
    # Foydalanuvchi manzillari
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

class Brand(models.Model):
    # Mahsulot brendlari
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)  # 🔹 null=True, blank=True qo‘shildi
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    # Mahsulot rasmlari
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_url = models.ImageField(upload_to='avatars/')

    def __str__(self):
        return self.product.name

class Supplier(models.Model):
    # Yetkazib beruvchilar
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    verified = models.BooleanField(default=False)

class Order(models.Model):
    # Buyurtmalar modeli
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    created_at = models.DateField(_('create_at'), auto_now_add=True)
    updated_at = models.DateField(_('update_at'), auto_now=True)

    def __str__(self):
        return self.user.username if self.user else "No User"

class OrderItem(models.Model):
    # Buyurtma ichidagi mahsulotlar
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class CartItem(models.Model):
    # Savatchadagi mahsulotlar
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Wishlist(models.Model):
    # Istaklar ro‘yxati (Wishlist)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

class Review(models.Model):
    # Foydalanuvchilar tomonidan mahsulot baholash
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=50, choices=[('visible', 'Visible'), ('hidden', 'Hidden')])
    created_at = models.DateField(_('created_at'), auto_now=True)

class Deal(models.Model):
    # Chegirmali mahsulotlar (aksiya)
    DISCOUNT_CHOICES = [
        ('no_discount', 'No Discount'),
        ('10%', '10%'),
        ('15%', '15%'),
        ('25%', '25%'),
        ('40%', '40%'),
    ]
    start_time = models.DateField()  # Aksiya boshlanish vaqti
    end_time = models.DateField()  # Aksiya tugash vaqti
    phone_name = models.CharField(_('phone name'), max_length=30, blank=True)  # Aksiya uchun mahsulot nomi
    img = models.ImageField(_('image'))  # Aksiya uchun rasm
    discount = models.CharField(max_length=20, choices=DISCOUNT_CHOICES, default='no_discount')  # Chegirma foizi
    discount_time = models.TimeField()  # Chegirma davomiyligi

    def __int__(self):
        return self.phone_name