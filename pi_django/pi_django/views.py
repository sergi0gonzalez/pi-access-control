from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from pi_django.models import Credential
import re


def main_page(request):
    logged_in = request.user.is_authenticated
    tparams = {'logged_in': logged_in}
    if logged_in:
        tparams["username"] = request.user.username

    return render(request, 'index.html', tparams)


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
        if request.POST['signup_email'] == '' or not re.match(r'[^@]+', request.POST['signup_email']):
            tparams["signup_error"] = True
            tparams["signup_error_reason"] = "Please insert an valid email."
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
            user = User.objects.create_user(username=signup_email, email=signup_email, password=signup_password)
            user.first_name = request.POST['signup_first_name']
            user.last_name = request.POST['signup_last_name']
            user.save()
            return redirect('/')
    else:
        return render(request, 'register.html', tparams)


def logout_page(request):
    logout(request)
    return redirect('/')


def profile_page(request):
    logged_in = request.user.is_authenticated
    tparams = {'logged_in': logged_in, 'nfc': False}

    if logged_in:
        tparams["username"] = request.user.username
        user = User.objects.get(username=request.user.username)
        tparams['email'] = user.email
        tparams['first_name'] = user.first_name
        tparams['last_name'] = user.last_name
        if Credential.objects.filter(user=user).exists():
            for cred in Credential.objects.filter(user=user):
                if cred.associated_name == 'NFC':
                    tparams['nfc'] = True

    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        if request.POST['nfc'] == 'On' and request.POST['nfc_password'] != '' and \
                not Credential.objects.filter(user=user, associated_name='NFC').exists():
            cred = Credential(associated_name='NFC', user=user)
            cred.save()

    return render(request, 'profile.html', tparams)


def security_dashboard(request):
    logged_in = request.user.is_authenticated
    tparams = {'logged_in': logged_in}

    if logged_in:
        tparams["username"] = request.user.username
    return render(request, 'sec_dashboard.html', tparams)
