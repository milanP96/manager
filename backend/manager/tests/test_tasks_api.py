from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from base.models import Task, Organization
import datetime
from manager.serializers import OrganizationSerializer

TASK_URL = reverse('manager:task-list')


class PublicOrganizationApiTests(TestCase):
    """Tests public organization endpoints"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Tests that login is required"""
        res = self.client.get(TASK_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateOrganizationApiTests(TestCase):
    """Tests authorized tasks endpoints"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@test.te',
            'Ime Korisnika',
            'password123'
        )
        self.organization = Organization(name="Org")
        self.organization.save()
        self.organization.users.add(self.user)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_task_on_authorized_user_successful(self):
        time_limit = datetime.datetime.now() + datetime.timedelta(hours=10)
        payload = {'name': "Test", 'description': "Ovo je neki desc", 'priority': "normal", 'time_limit': time_limit,
                   'organization_uuid': self.organization.uuid, 'status': "wait"}
        res = self.client.post(TASK_URL, payload)
        tasks = Task.objects.all()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.user.uuid, tasks[0].users.all()[0].uuid)

    def test_create_task_on_requested_users_successful(self):
        time_limit = datetime.datetime.now() + datetime.timedelta(hours=10)
        user1 = get_user_model().objects.create_user(
            'test1@test.te',
            'user1',
            'password123'
        )

        user2 = get_user_model().objects.create_user(
            'test2@test.te',
            'user2',
            'password123'
        )

        users = [user1.uuid, user2.uuid]

        payload = {'name': "Test", 'description': "Ovo je neki desc", 'priority': "normal", 'time_limit': time_limit,
                   'organization_uuid': self.organization.uuid, 'status': "wait",
                   "users_uuid": users}
        res = self.client.post(TASK_URL, payload)
        tasks = Task.objects.all()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for u in tasks[0].users.all().order_by('name'):
            self.assertIn(u.uuid, users)
