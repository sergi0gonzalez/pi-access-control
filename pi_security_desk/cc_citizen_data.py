from PyKCS11 import PyKCS11Error
from wand.image import Image
import PyKCS11
import sys

class CC_NOT_PRESENT(Exception):
    pass

class DEVICE_REMOVED(Exception):
    pass

class Citizen_Data(object):
   
    def __init__(self, lib='/usr/lib64/opensc-pkcs11.so'):
        self.pkcs11 = PyKCS11.PyKCS11Lib()
        self.pkcs11.load(lib)
        # Filter attributes
        self.all_attr = [e for e in list(PyKCS11.CKA.keys()) if isinstance(e, int)]
        

    def open_session(self):
        try:
            session = self.pkcs11.openSession(0)
            obj = session.findObjects([(PyKCS11.CKA_APPLICATION, 'Citizen Data')])[0]
            attr = session.getAttributeValue(obj, self.all_attr)
            self.data = bytes(dict(zip(map(PyKCS11.CKA.get, self.all_attr), attr))['CKA_VALUE'])
        except PyKCS11Error as e:
            if str(e).split()[0] == 'CKR_SLOT_ID_INVALID':
                #print('No card reader!')
                sys.exit(0)
            elif str(e).split()[0] == 'CKR_TOKEN_NOT_PRESENT':
                #print('No card plugged!')
                raise CC_NOT_PRESENT
            elif str(e).split()[0] == 'CKR_DEVICE_REMOVED':
                raise DEVICE_REMOVED
        

    def get_data_bytes(self):
        return self.data


    def get_name_id(self):
        info = self.data[0:1372].decode()
        tmp = info.split('\x00')
        tmp = list(filter(('').__ne__, tmp))
        id_number = tmp[3].split()[0]
        name = tmp[10] + ' ' +tmp[9]
        return name, id_number


    def get_photo_hex(self):
        hex_data = self.data.hex()
        pos = hex_data.find('0000000c6a502020')
        return hex_data[pos:]


    def get_photo_bytes(self):
        return bytes.fromhex(self.get_photo_hex())


    def get_photo_png_bytes(self):
        with Image(blob=self.get_photo_bytes()) as img:
            png_photo = img.convert('png')
        return png_photo.make_blob()


    def save_photo_to_file(self, filename='photo', filetype='jp2'):
        if filetype == 'jp2':
            with open(filename+'.jp2', 'wb') as f:
                f.write(self.get_photo_bytes())
        elif filetype == 'png':
            with Image(blob=self.get_photo_bytes) as img:
                png_photo = img.convert('png')
            with open(filename+'.png', 'wb') as f:
                f.write(bytes.fromhex(png.photo.make_blob()))

