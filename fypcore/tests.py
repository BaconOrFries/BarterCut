from django.test import TestCase, Client
from django.urls import reverse
from .models import AppUser, Transaction
from .form import CreateUserForm, LoginForm
from django.contrib.auth.models import User

class ViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_index_view(self):
        client = Client()
        response = client.get(reverse('fypcore:index'))
        self.assertEqual(response.status_code, 200)

    def test_contact_view(self):
        client = Client()
        response = client.get(reverse('fypcore:contact'))
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        client = Client()
        response = client.get(reverse('fypcore:register'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        client = Client()
        response = client.get(reverse('fypcore:login'))
        self.assertEqual(response.status_code, 200)

    def test_terms_view(self):
        client = Client()
        response = client.get(reverse('fypcore:terms'))
        self.assertEqual(response.status_code, 200)

    def test_policy_view(self):
        client = Client()
        response = client.get(reverse('fypcore:policy'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        client = Client()
        response = client.get(reverse('fypcore:logout'))
        self.assertEqual(response.status_code, 302) 

    def test_authenticated_user_registration(self):
        client = Client()
        client.login(username='testuser', password='testpassword')
        response = client.get(reverse('fypcore:register'))
        self.assertEqual(response.status_code, 302) 

    def test_unauthenticated_user_registration(self):
        client = Client()
        response = client.get(reverse('fypcore:register'))
        self.assertEqual(response.status_code, 200)

class FormsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser2', password='testpassword')
    def test_create_user_form_valid(self):
        form = CreateUserForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        self.assertTrue(form.is_valid())

    def test_create_user_form_invalid(self):
        form = CreateUserForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'wrongpassword', 
        })
        self.assertFalse(form.is_valid())

    def test_login_form_valid(self):
        form = LoginForm(data={
            'username': 'testuser2',
            'password': 'testpassword',
        })
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        form = LoginForm(data={
            'username': 'testuser2',
            'password': 'wrongpassword', 
        })
        self.assertFalse(form.is_valid())

class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_appuser_creation(self):
        app_user = AppUser.objects.create(user=self.user, point=20)
        self.assertEqual(app_user.user.username, 'testuser')
        self.assertEqual(app_user.point, 20)

    def test_transaction_creation(self):
        transaction = Transaction.objects.create(user=self.user, status='pending')
        self.assertEqual(transaction.user.username, 'testuser')
        self.assertEqual(transaction.status, 'pending')
