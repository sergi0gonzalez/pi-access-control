from django.shortcuts import render


def main_page(request):
    tparams = {}
    return render(request, 'index.html', tparams)

def services_page(request):
    tparams = {}
    return render(request, 'services.html', tparams)

def profile_page(request):
    tparams = {}
    return render(request, 'profile.html', tparams)