from django.urls import path
from api import views

urlpatterns = [
	path('check_nfc_credential/', views.check_nfc_credential),
    path('check_audio_credential/', views.check_audio_credential),
    path('check_qrcode_credential/', views.check_qrcode_credential),
    path('check_rfid_credential/', views.check_rfid_credential),
    path('token_request/', views.mobile_login),
    path('get_names/', views.mobile_get_names),
    path('get_email/', views.mobile_get_email),
    path('get_credential/', views.mobile_get_credential)
]
