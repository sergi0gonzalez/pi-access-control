# from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User


def api_test(request):
    return JsonResponse({"status": "OK"})


def user_test(request):
    print(User.objects.all())
    return JsonResponse({'status': 'OK'})


def check_credentials(request):
    if request.method == 'POST':
        return JsonResponse({'status': 'OK'})
    elif request.method == 'GET':
        return JsonResponse({'status': 'Not OK'})


def nfc_challenge(request):
    return JsonResponse({'status': 'OK'})


def nfc_response(request):
    return JsonResponse({'status': 'OK'})
