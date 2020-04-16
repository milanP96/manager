from django.urls import path, include
from manager import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('organizations', views.OrganizationViewSet)
router.register('tasks', views.TaskViewSet)

app_name = 'manager'

urlpatterns = [
    path('', include(router.urls)),
]