from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse


class IndexViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_returns_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_uses_correct_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'core/index.html')


class HealthCheckViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('health_check')

    def test_healthy_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['database'], 'connected')

    def test_unhealthy_hides_error_detail(self):
        with patch('apps.core.views.connection') as mock_conn:
            mock_conn.cursor.side_effect = Exception(
                'FATAL: password authentication failed for user "postgres" host="db"'
            )
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 503)
        data = response.json()
        self.assertEqual(data['status'], 'unhealthy')
        self.assertNotIn('password', data.get('error', ''))
        self.assertNotIn('postgres', data.get('error', ''))
        self.assertNotIn('FATAL', data.get('error', ''))
