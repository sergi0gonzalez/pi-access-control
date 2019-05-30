#from resources import send_credential, portic_signal
import PyKCS11
import time
import sys
import os
import cryptography.hazmat.primitives.hashes
from resources import send_cc_data, portic_signal

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
			cert_bytes = cc.get_auth_certificate()
			cert = cryptography.x509.load_der_x509_certificate(cert_bytes)
			challenge_bytes = os.urandom(16)
			signature = cc.sign_bytes(challenge_bytes) # TODO: janela fechada?
			
			public_key = cert.public_key()
			public_key.verify(
				signature,
				challenge_bytes,
				padding.PSS(
					mgf=padding.MGF1(hashes.SHA1()),
					salt_length=padding.PSS.MAX_LENGTH
				),
				hashes.SHA1()
			)
			
			send_cc_data(cert_bytes)
			
		except (PyKCS11.PyKCS11Error, CCUnplugged) as e:
			print("[*] CC Unplugged ... Continuing.") #replace by portic signal
			pass
		except cryptography.exceptions.InvalidSignature:
			print("[*] Signature invalid... Continuing.") #replace by portic signal
			pass
		time.sleep(2)
except KeyboardInterrupt:
    sys.exit(0)
