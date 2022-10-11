from django.urls import path

from .views import signup, token

urlpatterns = [
    path('signup/', signup),
    path('token/', token),
]
