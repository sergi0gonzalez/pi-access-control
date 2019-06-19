from django.urls import path
from api import views

urlpatterns = [
	path('check_nfc_credential/', views.check_nfc_credential),
    path('check_audio_credential/', views.check_audio_credential),
    path('check_qrcode_credential/', views.check_qrcode_credential),
    path('check_rfid_credential/', views.check_rfid_credential),
    path('check_cc_number/', views.check_cc_number),
    path('token_request/', views.mobile_login),
    path('get_name/', views.mobile_get_name),
    path('get_email/', views.mobile_get_email),
    path('get_credential/', views.mobile_get_credential),
    path('get_latest_logs/', views.mobile_get_latest_logs)
]
