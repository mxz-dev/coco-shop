from rest_framework import serializers
from .models import Profile, User, Products, ProductVariant, ProductCategory, ProductImage

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'first_name', 'last_name', 'email']

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedIdentityField(view_name="user-detail", lookup_field="pk", read_only=True)
    class Meta:
        model = Profile
        fields = "__all__"

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

class UserRegisterationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm Password")
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "password", "password2"]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True, 'allow_blank': False}
        }
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists.")
        if password != password2:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'], first_name=validated_data.get('first_name', ''), last_name=validated_data.get('last_name', ''), email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user
    