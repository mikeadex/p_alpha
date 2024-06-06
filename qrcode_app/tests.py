from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .views import QRCodeTemplate
from qrcode_app.hashers import CustomHasher
from django.core import mail


class ImageTestClass(TestCase):
    def test_generate_qr(self):
        response = self.client.get(reverse('generate_qr'), {'data': 'https://247media.uk'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'image/png')


class AuthenticationTests(TestCase):
    def test_user_registration(self ):
        response = self.client.post(reverse('account_signup'),
        {
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())


    def test_user_login(self ):
        User.objects.create_user(email='test@example.com', password='testpassword')
        response = self.client.post(reverse('account_login'), {
            'login': 'test@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)


class CustomizedQRCodeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.template = QRCodeTemplate.objects.create(
            name='Test Template',
            design='{}',  # Replace with actual design format
            color='#000000',
            user=self.user
        )

    def test_generate_custom_qr(self):
        self.client.login(email='test@example.com', password='testpassword')
        response = self.client.get(reverse('generate_custom_qr'), {
            'template_id': self.template.id,
            'data': 'https://example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/png')


class BusinessInfoTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_complete_business_info(self):
        response = self.client.post(reverse('complete_business_info'), {
            'business_name': 'Test Business',
            'business_address': '123 Test St',
            'contact_number': '1234567890',
        })
        self.assertEqual(response.status_code, 302)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.business_name, 'Test Business')


class PasswordHasherTests(TestCase):
    def test_custom_password_hasher(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.assertTrue(user.check_password('testpassword'))

        hasher = CustomHasher()
        encoded_password = hasher.encode('testpassword', 'salt')
        self.assertTrue(hasher.verify('testpassword', encoded_password))


class SecurityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_login_notification(self):
        self.client.login(username='testuser', password='testpassword')
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('New Login Detected', mail.outbox[0].subject)

    def test_two_factor_auth(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('two_factor'))
        self.assertEqual(len(mail.outbox), 1)
        code = self.client.session['2fa_code']
        response = self.client.post(reverse('two_factor'), {'code': code})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))


