from django.test import TestCase
from ..models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.profile = Profile.objects.create(user=self.user, address="test address", city="test city", state="test state", zip_code="2222")
    def test_create_profile(self):
        self.assertEqual(self.profile.address, "test address")

class ProductTest(TestCase):
    def setUp(self):
        self.product = Products.objects.create(name="Test Product", description="test desc", general_info="test general info")
        self.category = ProductCategory.objects.create(category="test cat")
        self.product.category.add(self.category)
        self.product.save()
    def test_create_product(self):
        self.assertEqual(self.product.name, "Test Product")

