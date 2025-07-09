from rest_framework import serializers
from api.models import Products, ProductVariant, ProductCategory, ProductImage, Cart, CartItem
from api.validators import validate_image
from .users import BaseUserSerializer
class ProductCategorySerilizer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ["category"]

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
    def validate(self, attrs):
        image = attrs.get('image')
        if image:
            validate_image(image)
        return attrs
class ProductVariantMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'sku']
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    categories = ProductCategorySerilizer(many=True, read_only=True, )
    variant = ProductVariantMiniSerializer(many=True,read_only=True) 
    class Meta:
        model = Products
        fields = "__all__"
        extra_kwargs = {
            'url': {'view_name': 'products-detail', 'lookup_field': 'slug'}
        }

class CartItemSerializer(serializers.ModelSerializer):
    variant_name = serializers.CharField(source='variant.name', read_only=True)
    variant_price = serializers.DecimalField(
        source='variant.price', 
        read_only=True, 
        max_digits=10, 
        decimal_places=2
    )
    variant_image = serializers.ImageField(source='variant.image', read_only=True)

    class Meta:
        model = CartItem
        fields = [
            'id', 
            'variant', 
            'variant_name', 
            'variant_price', 
            'variant_image',
            'quantity', 
            'added_at'
        ]
        extra_kwargs = {
            'variant': {'required': True},
            'quantity': {'min_value': 1}
        }

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            'id', 
            'user', 
            'is_active', 
            'created_at', 
            'updated_at', 
            'items', 
            'total'
        ]
        read_only_fields = ['user']

    def get_total(self, obj):
        return sum(
            item.variant.price * item.quantity 
            for item in obj.items.all()
        )