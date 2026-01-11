from health_backend.application.common.password_hasher import PasswordHasher


class MockPasswordHasher(PasswordHasher):
    def hash(self, password: str) -> str:
        return password
