from crypto import Asymmetric
import getpass
import os

__asym_obj = Asymmetric()

def rsa_keys(name):
    if not os.path.isfile(name+'_rsa'):
        password = getpass.getpass(prompt='Insert password to encrypt the RSA private key: ')
        conf_password = getpass.getpass(prompt='Confirm the password: ')
        while password != conf_password:
            print('Passwords don\'t match!')
            password = getpass.getpass(prompt='Insert password to encrypt the RSA private key: ')
            conf_password = getpass.getpass(prompt='Confirm the password: ')
        __asym_obj.create_rsa_keys(conf_password, name)


def ecc_keys(name):
    if not os.path.isfile(name+'_ecc'):
        password = getpass.getpass(prompt='Insert password to encrypt the ECC private key: ')
        conf_password = getpass.getpass(prompt='Confirm the password: ')
        while password != conf_password:
            print('Passwords don\'t match!')
            password = getpass.getpass(prompt='Insert password to encrypt the ECC private key: ')
            conf_password = getpass.getpass(prompt='Confirm the password: ')
        __asym_obj.create_ecc_keys(conf_password, name)


def generate_keys():
    name = input('Insert a name for the keys: ')
    rsa_keys(name)
    ecc_keys(name)


generate_keys()
