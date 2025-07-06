from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse
import json

class HealthCheckTestCase(TestCase):
    def test_health_check_endpoint(self):
        """Test that the health check endpoint returns the expected response."""
        response = self.client.get(reverse('health_check'))
        self.assertEqual(response.status_code, 200)
        
        # Parse JSON response
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['service'], 'ebast')

    def test_health_check_response_type(self):
        """Test that the health check endpoint returns JSON."""
        response = self.client.get(reverse('health_check'))
        self.assertEqual(response['Content-Type'], 'application/json')

class HomePageTestCase(TestCase):
    def test_home_page_loads(self):
        """Test that the home page loads successfully."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
