from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash():
    def encryptPassword(password:str):
        return pwd_context.hash(password)
    
    def decryptPassword(password:str, hashedPassword:str):
        return pwd_context.verify(password, hashedPassword)