from django.test import TestCase
from django.urls import reverse

class ImageTestClass(TestCase):
    def test_generate_qr(self):
        response = self.client.get(reverse('generate_qr'), {'data': 'https://247media.uk'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'image/png')
