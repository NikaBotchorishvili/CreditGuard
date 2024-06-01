from django.urls import path
from .views import router
from django.urls import include



urlpatterns = [
    path("", include(router.urls))
]
