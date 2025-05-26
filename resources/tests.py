from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from custom.models import User
from .models import resources

# Create your tests here.

class ResourceAPITestCase(APITestCase):
    def setUp(self):
        self.lecturer = User.objects.create_user(username='lecturer1', password='pass', role='lecture')
        self.client = APIClient()
        self.client.force_authenticate(user=self.lecturer)

    def test_create_resource(self):
        url = reverse('resource-list-create')
        data = {
            'resource_type': 'document',
            'description': 'Test resource',
            'is_active': True
        }
        response = self.client.post(url, data)
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])

    def test_list_resources(self):
        url = reverse('resource-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
