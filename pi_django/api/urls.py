from django.urls import path
from api import views

urlpatterns = [
    path('check_credential/', views.check_credential),
    path('token_request/', views.mobile_login),
    path('get_names/', views.mobile_get_names),
    path('get_email/', views.mobile_get_email),
    path('get_credential/', views.mobile_get_credential)
]
