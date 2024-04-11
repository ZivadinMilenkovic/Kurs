from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    hashed_pass = pwd_context.hash(password)
    return hashed_pass


def verify(paln_pass, hashed_pass):
    return pwd_context.verify(paln_pass, hashed_pass)
