from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.twofactor.totp import TOTP
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from tools.crypto import Asymmetric, Symmetric, HMAC
import requests
import json
import time
import sys


SERVER_RSAPUB_KEY = 'server_rsa.pub'
SERVER_SIGNPUB_KEY = 'server_ecc.pub'

__asym_obj = Asymmetric()
__sym_obj = Symmetric()
__hmac_obj = HMAC()
# TODO: load private keys, ask for password
__rsa_priv = __asym_obj.load_private_key('rasp_rsa', 'qwerty')
__ecc_priv = __asym_obj.load_private_key('rasp_ecc', 'qwerty')


def get_nfc_challenge():
    response = requests.get('http://10.42.0.1:8080/api/nfc_challenge').json()
    print(response)
    msg = json.loads(decrypt_msg(response, SERVER_SIGNPUB_KEY))
    if 'error' in msg:
        print('Error(...)', msg)
        return
    print(msg)

def send_audio_credential(identity, otp):
    #key = b'\xc9~I)\xef@\x1f\x16W\xd7\xe9)V\x01\x84d\x97\x9a\xe8K\xc2(\xb2\xac?c\xc5\xf1\x9c\xb0@\x12'
    #totp = TOTP(key, 8, SHA256(), 30, backend=default_backend())
    #totp_value = totp.generate(time.time())
    data = {'identity': identity, 'password': otp}
    msg = create_msg_to_send(json.dumps(data), SERVER_RSAPUB_KEY)
    response = requests.post('http://10.42.0.1:8080/api/audio_credential/', data=msg).json()
    #print(response)
    msg = json.loads(decrypt_msg(response, SERVER_SIGNPUB_KEY))
    if 'error' in msg:
        print('Error(...)', msg)
        return
    print(msg)



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

#get_nfc_challenge()
#send_audio_credential()

