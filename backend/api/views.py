from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from .serializers import UserSerializer, ProductVariantSerializer, ProductSerializer, ProductImageUploadSerializer, ProfileSerializer
from django.contrib.auth import get_user_model
from .models import Products, ProductVariant, ProductImage, Profile
from .permissions import IsProfileOwenerOrReadOnly
User = get_user_model()
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsProfileOwenerOrReadOnly]
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'slug'
class ProductVariantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProductImageUploadViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageUploadSerializer
    permission_classes = [IsAdminUser]