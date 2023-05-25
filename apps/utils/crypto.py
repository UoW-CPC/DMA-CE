import hashlib
import os
import secrets
from base64 import b64encode

import pbkdf2
import pyaes


# CSPRNG: Cryptography Secure Pseudo-Random Number Generator
# CSPRNG guarantee that the random number coming from it is absolutely unpredictable.
def nonce_generation():
    return b64encode(os.urandom(32)).decode('utf-8')

# SHA-512 is based on "MerKle-Damgard construction".
# It is considered highly secure and collision resistance for most applications.
def H2_hash_function(temp):
    res = hashlib.sha512(temp.encode('utf-8')).hexdigest()
    return res

# As AES CTR Block Mode is used in DMA.TL,
# so passwordSalt and IV need to be initialized by EMGWAM before sharing them with MH and CE.
def passwordSaltAndiv_generation():
    passwordSalt_value = os.urandom(16)
    iv_value = secrets.randbits(256)
    return passwordSalt_value, iv_value

# Encryptor
class SymmetricEncryption(object):
    def __init__(self, passwordSalt_value, iv_value):
        self.passwordSalt = passwordSalt_value
        self.iv = iv_value

    def encryption(self, msg, password):
        key = pbkdf2.PBKDF2(password, self.passwordSalt).read(32)
        aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(self.iv))
        ciphertext = aes.encrypt(msg)
        return ciphertext

    def decryption(self, ciphertext, password):
        key = pbkdf2.PBKDF2(password, self.passwordSalt).read(32)
        aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(self.iv))
        message = aes.decrypt(ciphertext)
        return message


