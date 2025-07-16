from django.urls import path, include
from .views import UserViewSet, ProductViewSet, ProductVariantViewSet, ProductImageUploadViewSet, ProfileViewSet, UserRegisterationViewSet, CartItemViewSet, CartViewSet, OrderViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='user')
router.register(r'signup', UserRegisterationViewSet, basename='signup')
router.register(r'profile', ProfileViewSet, basename="profile")
router.register(r'product', ProductViewSet, basename='products')
router.register(r'product-varaint', ProductVariantViewSet, basename='productvariant')
router.register(r'product-image-upload', ProductImageUploadViewSet, basename='productimage')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'cart-items', CartItemViewSet, basename='cartitem')
router.register(r'order', OrderViewSet, basename="order")
urlpatterns = [ path('', include(router.urls)) ] 