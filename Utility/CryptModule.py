import hashlib, base64, sys
from cryptography.fernet import Fernet
from typing import List, Any

UnitAll = sys.maxsize  # 임시 enum 배치

class CryptModule():
    CryptUnit = UnitAll
    CryptDelimiter = '\t'  # 임의 문자, str(대상 오브젝트)에서 나타나지 않는 문자열이어야 한다 todo 구분자 바꿀것
    __Password = 'CopyRight@: 2doo - github.com/doobee98'

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

