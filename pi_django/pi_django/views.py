from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from pi_django.models import Credential, Permission, Log, Method, Profile
from django.utils import timezone
import re
import os
import io


def main_page(request):
    tparams = {}
    return render(request, 'index.html', tparams)


def login_page(request):
    tparams = {}

    if "login_email" in request.POST:
        tparams["error"] = False
        tparams["error_reason"] = None
        user = authenticate(username=request.POST["login_email"], password=request.POST["login_password"])
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            tparams["login_error"] = True
            tparams["login_error_reason"] = "Authentication Failed."
            return render(request, 'login.html', tparams)
    elif request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request, 'login.html', tparams)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def register_page(request):
    tparams = {}

    if "signup_email" in request.POST:
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
        elif len(request.POST['signup_password']) < 9:
            tparams["signup_error"] = True
            tparams["signup_error_reason"] = "Password too short."
            return render(request, 'register.html', tparams)
        elif request.POST['signup_confpassword'] != request.POST['signup_password']:
            tparams['signup_error'] = True
            tparams['signup_error_reason'] = 'Passwords don\'t match!'
            return render(request, 'register.html', tparams)
        else:
            user = User.objects.create_user(username=request.POST['signup_email'], email=request.POST['signup_email'],
                                            password=request.POST["signup_password"])
            user.last_name = request.POST['signup_full_name']
            user.save()
            if 'signup_civilid' in request.POST:
                profile = Profile.objects.get(user=user)
                profile.id_number = request.POST['signup_civilid']
                profile.photo.save('photo.png', io.BytesIO(bytes.fromhex(request.POST['signup_photo'])), save=False)
                profile.save()
            perm = Permission(user=user)
            perm.save()
            secret = os.urandom(20).hex()
            cred = Credential(status="valid", user=user, data=secret)
            cred.save()
            return redirect('/')
    else:
        return render(request, 'register.html', tparams)


def logout_page(request):
    logout(request)
    return redirect('/')


@login_required
def profile_page(request):
    tparams = {'perm': True, 'active_tab': False, 'error': False, 'last_access': ''}

    if Permission.objects.filter(user=request.user).exists():
        tparams['perm'] = Permission.objects.get(user=request.user).state
    if Log.objects.filter(user=request.user).exists():
        tparams['last_access'] = Log.objects.filter(user=request.user).all().order_by('time_stamp').reverse()[0]
    if request.method == 'POST':
        if 'btnChange' in request.POST:
            tparams['active_tab'] = True
            user_auth = authenticate(username=request.user.username, password=request.POST['password'])
            if user_auth is not None and request.POST['new_password'] == request.POST['new_confpassword']:
                request.user.set_password(request.POST['new_confpassword'])
                request.user.save()
            elif user_auth is None and request.POST['password'] != '':
                tparams['change_error'] = True
                tparams['change_error_reason'] = 'Wrong password!'
                return render(request, 'profile.html', tparams)
            elif request.POST['new_password'] != request.POST['new_confpassword']:
                tparams['change_error'] = True
                tparams['change_error_reason'] = 'Passwords don\'t match!'
                return render(request, 'profile.html', tparams)
            else:
                tparams['change_error'] = True
                tparams['change_error_reason'] = 'No password!'
                return render(request, 'profile.html', tparams)
        else:
            request.user.profile.photo = request.FILES['photo']
            request.user.profile.save()

    return render(request, 'profile.html', tparams)


def mobile_page(request):
    tparams = {}
    return render(request, 'mobile_app.html', tparams)


@login_required
@user_passes_test(lambda u: u.is_staff)
def students_perms(request):
    tparams = {}
    return render(request, 'students_perms.html', tparams)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def security_dashboard(request):
    tparams = {'revoke_tab': False, 'method_tab': False}
    permissions = Permission.objects.filter(state=False)
    tparams['permissions'] = permissions
    accesses = Permission.objects.filter(state=True)
    tparams['accesses'] = accesses
    logs = Log.objects.all().order_by('time_stamp').reverse()
    tparams['logs'] = logs
    tparams['methods'] = Method.objects.all()

    if request.method == 'POST':
        if 'grant' in request.POST:
            for email in dict(request.POST)['grant']:
                if User.objects.filter(username=email).exists():
                    user = User.objects.get(username=email)
                    user.is_staff = True
                    user.save()
                    perm = Permission.objects.get(user=user)
                    perm.state = True
                    perm.start_time = timezone.now()
                    perm.end_time = None
                    perm.save()
        if 'revoke' in request.POST:
            tparams['revoke_tab'] = True
            for email in dict(request.POST)['revoke']:
                if User.objects.filter(username=email).exists():
                    user = User.objects.get(username=email)
                    user.is_staff = False
                    user.save()
                    perm = Permission.objects.get(user=user)
                    perm.state = False
                    perm.end_time = timezone.now()
                    perm.save()
        if 'method' in request.POST:
            tparams['method_tab'] = True
            for name in dict(request.POST)['method']:
                method = Method.objects.get(name=name)
                if method.status:
                    method.status = False
                else:
                    method.status = True
                method.save()

    return render(request, 'sec_dashboard.html', tparams)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def last_access(request):
    tparams = {'last_entry': 0}

    logs = Log.objects.filter(log_type='entry').order_by('time_stamp').reverse()
    if logs:
        tparams['last_entry'] = logs[0]

    return render(request, 'last_access.html', tparams)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_user(request, user_email):
    tparams = {'user_search': User.objects.get(username=user_email)}

    if request.method == 'POST':
        user = User.objects.get(username=request.POST['manage_user'])
        if 'credential' in request.POST:
            secret = os.urandom(20).hex()
            print('Secret ---> ',secret)
            cred = Credential(status="valid", user=user, data=secret)
            cred.save()
        if user.profile.rfid == '' and request.POST['manage_rfid'] != '':
            user.profile.rfid = request.POST['manage_rfid']
            user.profile.save()
        elif user.profile.rfid != request.POST['manage_rfid'] and request.POST['manage_rfid'] != '':
            user.profile.rfid = request.POST['manage_rfid']
            user.profile.save()

    return render(request, 'manage_user.html', tparams)
