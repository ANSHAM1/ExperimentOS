from pwdlib import PasswordHash


class PasswordService:

    _hasher = PasswordHash.recommended()

    @classmethod
    def hash(cls, password: str) -> str:
        return cls._hasher.hash(password)

    @classmethod
    def verify(cls, password: str, password_hash: str) -> bool:
        return cls._hasher.verify(password, password_hash)