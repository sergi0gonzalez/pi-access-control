from django.shortcuts import render
from django.http import JsonResponse

def main_page(request):
    tparams = {}
    return render(request, 'index.html', tparams)


def profile_page(request):
    tparams = {}
    return render(request, 'profile.html', tparams)

def api_test(request):
    return JsonResponse({"status":"OK"})