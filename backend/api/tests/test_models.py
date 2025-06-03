from django.test import TestCase
from ..models import *
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import tempfile
import shutil
from django.test import override_settings
import io
from django.utils.timezone import datetime
User = get_user_model()
TEMP_MEDIA_ROOT = tempfile.mkdtemp()


def generate_test_image():
    image = Image.new("RGB", (100, 100), color="blue")
    byte_io = io.BytesIO()
    image.save(byte_io, format='JPEG')
    byte_io.seek(0)
    return SimpleUploadedFile("test.jpg", byte_io.read(), content_type="image/jpeg")    
class ProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.profile = Profile.objects.create(user=self.user, address="test address", city="test city", state="test state", zip_code="2222")
    def test_create_profile(self):
        self.assertEqual(self.profile.address, "test address")
@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ProductTest(TestCase):
    def setUp(self):
        self.product = Products.objects.create(name="Test Product", description="test desc", general_info="test general info")
        self.category = ProductCategory.objects.create(category="test cat")
        self.product.category.add(self.category)
        self.product.save()
        self.variant = ProductVariant.objects.create(product=self.product, sku="test-sku", color="red", size="XS", price=22.00, discount_price=0, stock=2, is_active=True)

    def test_create_product(self):
        self.assertEqual(self.product.name, "Test Product")
    
    def test_product_variant(self):
        self.assertEqual(self.variant.sku, "test-sku")

    def test_product_image(self):
        image_file =  generate_test_image()
        self.image = ProductImage.objects.create(product=self.variant, image=image_file, is_main=True)
        self.assertTrue(self.image.image.name.startswith("product/"))
    def tearDown(self):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

class CartTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.cart = Cart.objects.create(user=self.user, is_active=True)
    
        # create product for test cartitem .
        self.product = Products.objects.create(name="Test Product", description="test desc", general_info="test general info")
        self.category = ProductCategory.objects.create(category="test cat")
        self.product.category.add(self.category)
        self.product.save()
        self.variant = ProductVariant.objects.create(product=self.product, sku="test-sku", color="red", size="XS", price=22.00, discount_price=0, stock=2, is_active=True)

    def test_cart(self):
        self.assertTrue(self.cart.is_active)
    
    def test_cart_item(self):
        self.cart_item = CartItem.objects.create(cart=self.cart, variant=self.variant, quantity=10)
        self.assertEqual(self.cart_item.variant, self.variant)

class OrderTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.order = Order.objects.create(user=self.user, status="PROCESSING", total_price=100.00, is_paid=False, paid_at=datetime.now())
        # create product for test order item .
        self.product = Products.objects.create(name="Test Product", description="test desc", general_info="test general info")
        self.category = ProductCategory.objects.create(category="test cat")
        self.product.category.add(self.category)
        self.product.save()
        self.variant = ProductVariant.objects.create(product=self.product, sku="test-sku", color="red", size="XS", price=22.00, discount_price=0, stock=2, is_active=True)

    def test_order_item(self):
        self.order_item = OrderItem.objects.create(order=self.order, product=self.variant, quantity=10, price_at_perchase=100)
        self.assertEqual(self.order_item.product, self.variant)
