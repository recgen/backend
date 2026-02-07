from dataclasses import dataclass

import argon2
from argon2.exceptions import VerifyMismatchError

from health_backend.application.common.password_hasher import PasswordHasher


class ArgonPasswordHasher(PasswordHasher):
    argon_hasher = argon2.PasswordHasher()

    def hash(self, password: str) -> str:
        return self.argon_hasher.hash(password)

    def verify(self, password: str, hashed_password: str) -> bool:
        try:
            return self.argon_hasher.verify(hash=hashed_password, password=password)
        except VerifyMismatchError:
            return False
