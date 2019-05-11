from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from pi_django.models import Credential, Permissions, Log
from django.utils import timezone
import base64
import re
import os


def main_page(request):
    logged_in = request.user.is_authenticated
    tparams = {'logged_in': logged_in}
    if logged_in:
        tparams['username'] = request.user.username
        tparams['is_admin'] = request.user.is_superuser

    return render(request, 'index.html', tparams)


def login_page(request):
    tparams = {}

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
        if request.POST['signup_email'] == '' or not re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                                                              request.POST['signup_email']):
            tparams["signup_error"] = True
            tparams["signup_error_reason"] = "Please insert a valid email."
            return render(request, 'register.html', tparams)
        elif User.objects.filter(username=request.POST['signup_email']).exists():
            tparams['signup_error'] = True
            tparams['signup_error_reason'] = 'E-mail already in use!'
            return render(request, 'register.html', tparams)
        elif request.POST['signup_password'] == '':
            tparams["signup_error"] = True
            tparams["signup_error_reason"] = "Please insert a password."
            return render(request, 'register.html', tparams)
        elif len(signup_password) < 9:
            tparams["signup_error"] = True
            tparams["signup_error_reason"] = "Password too short."
            return render(request, 'register.html', tparams)
        elif request.POST['signup_confpassword'] != request.POST['signup_password']:
            tparams['signup_error'] = True
            tparams['signup_error_reason'] = 'Passwords don\'t match!'
            return render(request, 'register.html', tparams)
        else:
            user = User.objects.create_user(username=signup_email, email=signup_email, password=signup_password)
            user.last_name = request.POST['signup_full_name']
            user.save()
            perm = Permissions(user=user)
            perm.save()
            return redirect('/')
    else:
        return render(request, 'register.html', tparams)


def logout_page(request):
    logout(request)
    return redirect('/')


@login_required
def profile_page(request):
    logged_in = request.user.is_authenticated
    tparams = {'logged_in': logged_in, 'nfc': False, 'audio': False, 'cc': False}

    if logged_in:
        tparams["username"] = request.user.username
        user = User.objects.get(username=request.user.username)
        tparams['email'] = user.email
        tparams['full_name'] = user.last_name
        if Credential.objects.filter(user=user).exists():
            for cred in Credential.objects.filter(user=user):
                if cred.associated_name == 'NFC':
                    tparams['nfc'] = True
                if cred.associated_name == 'Audio':
                    tparams['audio'] = True
                if cred.associated_name == 'CitizensCard':
                    tparams['cc'] = True

    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        if request.POST['nfc'] == 'On' and request.POST['nfc_password'] != '' and \
                not Credential.objects.filter(user=user, associated_name='NFC').exists():
            cred = Credential(associated_name='NFC', user=user)
            cred.save()
        elif request.POST['audio'] == 'On' and request.POST['audio_password'] != '' and \
                not Credential.objects.filter(user=user, associated_name='Audio').exists():
            cred = Credential(associated_name='Audio', user=user)
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(algorithm=SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
            key = kdf.derive(request.POST['audio_password'].encode())
            # print(key)
            cred.data = base64.b64encode(key).decode()
            cred.save()
        elif request.POST['cc'] == 'On' and request.POST['id_number'] != '' and \
                not Credential.objects.filter(user=user, associated_name='CitizensCard').exists():
            cred = Credential(associated_name='CitizensCard', user=user)
            cred.data = request.POST['id_number']
            cred.save()

    return render(request, 'profile.html', tparams)


def mobile_page(request):
    logged_in = request.user.is_authenticated
    tparams = {'logged_in': logged_in}

    if logged_in:
        tparams["username"] = request.user.username
    return render(request, 'mobile_app.html', tparams)


@login_required
def students_perms(request):
    logged_in = request.user.is_authenticated
    tparams = {'logged_in': logged_in}

    if logged_in:
        tparams["username"] = request.user.username
    return render(request, 'students_perms.html', tparams)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def security_dashboard(request):
    logged_in = request.user.is_authenticated
    tparams = {'logged_in': logged_in}

    if logged_in:
        tparams['username'] = request.user.username
        permissions = Permissions.objects.filter(state=False)
        tparams['permissions'] = permissions
        accesses = Permissions.objects.filter(state=True)
        tparams['accesses'] = accesses
        logs = Log.objects.all().order_by('time_stamp').reverse()
        tparams['logs'] = logs

        if request.method == 'POST':
            if 'perm' in request.POST:
                for email in dict(request.POST)['perm']:
                    if User.objects.filter(username=email).exists():
                        user = User.objects.get(username=email)
                        perm = Permissions.objects.get(user=user)
                        perm.state = True
                        perm.start_time = timezone.now()
                        perm.end_time = None
                        perm.save()
            if 'access' in request.POST:
                for email in dict(request.POST)['access']:
                    if User.objects.filter(username=email).exists():
                        user = User.objects.get(username=email)
                        perm = Permissions.objects.get(user=user)
                        perm.state = False
                        perm.end_time = timezone.now()
                        perm.save()

    return render(request, 'sec_dashboard.html', tparams)
