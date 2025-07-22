from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import action

from .serializers.users import BaseUserSerializer, UserRegisterationSerializer, ProfileSerializer
from .serializers.product import ProductSerializer, ProductVariantSerializer, ProductImageUploadSerializer
from .serializers.checkout import CartSerializer, CartItemSerializer, OrderSerializer

from .models import Products, ProductVariant, ProductImage, Profile, Cart, CartItem, Order
from .permissions import IsProfileOwenerOrReadOnly

from .payments.zarinpal import zarinpal_payment, zarinpal_verify
User = get_user_model()

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = BaseUserSerializer
    permission_classes = [IsAuthenticated]

class UserRegisterationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterationSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User created successfully"
        }, status=201)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsProfileOwenerOrReadOnly]
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
class ProductVariantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProductImageUploadViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageUploadSerializer
    permission_classes = [IsAdminUser]

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).prefetch_related(
            'items__variant'
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def clear(self, request):
        cart = self.get_queryset().first()
        if cart:
            cart.items.all().delete()
            return Response({'status': 'cart cleared'})
        return Response(
            {'error': 'Cart not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(
            cart__user=self.request.user
        ).select_related('variant')

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        variant = serializer.validated_data['variant']
        item = CartItem.objects.get(cart=cart, variant=variant)

        if item:
            item.quantity += serializer.validated_data.get('quantity', 1)
            item.save()
        else:
            serializer.save(cart=cart)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id , format=None):

        order = get_object_or_404(Order, id=order_id, user=request.user)
        if order.is_paid:
            return Response({
                "message":"This order is already paid."
            }, status=status.HTTP_400_BAD_REQUEST)
        payment_url = zarinpal_payment(amount=order.total_price, description=f"پرداخت سفارش #{order.id}", email=request.user.email, mobile=request.user.profile.mobile)
        return Response({"payment_url":payment_url})
