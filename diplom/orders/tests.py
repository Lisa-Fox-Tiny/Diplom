from orders.models import Shop, Contact, User
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
import json


class TestRegisterAccount(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_account_success(self):
        url = reverse('user-register')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password': 'StrongPassword123',
            'company': 'Example Company',
            'position': 'Manager'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['Status'], True)

    def test_register_account_missing_arguments(self):
        url = reverse('user-register')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'company': 'Example Company',
            'position': 'Manager'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['Status'], False)
        self.assertIn('Errors', response.data)

    def test_register_account_weak_password(self):
        url = reverse('user-register')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password': 'weak',
            'company': 'Example Company',
            'position': 'Manager'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['Status'], False)
        self.assertIn('Errors', response.data)


class TestAccountAPIViews(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_confirm_account_valid_token(self):
        user = User.objects.create_user(username='test_user', email='test@example.com', password='TestPassword123')
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        url = reverse('confirm-account')
        data = {
            'email': user.email,
            'token': token
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.get(email='test@example.com').is_active)

    def test_confirm_account_invalid_token(self):
        url = reverse('confirm-account')
        data = {
            'email': 'test@example.com',
            'token': 'invalid_token'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(json.loads(response.content)['Status'])

    def test_account_details_authenticated(self):
        user = User.objects.create_user(username='test_user', email='test@example.com', password='TestPassword123')
        self.client.force_authenticate(user=user)
        url = reverse('account-details')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['email'], 'test@example.com')

    def test_account_details_unauthenticated(self):
        url = reverse('account-details')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_account_valid_credentials(self):
        user = User.objects.create_user(username='test_user', email='test@example.com', password='TestPassword123')
        url = reverse('login-account')
        data = {
            'email': 'test@example.com',
            'password': 'TestPassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(json.loads(response.content)['Status'])
        self.assertIn('Token', json.loads(response.content))

    def test_login_account_invalid_credentials(self):
        url = reverse('login-account')
        data = {
            'email': 'test@example.com',
            'password': 'invalid_password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(json.loads(response.content)['Status'])


class TestPartnerAPIViews(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_partner_update_valid_data(self):
        user = User.objects.create_user(username='test_user', email='test@example.com', password='TestPassword123')
        user.type = 'shop'
        user.save()
        self.client.force_authenticate(user=user)
        url = reverse('partner-update')
        data = {
            'url': 'https://example.com/data.yaml'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(json.loads(response.content)['Status'])

    def test_partner_state_valid_data(self):
        user = User.objects.create_user(username='test_user', email='test@example.com', password='TestPassword123')
        user.type = 'shop'
        user.save()
        self.client.force_authenticate(user=user)
        url = reverse('partner-state')
        data = {
            'state': 'True'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(json.loads(response.content)['Status'])

    def test_partner_orders_authenticated(self):
        user = User.objects.create_user(username='test_user', email='test@example.com', password='TestPassword123')
        user.type = 'shop'
        user.save()
        self.client.force_authenticate(user=user)
        url = reverse('partner-orders')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestContactAPIViews(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_contact_view_authenticated(self):
        user = User.objects.create_user(username='test_user', email='test@example.com', password='TestPassword123')
        self.client.force_authenticate(user=user)
        url = reverse('contact')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_contact_view_unauthenticated(self):
        url = reverse('contact')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_contact_valid_data(self):
        user = User.objects.create_user(username='test_user', email='test@example.com', password='TestPassword123')
        self.client.force_authenticate(user=user)
        url = reverse('contact')
        data = {
            'city': 'Test City',
            'street': 'Test Street',
            'phone': '1234567890'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(json.loads(response.content)['Status'])

    def test_update_contact_valid_data(self):
        user = User.objects.create_user(username='test_user', email='test@example.com', password='TestPassword123')
        self.client.force_authenticate(user=user)
        contact = Contact.objects.create(user=user, city='Test City', street='Test Street', phone='1234567890')
        url = reverse('contact')
        data = {
            'id': contact.id,
            'city': 'New City',
            'street': 'New Street',
            'phone': '9876543210'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(json.loads(response.content)['Status'])

    def test_delete_contact_valid_data(self):
        user = User.objects.create_user(username='test_user', email='test@example.com', password='TestPassword123')
        self.client.force_authenticate(user=user)
        contact = Contact.objects.create(user=user, city='Test City', street='Test Street', phone='1234567890')
        url = reverse('contact')
        data = {
            'items': str(contact.id)
        }
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(json.loads(response.content)['Status'])


class TestOrderAPIViews(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_order_view_authenticated(self):
        user = User.objects.create_user(username='test_user', email='test@example.com', password='TestPassword123')
        self.client.force_authenticate(user=user)
        url = reverse('order')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_view_unauthenticated(self):
        url = reverse('order')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_order_valid_data(self):
        user = User.objects.create_user(username='test_user', email='test@example.com', password='TestPassword123')
        self.client.force_authenticate(user=user)
        order = Order.objects.create(user=user)
        contact = Contact.objects.create(user=user, city='Test City', street='Test Street', phone='1234567890')
        url = reverse('order')
        data = {
            'id': order.id,
            'contact': contact.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(json.loads(response.content)['Status'])