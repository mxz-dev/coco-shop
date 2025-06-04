from django.urls import path, include
from .views import UserViewSet, ProductViewSet, ProductVariantViewSet, ProductImageUploadViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='user')
router.register(r'product', ProductViewSet, basename='products')
router.register(r'product-varaint', ProductVariantViewSet, basename='productvariant')
router.register(r'product-image-upload', ProductImageUploadViewSet, basename='productimage')

urlpatterns = [ path('', include(router.urls)) ] 