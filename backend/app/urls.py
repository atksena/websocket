from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/', include('jwt_authentication.urls')),
    path('api/', include('chat.urls')),
]
