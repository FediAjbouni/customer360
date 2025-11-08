from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Customer
from .forms import CustomerForm


class CustomerModelTest(TestCase):
    """Test cases for Customer model."""

    def setUp(self):
        self.customer_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '+1234567890',
            'address': '123 Main St, City, State',
            'social_media': '@johndoe'
        }

    def test_customer_creation(self):
        """Test creating a customer with valid data."""
        customer = Customer.objects.create(**self.customer_data)
        self.assertEqual(customer.name, 'John Doe')
        self.assertEqual(customer.email, 'john.doe@example.com')
        self.assertTrue(customer.is_active)
        self.assertIsNotNone(customer.created_at)

    def test_customer_str_representation(self):
        """Test string representation of customer."""
        customer = Customer.objects.create(**self.customer_data)
        expected_str = f"{customer.name} ({customer.email})"
        self.assertEqual(str(customer), expected_str)

    def test_email_uniqueness(self):
        """Test that email must be unique."""
        Customer.objects.create(**self.customer_data)
        
        # Try to create another customer with same email
        with self.assertRaises(IntegrityError):
            Customer.objects.create(
                name='Jane Doe',
                email='john.doe@example.com',  # Same email
                phone='+0987654321',
                address='456 Oak St, City, State'
            )

    def test_phone_validation(self):
        """Test phone number validation."""
        # Valid phone numbers
        valid_phones = ['+1234567890', '1234567890', '+12345678901234']
        for phone in valid_phones:
            customer_data = self.customer_data.copy()
            customer_data['phone'] = phone
            customer_data['email'] = f'test{phone}@example.com'
            customer = Customer(**customer_data)
            customer.full_clean()  # This should not raise ValidationError

    def test_interaction_count_property(self):
        """Test interaction_count property."""
        customer = Customer.objects.create(**self.customer_data)
        self.assertEqual(customer.interaction_count, 0)


class CustomerFormTest(TestCase):
    """Test cases for CustomerForm."""

    def setUp(self):
        self.valid_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '+1234567890',
            'address': '123 Main St, City, State',
            'social_media': '@johndoe'
        }

    def test_valid_form(self):
        """Test form with valid data."""
        form = CustomerForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_required_fields(self):
        """Test that required fields are validated."""
        form = CustomerForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('phone', form.errors)
        self.assertIn('address', form.errors)

    def test_name_validation(self):
        """Test name field validation."""
        # Test short name
        data = self.valid_data.copy()
        data['name'] = 'A'
        form = CustomerForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_email_uniqueness_validation(self):
        """Test email uniqueness validation in form."""
        # Create a customer first
        Customer.objects.create(**self.valid_data)
        
        # Try to create another with same email
        form = CustomerForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_social_media_cleaning(self):
        """Test social media field cleaning."""
        data = self.valid_data.copy()
        data['social_media'] = 'johndoe'  # Without @
        form = CustomerForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['social_media'], '@johndoe')


class CustomerViewTest(TestCase):
    """Test cases for Customer views."""

    def setUp(self):
        self.client = Client()
        self.customer = Customer.objects.create(
            name='John Doe',
            email='john.doe@example.com',
            phone='+1234567890',
            address='123 Main St, City, State'
        )

    def test_customer_list_view(self):
        """Test customer list view."""
        url = reverse('customer_management:customer_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')

    def test_customer_detail_view(self):
        """Test customer detail view."""
        url = reverse('customer_management:customer_detail', kwargs={'pk': self.customer.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')

    def test_customer_create_view_get(self):
        """Test customer create view GET request."""
        url = reverse('customer_management:customer_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_customer_create_view_post(self):
        """Test customer create view POST request."""
        url = reverse('customer_management:customer_create')
        data = {
            'name': 'Jane Doe',
            'email': 'jane.doe@example.com',
            'phone': '+0987654321',
            'address': '456 Oak St, City, State'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Customer.objects.filter(email='jane.doe@example.com').exists())

    def test_customer_update_view(self):
        """Test customer update view."""
        url = reverse('customer_management:customer_update', kwargs={'pk': self.customer.pk})
        data = {
            'name': 'John Updated',
            'email': 'john.doe@example.com',
            'phone': '+1234567890',
            'address': '123 Main St, City, State'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        
        # Check if customer was updated
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.name, 'John Updated')

    def test_customer_search(self):
        """Test customer search functionality."""
        url = reverse('customer_management:customer_list')
        response = self.client.get(url, {'search_query': 'John'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')

    def test_customer_search_api(self):
        """Test customer search API."""
        url = reverse('customer_management:customer_search_api')
        response = self.client.get(url, {'q': 'John'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('customers', data)
        self.assertEqual(len(data['customers']), 1)
        self.assertEqual(data['customers'][0]['name'], 'John Doe')