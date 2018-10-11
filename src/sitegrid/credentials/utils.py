from django.conf import settings
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import zlib
import base64
import uuid

import os

def rsa_encrypt(cur_item, pub_path=None):

    is_encrypted = False
    encrypted_value = None
    if pub_path is None:
        pub_path = settings.RSA_PUBKEY_APACHE_PATH
        if not os.path.isfile(pub_path) and settings.DEBUG:
            #Only use this from the command line
            pub_path = settings.RSA_PUBKEY_PATH
    public_key = None
    if os.path.isfile(pub_path):
        with open(pub_path, 'rb') as fh:
            public_key = fh.read()
            fh.close()
        #Import the Public Key and use for encryption using PKCS1_OAEP
        session_key = get_random_bytes(16)
        rsa_key = RSA.importKey(public_key)
        key_len = rsa_key.size_in_bytes()
        
        cipher_rsa = PKCS1_OAEP.new(rsa_key)

        # Encrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        
        enc_session_key = cipher_rsa.encrypt(session_key)
        
        # convert the data to a bytestring
        cur_item = cur_item.encode('utf-8')
        
        ciphertext, tag = cipher_aes.encrypt_and_digest(cur_item)
        
        encrypted_list = [base64.encodestring(enc_session_key), base64.encodestring(cipher_aes.nonce), base64.encodestring(tag), base64.encodestring(ciphertext)]
        
        return encrypted_list
        
    return is_encrypted



def rsa_decrypt(cur_item, priv_path = None):

    decrypted_value = uuid.uuid4()
    if priv_path is None:
        priv_path = settings.RSA_PRIVKEY_APACHE_PATH
        if not os.path.isfile(priv_path) and settings.DEBUG:
            #Only use this from the command line
            priv_path = settings.RSA_PRIVKEY_PATH
    private_key = None
    if os.path.isfile(priv_path):
        with open(priv_path, 'rb') as fh:
            private_key = fh.read()
            fh.close()
        #Import the Private Key and use for decryption using PKCS1_OAEP
        rsa_key = RSA.importKey(private_key)
        key_len = rsa_key.size_in_bytes()
        
        cipher_rsa = PKCS1_OAEP.new(rsa_key)
        
        #Base 64 decode the data
        #encrypted_item = base64.b64decode(cur_item)

        #enc_session_key, nonce, tag, ciphertext = [ file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]
        # Translated to regular list, as we are storing this stuff in the DB.
        enc_session_key = base64.decodestring(cur_item[0])
        nonce = base64.decodestring(cur_item[1])
        tag = base64.decodestring(cur_item[2])
        ciphertext = base64.decodestring(cur_item[3])
        
        try:
            session_key = cipher_rsa.decrypt(enc_session_key)
            # Decrypt the data with the AES session key
            cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
            data = cipher_aes.decrypt_and_verify(ciphertext, tag)
            decrypted_value = data.decode("utf-8")
            #print(decrypted_value)

            return decrypted_value
        except Exception as e:
            #print("Error decrypting data %s" % (e, ))
            pass
            
    return False
