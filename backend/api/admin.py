from django.contrib import admin
from .models import (
    Profile,
    Products,
    ProductVariant,
    ProductImage,
    ProductCategory,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Payment,
)

admin.site.register(Profile)
admin.site.register(Products)
admin.site.register(ProductVariant)
admin.site.register(ProductImage)
admin.site.register(ProductCategory)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
