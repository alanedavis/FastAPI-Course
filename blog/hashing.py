from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrypt(data: str):
        return pwd_context.hash(data)

    def verify(hashed_password, plain_password):
        return pwd_context.verify(plain_password, hashed_password)