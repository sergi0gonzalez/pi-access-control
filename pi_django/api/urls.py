from django.urls import path
from api import views

urlpatterns = [
    path('test/', views.api_test),
    path('user/', views.user_test),
    path('credentials/', views.check_credentials),
    path('nfc_challenge/', views.nfc_challenge)
]
