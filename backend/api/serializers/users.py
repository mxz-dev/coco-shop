from rest_framework import serializers
from api.models import Profile, User, Cart, CartItem
from api.validators import validate_confirm_password, validate_email_uniqueness

class BaseUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'first_name', 'last_name', 'email']

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedIdentityField(view_name="user-detail", lookup_field="pk", read_only=True)
    class Meta:
        model = Profile
        fields = "__all__"


class UserRegisterationSerializer(BaseUserSerializer):
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm Password")
    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ['password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True, 'allow_blank': False}
        }

    def validate(self, attrs):
        validate_confirm_password(attrs.get('password'),  attrs.get('password2'))
        validate_email_uniqueness(attrs.get('email'), User)
        return attrs
    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'], first_name=validated_data.get('first_name', ''), last_name=validated_data.get('last_name', ''), email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user
    