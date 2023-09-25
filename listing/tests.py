from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Item
from django.contrib.auth.models import User
from .form import CreateListingForm, EditListingForm

class CreateListingFormTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Furniture')

    def test_create_listing_form_valid(self):
        form_data = {
            'category': self.category.id,  # Replace with a valid category ID
            'name': 'Test Item',
            'description': 'This is a test item.',
            'point': 10,
        }
        form = CreateListingForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_listing_form_invalid(self):
        form_data = {
            'category': 'Test',  # Replace with a valid category ID
            'name': '',  # Invalid, name is required
            'description': 'This is a test item.',
            'point': -5,  # Invalid, points should be positive
        }
        form = CreateListingForm(data=form_data)
        self.assertFalse(form.is_valid())

class EditListingFormTest(TestCase):
    def test_edit_listing_form_valid(self):
        form_data = {
            'category': 'Furniture',  # Replace with a valid category ID
            'name': 'Updated Test Item',  # Modify fields as needed
            'description': 'Updated description.',
            'point': 20,
        }
        form = EditListingForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_edit_listing_form_invalid(self):
        form_data = {
            'category': 1,  # Replace with a valid category ID
            'name': '',  # Invalid, name is required
            'description': 'Updated description.',
            'point': -5,  # Invalid, points should be positive
        }
        form = EditListingForm(data=form_data)
        self.assertFalse(form.is_valid())

class ListingViewsTest(TestCase):
    def setUp(self):
        categories = "Furniture"
        name = "Test Item"
        description = "This is a test item"
        point = "10"

    def test_create_listing_view(self):
        client = Client()
        user = User.objects.create_user(username='testuser', password='testpassword')
        client.login(username='testuser', password='testpassword')

        response = client.post(reverse('listing:create_listing'), {
            'category': 'Furniture',  # Replace with a valid category ID
            'name': 'Test Item',
            'description': 'This is a test item.',
            'point': 10,
        })
        self.assertEqual(response.status_code, 200)