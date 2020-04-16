from abc import ABC

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from base.models import Organization, Wallet, Task


class OrganizationSerializer(serializers.Serializer):
    """Serializer for the organization object"""
    name = serializers.CharField()
    wallet = serializers.BooleanField()

    def save(self, user):
        name = self.validated_data['name']
        wallet = None
        if self.validated_data['wallet']:
            wallet = Wallet(amount=0)
            wallet.save()
        org = Organization(name=name, wallet=wallet)
        org.save()
        org.users.add(user)


class TaskSerializer(serializers.Serializer):
    """Task for the organization object"""
    name = serializers.CharField()
    description = serializers.CharField()
    priority = serializers.CharField()
    time_limit = serializers.DateTimeField()
    organization_uuid = serializers.UUIDField()
    status = serializers.CharField()
    users_uuid = serializers.ListField(child=serializers.UUIDField(), required=False)

    def save(self, user):
        payload = {k: v for (k, v) in self.validated_data.items() if k != 'organization_uuid' and k != 'users_uuid'}
        organization = Organization.objects.get(uuid=self.validated_data['organization_uuid'])
        task = Task(organization=organization, **payload)
        task.save()
        users = [get_user_model().objects.get(uuid=uuid) for uuid in self.validated_data['users_uuid']] \
            if 'users_uuid' in self.validated_data else [user]
        task.users.add(*users)
        return {'users': [{'uuid': u.uuid, 'name': u.name} for u in users], **self.validated_data}
