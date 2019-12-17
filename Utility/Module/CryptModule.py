import hashlib, base64, sys
from cryptography.fernet import Fernet

"""
CryptModule
문자열을 Password를 통해 암호화하고 복호화하는 모듈
"""
# todo 패스워드를 지정 가능하게?

class CryptModule:
    CryptDelimiter = '\t'  # 임의 문자, str(대상 오브젝트)에서 나타나지 않는 문자열이어야 한다 todo 구분자 바꿀것
    __Password = 'CopyRight@: 2doo - github.com/doobee98'

    """
    method
    * encrypt, decrypt
    """
    @classmethod
    def encrypt(cls, s: str) -> bytes:
        m = hashlib.sha256()
        m.update(CryptModule.__Password.encode())
        key = base64.urlsafe_b64encode(m.digest())
        cipher_suite = Fernet(key)
        return cipher_suite.encrypt(s)

    @classmethod
    def decrypt(cls, b: bytes) -> str:
        m = hashlib.sha256()
        m.update(CryptModule.__Password.encode())
        key = base64.urlsafe_b64encode(m.digest())
        cipher_suite = Fernet(key)
        return cipher_suite.decrypt(b)

