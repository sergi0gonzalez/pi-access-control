from django.shortcuts import render


def main_page(request):
    tparams = {}
    return render(request, 'index.html', tparams)


def profile_page(request):
    tparams = {}
    return render(request, 'profile.html', tparams)
