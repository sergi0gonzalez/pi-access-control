from django.shortcuts import render
from django.http import JsonResponse

def main_page(request):
    logged_in = request.user.is_authenticated
    tparams = {'logged_in': logged_in}
    if logged_in:
        tparams["username"] = request.user.username

    return render(request, 'index.html', tparams)


def profile_page(request):
    logged_in = request.user.is_authenticated
    tparams = {'logged_in': logged_in}

    if logged_in:
        tparams["username"] = request.user.username

    return render(request, 'profile.html', tparams)

def login_page(request):
    tparams={}
    return render(request, 'login.html', tparams)

def api_test(request):
    return JsonResponse({"status":"OK"})