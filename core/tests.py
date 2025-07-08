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

from .models import Operator, Kelompok

class KelompokUpdateViewTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.operator1 = Operator.objects.create(name="Test Operator 1", NIP="1234567890123456")
        self.operator2 = Operator.objects.create(name="Test Operator 2", NIP="2345678901234567")
        self.kelompok = Kelompok.objects.create(name=1, member=f"{self.operator1.pk},{self.operator2.pk}")

    def test_update_view_passes_existing_members(self):
        """Test that the update view passes existing_members to the template context"""
        url = reverse('core:kelompok_update', kwargs={'pk': self.kelompok.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('existing_members', response.context)
        self.assertEqual(response.context['existing_members'], [str(self.operator1.pk), str(self.operator2.pk)])

    def test_update_view_template_contains_existing_members_data(self):
        """Test that the template contains the existing_members data for JavaScript"""
        url = reverse('core:kelompok_update', kwargs={'pk': self.kelompok.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'existingMemberIds')
        self.assertContains(response, f"'{self.operator1.pk}'")
        self.assertContains(response, f"'{self.operator2.pk}'")

    def test_create_view_has_empty_existing_members(self):
        """Test that the create view has empty existing_members"""
        url = reverse('core:kelompok_create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'existingMemberIds = []')