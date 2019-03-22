from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout

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

    if "login_email" in request.POST:
        login_email = request.POST["login_email"]
        login_password = request.POST["login_password"]
        tparams["error"] = False
        tparams["error_reason"] = None

        user = authenticate(username=login_email, password=login_password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            tparams["login_error"] = True
            tparams["login_error_reason"] = "Authentication Failed."
            return render(request, 'login.html', tparams)
    else:
        return render(request, 'login.html', tparams)


def register_page(request):
    tparams = {}

    if "signup_email" in request.POST:
        signup_email = request.POST["signup_email"]
        signup_password = request.POST["signup_password"]
        tparams["error"] = False
        tparams["error_reason"] = None
        # TODO: additional validations
        if request.POST['signup_email'] == '':
            tparams["signup_error"] = True
            tparams["signup_error_reason"] = "Please insert an email."
            return render(request, 'register.html', tparams)
        elif User.objects.filter(username=request.POST['signup_email']).exists():
            tparams['signup_error'] = True
            tparams['signup_error_reason'] = 'E-mail already in use!'
            return render(request, 'register.html', tparams)
        elif request.POST['signup_password'] == '':
            tparams["signup_error"] = True
            tparams["signup_error_reason"] = "Please insert a password."
            return render(request, 'register.html', tparams)
        elif len(signup_password) < 5:
            tparams["signup_error"] = True
            tparams["signup_error_reason"] = "Password too short."
            return render(request, 'register.html', tparams)
        elif request.POST['signup_confpassword'] != request.POST['signup_password']:
            tparams['signup_error'] = True
            tparams['signup_error_reason'] = 'Passwords don\'t match!'
            return render(request, 'register.html', tparams)
        else:
            user = User.objects.create_user(signup_email, password=signup_password)
            return redirect('/')

    else:
        return render(request, 'register.html', tparams)


def logout_page(request):
    logout(request)
    return redirect('/')


def api_test(request):
    return JsonResponse({"status":"OK"})
