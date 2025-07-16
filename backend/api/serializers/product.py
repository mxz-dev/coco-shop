from rest_framework import serializers
from api.models import Products, ProductVariant, ProductCategory, ProductImage
from api.validators import validate_image

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

