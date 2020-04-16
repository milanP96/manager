from django.urls import include, path
from django.contrib import admin

# Setup automatic URL routing
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('api/manager/', include('manager.urls'))
]