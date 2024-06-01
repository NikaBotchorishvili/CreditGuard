from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework_simplejwt.views import TokenObtainPairView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  
    path('', SpectacularSwaggerView.as_view(url_name='schema')),
    path("/", include("cards.urls")),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
]
