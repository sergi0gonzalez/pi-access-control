from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.twofactor.totp import TOTP, InvalidToken
from cryptography.hazmat.primitives.hashes import SHA256
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import JsonResponse
from pi_django.models import Credential, UniversalUser, Permissions, Log
from tools.crypto import Asymmetric, Symmetric, HMAC
from django.utils import timezone
import base64
import json
import time
import os


RASP_RSAPUB_KEY = 'tools/rasp_rsa.pub'
RASP_ECCPUB_KEY = 'tools/rasp_ecc.pub'


__asym_obj = Asymmetric()
__sym_obj = Symmetric()
__hmac_obj = HMAC()
# TODO: load private keys, ask for password
__rsa_priv = __asym_obj.load_private_key('tools/server_rsa', 'qwerty')
__ecc_priv = __asym_obj.load_private_key('tools/server_ecc', 'qwerty')


def user_test(request):
    print(User.objects.all())
    return JsonResponse({'status': 'OK'})


def api_test(request):
    print(request.method)
    if request.method == 'POST':
        return JsonResponse({'status': 'POST'})
    if request.method == 'GET':
        return JsonResponse({'status': 'GET'})


def nfc_challenge(request):
    if request.method == 'GET':
        data = {'nonce': base64.b64encode(os.urandom(32)).decode()}
        print(data)
        msg = create_msg_to_send(data, RASP_RSAPUB_KEY)
        return JsonResponse(msg)
    else:
        msg = create_msg_to_send(create_status_msg(405, 'Only GET method is allowed!'), RASP_RSAPUB_KEY)
        return JsonResponse(msg)


def nfc_response(request):
    return JsonResponse({'status': 'OK'})


@csrf_exempt
def check_audio_credential(request):
    if request.method == 'POST':
        msg = json.loads(decrypt_msg(request.POST, RASP_ECCPUB_KEY))
        msg = json.loads(msg)
        email = msg['identity']
        user = None
        if User.objects.filter(username=email).exists():
            user = User.objects.get(username=email)
        elif UniversalUser.objects.filter(e_mail=email).exists():
            user = UniversalUser.objects.get(username=email)
        # TODO: Permission validation (and perm.end_time > timezone.now())
        perm = Permissions.objects.get(user=user)
        if perm.state == True and perm.start_time < timezone.now():
            if Credential.objects.filter(user=user, associated_name='Audio').exists():
                cred = Credential.objects.get(user=user, associated_name='Audio')
                key = base64.b64decode(cred.data.encode())
                totp = TOTP(key, 8, SHA256(), 30, backend=default_backend())
                try:
                    totp.verify(msg['password'].encode(), time.time())
                except InvalidToken:
                    return JsonResponse(create_msg_to_send(create_status_msg(400, 'Authentication Failed!'), RASP_RSAPUB_KEY))
                log = Log(credential=cred, log_type='access', time_stamp=timezone.now())
                log.save()
                return JsonResponse(create_msg_to_send(create_status_msg(200, 'Authentication Successful'), RASP_RSAPUB_KEY))
    else:
        return JsonResponse(create_msg_to_send(create_status_msg(405, 'Only GET method is allowed!'), RASP_RSAPUB_KEY))


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
