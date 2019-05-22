import PyKCS11
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID

import pkcs11
import os

#pkcs11 sun


from base64 import b64decode

# version 1.2

def sign_data(data: bytes) -> bytes:
    lib = '/usr/local/lib/libpteidpkcs11.dylib'
    pkcs11 = PyKCS11.PyKCS11Lib()
    pkcs11.load(lib)
    
    

    slot = pkcs11.getSlotList(tokenPresent=True)[0]

    session = pkcs11.openSession(slot)


    private_key = session.findObjects([(PyKCS11.CKA_CLASS, PyKCS11.CKO_PRIVATE_KEY),(PyKCS11.CKA_LABEL, 'CITIZEN AUTHENTICATION KEY')])[0]
    mechanism = PyKCS11.Mechanism(PyKCS11.CKM_SHA1_RSA_PKCS, None)
    signature = bytes(session.sign(private_key, data, mechanism))



    session.closeSession()
    return signature


def get_auth_certificate() -> bytes:
    lib = '/usr/local/lib/libpteidpkcs11.dylib'
    pkcs11 = PyKCS11.PyKCS11Lib()
    pkcs11.load(lib)



    slot = pkcs11.getSlotList(tokenPresent=True)[0]
    
    session = pkcs11.openSession(slot)

    info = session.findObjects()

    all_attr = [e for e in list(PyKCS11.CKA.keys()) if isinstance(e, int)]
    user_cert_value = None
    for obj in info:
        attr= session.getAttributeValue(obj, all_attr)
        attr = dict(zip(map(PyKCS11.CKA.get, all_attr), attr))
        if attr['CKA_LABEL'].strip() == "CITIZEN AUTHENTICATION CERTIFICATE":
            user_cert_value = bytes(attr['CKA_VALUE'])
            break
    return user_cert_value


'''
def get_pic():
    lib = pkcs11.lib(os.environ['PKCS11_MODULE'])

    
    print(list(lib.get_tokens()))
    token = lib.get_token(token_label='Auth PIN (CARTAO DE CIDADAO)')


    with token.open(rw=True) as session:
        print("----")
        for obj in session.get_objects({pkcs11.Attribute.LABEL: 'Citizen Data'}):
            print(obj)

    return None
'''


def get_cc_number():

    lib = '/usr/local/lib/libpteidpkcs11.dylib'
    pkcs11 = PyKCS11.PyKCS11Lib()
    pkcs11.load(lib)


    slot = pkcs11.getSlotList(tokenPresent=True)[0]
    
    session = pkcs11.openSession(slot)

    info = session.findObjects()

    infos1 = ''.join(chr(c) for c in [c.to_dict()['CKA_SUBJECT'] for c in info][0])

    bi = infos1.split("BI")[1][:8]
    return bi


def get_user_name(certificate: bytes = None) -> str:
    if certificate == None:
        certificate = x509.load_der_x509_certificate(get_auth_certificate(), default_backend())
    else:
        certificate = x509.load_der_x509_certificate(certificate, default_backend())
    return certificate.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value


#print(sign_data(b'48656c6c6f20776f726c640d0a').hex())

print("---------")

print(get_cc_number())

print("---------")

print(get_user_name())

print("---------")


#print(get_pic())




