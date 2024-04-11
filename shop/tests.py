from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from .models import Product, Order, OrderDetail

User = get_user_model()

class ProductAPITests(APITestCase):
    def setUp(self):
        Product.objects.create(name="Test Product", price=10.99, stock_quantity=100)

    def test_view_product_list(self):
        """
        Ensure we can retrieve the product list.
        """
        url = reverse('product-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Test Product")

class UserAPITests(APITestCase):
    def test_create_user(self):
        """
        Ensure we can create a new user.
        """
        url = reverse('user-list')
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpass123', 'role': 'customer'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

class OrderAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.product = Product.objects.create(name="Test Product", price=10.99, stock_quantity=100)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_place_order(self):
        """
        Ensure we can place an order for a product.
        """
        order_url = reverse('order-list')
        order_data = {'user': self.user.id, 'order_date': '2023-01-01T00:00:00Z', 'status': 'Placed', 'total_price': 10.99}
        order_response = self.client.post(order_url, order_data, format='json')
        self.assertEqual(order_response.status_code, status.HTTP_201_CREATED)

        order_detail_url = reverse('orderdetail-list')
        order_detail_data = {'order': order_response.data['id'], 'product': self.product.id, 'quantity': 1, 'price_at_purchase': 10.99}
        order_detail_response = self.client.post(order_detail_url, order_detail_data, format='json')
        self.assertEqual(order_detail_response.status_code, status.HTTP_201_CREATED)
