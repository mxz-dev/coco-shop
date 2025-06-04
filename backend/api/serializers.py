from rest_framework import serializers
from .models import Profile, User, Products, ProductVariant, ProductCategory, ProductImage

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'first_name', 'last_name', 'email']

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedIdentityField(view_name="user-detail", lookup_field="pk", many=True, read_only=True)
    class Meta:
        model = Profile
        exclude = ['created_at', 'updated_at']

class ProductCategorySerilizer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"

class ProductImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image","is_main"]
    
class ProductVariantSerializer(serializers.HyperlinkedModelSerializer):
    product = serializers.HyperlinkedRelatedField(view_name="products-detail", lookup_field="slug", read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = ProductVariant
        fields = "__all__"


class ProductImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id","product","image","is_main"]

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = ProductCategorySerilizer(many=True, read_only=True)
    variant = ProductVariantSerializer(many=True,read_only=True) 
    class Meta:
        model = Products
        fields = "__all__"
        extra_kwargs = {
            'url': {'view_name': 'products-detail', 'lookup_field': 'slug'}
        }