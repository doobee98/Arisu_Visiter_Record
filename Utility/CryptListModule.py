import hashlib, base64, sys
from cryptography.fernet import Fernet
from typing import List, Any

UnitAll = sys.maxsize  # 임시 enum 배치

class CryptListModule():
    CryptUnit = UnitAll
    CryptDelimiter = '\t'  # 임의 문자, str(대상 오브젝트)에서 나타나지 않는 문자열이어야 한다 todo 구분자 바꿀것
    __Password = 'CopyRight@: 2doo - github.com/doobee98'

    @classmethod
    def encrypt(cls, l: List[Any]) -> List[bytes]:
        m = hashlib.sha256()
        m.update(CryptListModule.__Password.encode())
        key = base64.urlsafe_b64encode(m.digest())
        cipher_suite = Fernet(key)

        start = 0
        cur = start
        end = len(l)
        result = []

        while cur < end:
            if cur + CryptListModule.CryptUnit < end:
                tempend = cur + CryptListModule.CryptUnit
            else:
                tempend = end

            b = b''
            for i in range(cur, tempend):
                b += (str(l[i]) + CryptListModule.CryptDelimiter).encode()

            e = cipher_suite.encrypt(b)
            result.append(e)

            cur += CryptListModule.CryptUnit

        return result

    @classmethod
    def decrypt(cls, l: List[bytes], class_name: type) -> List[Any]:
        m = hashlib.sha256()
        m.update(CryptListModule.__Password.encode())
        key = base64.urlsafe_b64encode(m.digest())
        cipher_suite = Fernet(key)

        d = []

        for h in l:
            d += cipher_suite.decrypt(h)

        string = bytes(d).decode()

        object_str_list = string.split(CryptListModule.CryptDelimiter)[:-len(CryptListModule.CryptDelimiter)]
        # 마지막에도 추가된 delimiter 를 빼주기 위해
        object_list = [class_name(object_str) for object_str in object_str_list]

        return object_list
