from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from base.models import Organization
from manager.serializers import OrganizationSerializer

ORGANIZATION_URL = reverse('manager:organization-list')

class PublicOrganizationApiTests(TestCase):
    """Tests public organization endpoints"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Tests that login is required"""
        res = self.client.get(ORGANIZATION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateOrganizationApiTests(TestCase):
    """Tests authorized organization endpoints"""
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@test.te',
            'Ime Korisnika',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_fetch_organizations(self):
        """Test fetching organizations"""
        org = Organization(name='tester')
        org.save()
        org.users.set([self.user])

        org1 = Organization(name='tester1')
        org1.save()
        org1.users.set([self.user])

        res = self.client.get(ORGANIZATION_URL)
        organizations = Organization.objects.all().order_by('name')
        serializer = OrganizationSerializer(organizations, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(res.data)['results'], serializer.data)

    def test_success_create_organization(self):
        """Test create a new organization"""
        payload = {'name': 'Tester Tester'}
        self.client.post(ORGANIZATION_URL, payload)

        exists = Organization.objects.filter(name=payload['name']).exists()
        self.assertTrue(exists)

    def test_success_create_organization_and_add_user(self):
        """Test create a new organization and adding current user to this organization"""
        payload = {'name': self.user.name}
        self.client.post(ORGANIZATION_URL, payload)
        org = Organization.objects.get(name=payload['name'])
        users = org.users.all()
        exists = Organization.objects.filter(name=payload['name']).exists()
        self.assertEqual(users[0].name, payload['name'])
        self.assertTrue(exists)

    def test_fail_create_organization(self):
        """Test fail to create organization with wrong payload"""
        payload = {'names': 'Tester Tester'}
        res = self.client.post(ORGANIZATION_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)