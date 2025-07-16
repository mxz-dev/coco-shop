from rest_framework import serializers
from api.models import Cart, CartItem, Order, OrderItem

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
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'id',
            'variant',
            'quantity',
            'price_at_perchase',
        ]
        read_only_fields = ['id','price_at_perchase']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = [
            'items',
            'id',
            'user',
            'status',
            'total_price',
            'is_paid',
            'paid_at',
            'created_at'
        ]
        read_only_fields = ['user','status','is_paid','paid_at','total_price','created_at']

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        user = self.context["request"].user
        validated_data.pop("user", None) 
        order = Order.objects.create(user=user, total_price=0, **validated_data)

        total_price = 0

        for item_data in items_data:
            product_variant = item_data["variant"]
            quantity = item_data["quantity"]
            price = product_variant.price
            if product_variant.discount_price:
                price = product_variant.discount_price
            total_price += price * quantity
            OrderItem.objects.create(
                order=order,
                variant=product_variant,
                quantity=quantity,
                price_at_perchase=price
            )

        order.total_price = total_price
        order.save()

        return order