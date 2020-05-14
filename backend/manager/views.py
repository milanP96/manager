from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from django.db.models import Count
from user.serializers import UserSerializer

from base.models import Organization, Task
from base.view_set_custom_mixins import CreateModelMixin

from .serializers import OrganizationSerializer, TaskSerializer, OrganizationsSerializer, FriendRequestSerializer
import json


class UserViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = FriendRequestSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Organization.objects.all()

    @action(detail=False, methods=['POST'], url_path='friend_request')
    def friend_request(self, request, pk=None):
        return Response({'results': "json.loads(my_serializer.serialize(personal))"}, status=status.HTTP_200_OK)


class OrganizationViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = OrganizationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Organization.objects.all()

    @action(detail=False, methods=['GET'], url_path='my')
    def my(self, request, pk=None):
        organizations = []
        print(self.request.user)
        personal = Organization.objects.filter(name=self.request.user.name).annotate(
            notes_count=Count('note'), participants=Count('users')
        )
        organizations.append(personal)
        print(personal)
        my_serializer = OrganizationsSerializer()
        return Response({'results': json.loads(my_serializer.serialize(personal))}, status=status.HTTP_200_OK)

    def get_queryset(self):
        return self.queryset.filter(users__in=[self.request.user])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, CreateModelMixin):
    serializer_class = TaskSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Task.objects.all()

    def get_queryset(self):
        return self.queryset.filter(users__in=[self.request.user])

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)