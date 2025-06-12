from ast import arg
from django.db import models
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify
User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, related_name="user_profile", on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatar/", null=True, blank=True)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=50)
    country = CountryField(blank_label='(Select country)', null=True, blank=True)
    state = models.CharField(max_length=100)
    zip_code = models.PositiveIntegerField()
    phone = PhoneNumberField(blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    @property
    def full_name(self):
        return self.user.get_full_name()
    @property
    def email(self):
        return self.user.email
    
    def __str__(self):
        return f"{self.user.username} Profile."
    class Meta:
        verbose_name_plural = "User Profiles"

class ProductCategory(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category
    class Meta:
        verbose_name_plural = "Product Categories"

class Products(models.Model):
    name = models.CharField(max_length=400)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    general_info = models.TextField(max_length=600)
    categories = models.ManyToManyField(ProductCategory)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
           self.slug = slugify(self.name)
        super(Products, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Products"
        ordering = ['-created_at']
        
class ProductVariant(models.Model):
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
        ('XXXL', 'Tripel Extra Large'),

    ]
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="variant")
    sku = models.CharField(unique=True, blank=True, max_length=120)
    color = models.CharField(max_length=10, blank=True, null=True)
    size = models.CharField(choices=SIZE_CHOICES, blank=True, null=True, max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    @property
    def discount_percent(self):
        if self.discount_price and self.discount_price < self.price:
            discount = (self.price - self.discount_price) / self.price * 100
            return round(discount, 2)  # Rounded to 2 decimal places
        return 0
    def __str__(self):
        return f"Variant for {self.product.name}"

class ProductImage(models.Model):
    product = models.ForeignKey(ProductVariant, related_name="images", on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to="product/", null=True)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"image for {self.product.product.name} product"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Cart for {self.user.username}"
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'variant')  # Prevents duplicate variant entries in a single cart
    def __str__(self):
        return f"Item {self.variant} in {self.cart.user.username}'s cart"
class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order")
    status = models.CharField(choices=STATUS_CHOICES, default="PENDING", max_length=25)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"order for {self.user.username} - {self.status}"
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item')
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_perchase = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"order item for {self.order.user.username} - {self.product.product.name} ({self.quantity})"
class Payment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('CANCELLED', 'Cancelled'),
        ('SUCCESSFUL', 'Successful')
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order')
    status = models.CharField(choices=STATUS_CHOICES, default="PENDING", max_length=25)
    ref_id = models.PositiveIntegerField()
    card_pan = models.CharField(max_length=20)
    fee_type = models.CharField(max_length=100)
    fee = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"payment info for {self.order.user}"