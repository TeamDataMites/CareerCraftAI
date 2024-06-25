from passlib.context import CryptContext


class Hash:
    def __init__(self, password):
        self.password = password
        self.ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def bcrypt(self):
        return self.ctx.hash(self.password)

    def verify(self, hashed_password):
        return self.ctx.verify(self.password, hashed_password)
