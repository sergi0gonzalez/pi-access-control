from django.urls import path
from api import views

urlpatterns = [
    path('user/', views.user_test),
    path('audio_credential/', views.check_audio_credential),
    path('test/', views.api_test),
    path('nfc_challenge/', views.nfc_challenge),
    path('token_request/', views.mobile_login),
    path('get_names/', views.mobile_get_names),
    path('get_email/', views.mobile_get_email)
]
