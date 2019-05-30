#from resources import send_credential, portic_signal
import PyKCS11
import time
import sys
import os
from cryptography import x509
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
from cryptography import x509

class CCUnplugged(Exception):
	pass
class CitizenCard:
	class __CitizenCard:
		def __init__(self):
			self.lib = '/usr/local/lib/libpteidpkcs11.so'
			self.pkcs11 = PyKCS11.PyKCS11Lib()
			self.pkcs11.load(self.lib)

			slots = self.pkcs11.getSlotList()

			if len(slots) == 0:
				raise CCUnplugged()
			else:
				self.slot = slots[0]

		def sign_bytes(self, document_bytes):
			session = self.pkcs11.openSession(self.slot, PyKCS11.CKF_RW_SESSION)	
			private_key = session.findObjects([
				(PyKCS11.CKA_CLASS, PyKCS11.CKO_PRIVATE_KEY),
				(PyKCS11.CKA_LABEL, 'CITIZEN AUTHENTICATION KEY')
			])[0]
			mechanism = PyKCS11.Mechanism(PyKCS11.CKM_SHA1_RSA_PKCS, None)
			signature = bytes(session.sign(private_key, document_bytes, mechanism))
			
			session.closeSession()
			return signature
		
		def get_auth_certificate(self):
			all_attr = list(PyKCS11.CKA.keys())
			all_attr = [e for e in all_attr if isinstance(e, int)]
			session = self.pkcs11.openSession(self.slot)
			certbytes = None
			for obj in session.findObjects():
				# Get object attributes
				attr = session.getAttributeValue(obj, all_attr)
				# Create dictionary with attributes
				attr = dict(zip(map(PyKCS11.CKA.get, all_attr), attr))
				if attr['CKA_LABEL'].strip() == "CITIZEN AUTHENTICATION CERTIFICATE":
					certbytes = bytes(attr['CKA_VALUE'])
					break
					
			session.closeSession()
			return certbytes

		def get_username(self, auth_certificate):
			cert = x509.load_der_x509_certificate(auth_certificate, default_backend())
			return cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value

		def print_info(self):
			print(self.pkcs11.getTokenInfo(self.slot))
			all_attr = list(PyKCS11.CKA.keys())
			#Filter attributes
			all_attr = [e for e in all_attr if isinstance(e, int)]
			session = self.pkcs11.openSession(self.slot)
			for obj in session.findObjects():
				# Get object attributes
				attr = session.getAttributeValue(obj, all_attr)
				# Create dictionary with attributes
				attr = dict(zip(map(PyKCS11.CKA.get, all_attr), attr))
				print('Label: ', attr['CKA_LABEL'])
				if "CERTIFICATE" in attr['CKA_LABEL']:
					certbytes = bytes(attr['CKA_VALUE'])
					cert = x509.load_der_x509_certificate(certbytes, default_backend())
					print("\t" + "Subject: " + str(cert.subject.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value))
					print("\t" + "Issuer: " + str(cert.issuer.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value))
	
	# singleton stuff
	instance = None
	def __init__(self):
		if not CitizenCard.instance:
			CitizenCard.instance = CitizenCard.__CitizenCard()

try:
	while(True):
		try:
			cc = CitizenCard().instance
			cert = cc.get_auth_certificate()
			cert = x509.load_der_x509_certificate(cert, default_backend())
			pub_key = cert.public_key()
			challenge_bytes = os.urandom(16)
			signature = cc.sign_bytes(challenge_bytes) # TODO: janela fechada?
			
			try:
				pub_key.verify(signature, challenge_bytes, padding.PKCS1v15(), hashes.SHA1())
				print("[*] User authenticated...")
				sleep(10)
			except InvalidSignature:
				# show error in rasp
				print("[*] Signature wrong...")
				sleep(10)
			
			# IF VALID SEND TO SERVER
			
			# TODO: Escape loop procedures, signature wrong, already sent one message to server, etc
		except (PyKCS11.PyKCS11Error, CCUnplugged) as e:
			print("[*] CC Unplugged ... Continuing.")
			pass
		time.sleep(2)
except KeyboardInterrupt:
    sys.exit(0)
