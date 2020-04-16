from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, mixins
from base.models import Organization, Task
from base.view_set_custom_mixins import CreateModelMixin

from .serializers import OrganizationSerializer, TaskSerializer


class OrganizationViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = OrganizationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Organization.objects.all()

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