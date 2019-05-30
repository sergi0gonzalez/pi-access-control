from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.twofactor.totp import TOTP, InvalidToken
from cryptography.hazmat.primitives.hashes import SHA256
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from pi_django.models import Credential, Permission, Log
from rest_framework.decorators import api_view
from tools.crypto import Asymmetric, Symmetric, HMAC
from django.utils import timezone
import json
import time
import logging

RASP_RSAPUB_KEY = 'tools/rasp_rsa.pub'
RASP_ECCPUB_KEY = 'tools/rasp_ecc.pub'


__asym_obj = Asymmetric()
__sym_obj = Symmetric()
__hmac_obj = HMAC()
# TODO: load private keys, ask for password
__rsa_priv = __asym_obj.load_private_key('tools/server_rsa', 'qwerty')
__ecc_priv = __asym_obj.load_private_key('tools/server_ecc', 'qwerty')
logger = logging.getLogger(__name__)


@csrf_exempt
def check_credential(request):
    if request.method == 'POST':
        msg = json.loads(decrypt_msg(request.POST, RASP_ECCPUB_KEY))
        msg = json.loads(msg)
        email = msg['identity']
        user = None
        if User.objects.filter(username=email).exists():
            user = User.objects.get(username=email)
        # TODO: Permission validation (and perm.end_time > timezone.now())
        perm = Permission.objects.get(user=user)
        if perm.state and perm.start_time < timezone.now():
            credential = Credential.objects.get(user=user)
            if credential is not None and credential.status == 'valid':
                key = bytes.fromhex(credential.data)
                totp = TOTP(key, 8, SHA256(), 30, backend=default_backend())
                try:
                    totp.verify(msg['password'].encode(), time.time())
                except InvalidToken:
                    return JsonResponse(create_msg_to_send(create_status_msg(400, 'Authentication Failed!'), RASP_RSAPUB_KEY))
                logs = Log.objects.get(user=user).all().order_by('time_stamp').reverse()
                if logs[0].log_type == 'leave':
                    log = Log(user=user, log_type='entry', time_stamp=timezone.now())
                    log.save()
                else:
                    log = Log(user=user, log_type='leave', time_stamp=timezone.now())
                    log.save()
                return JsonResponse(create_msg_to_send(create_status_msg(200, 'Authentication Successful'), RASP_RSAPUB_KEY))
        else:
            return JsonResponse(create_msg_to_send(create_status_msg(400, 'Authentication Failed!'), RASP_RSAPUB_KEY))

    else:
        return JsonResponse(create_msg_to_send(create_status_msg(405, 'Only POST method is allowed!'), RASP_RSAPUB_KEY))
#@csrf_excempt
#def check_cc_cert(request):
#	if request.method == 'POST':
#		msg = json.loads(decrypt_msg(request.POST, RASP_ECCPUB_KEY))
#		msg = json.loads(msg)
#		certbytes = bytes.fromhex(msg['cert'])
#		certificate = cryptography.x509.load_der_x509_certificate(cert_bytes)
		# to do ...
#	else:
#		return JsonResponse(create_msg_to_send(create_status_msg(405, 'Only POST method is allowed!'), RASP_RSAPUB_KEY))


@csrf_exempt
def mobile_login(request):
    if "username" not in request.POST or "password" not in request.POST:
        print("DENIED: us/ps not in form")
        return JsonResponse({"status": "denied", "reason": "Username or password missing."})

    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(username=username, password=password)
    if not user:
        print("DENIED: invalid credentials")
        return JsonResponse({"status": "denied", "reason": "Invalid Credentials."})
    token, _ = Token.objects.get_or_create(user=user)
    print("granted login")
    return JsonResponse({"status": "granted", "token": token.key})


@csrf_exempt
@api_view(["GET"])
def mobile_get_names(request):
    return JsonResponse({"first_name": request.user.first_name, "last_name": request.user.last_name})


@csrf_exempt
@api_view(["GET"])
def mobile_get_email(request):
    return JsonResponse({"email": request.user.username})


@csrf_exempt
@api_view(["GET"])
def mobile_get_credential(request):
    cred = Credential.objects.get(user=request.user)
    return JsonResponse({"credential": cred.data})


def create_msg_to_send(data, public_key):
    msg = {}
    # Encrypt data with symmetric key
    sym_key = __sym_obj.create_key()
    enc_data = __sym_obj.encrypt_data(sym_key[1], json.dumps(data))
    msg['msg'] = enc_data
    # Encrypt symmetric key with public key
    msg['key'] = __asym_obj.encrypt_msg(__asym_obj.load_public_key(public_key), json.dumps(sym_key[0]))
    # Create enc_data hash
    msg_hash = __hmac_obj.message_digest(enc_data)
    msg['mac'] = msg_hash[1]
    # Encrypt hash key with public key
    msg['mac_key'] = __asym_obj.encrypt_msg(__asym_obj.load_public_key(public_key), msg_hash[0])
    # Create signature for the enc_data
    msg['signature'] = __asym_obj.sign_msg(__ecc_priv, enc_data)
    return msg


def create_status_msg(code, msg):
    data = {}
    if code != 200:
        data['error'] = code
    else:
        data['ok'] = code
    data['message'] = msg
    return json.dumps(data)


def decrypt_msg(data, sign_key):
    if not verify_signature_msg(data['signature'], data['msg'], sign_key):
        return create_status_msg(500, 'Client Warning: Something is wrong with the signature!')
    if check_hmac(data['mac_key'], data['msg'], data['mac']):
        dec_key = __asym_obj.decrypt_msg(__rsa_priv, data['key']).decode('utf-8')
        dec_key = json.loads(dec_key)
        sym_key = __sym_obj.create_key(dec_key[0], dec_key[1], dec_key[2])[1]
        return __sym_obj.decrypt_data(sym_key, data['msg'])
    else:
        return create_status_msg(500, 'Client Warning: Message altered!')


def check_hmac(key, data, digest):
    hmac_key = __asym_obj.decrypt_msg(__rsa_priv, key)
    return __hmac_obj.verify_digest(hmac_key, data, digest)


def verify_signature_msg(signature, msg, public_key):
    sign_key = __asym_obj.load_public_key(public_key)
    return __asym_obj.verify_sign(sign_key, msg.encode(), signature)
