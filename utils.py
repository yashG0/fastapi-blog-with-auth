import os
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

JWT_KEY = str(os.getenv("JWT_KEY"))
ALGORITHM = "HS256"

pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def encodePasswd(passwd:str) -> str:
    return pwdContext.hash(passwd)

def decodePasswd(passwd:str, hashPasswd:str) -> bool:
    return pwdContext.verify(passwd, hashPasswd)


def generateJwtToken(username:str, expiration_minutes:int = 15) -> str:
    expiration = datetime.now() + timedelta(minutes=expiration_minutes)

    payload = {
        "sub": username,
        "exp":expiration
    }
    token = jwt.encode(payload, JWT_KEY, algorithm=ALGORITHM) # type: ignore
    return token

def decodeJwtToken(token:str) -> dict[str,str]:
    try:
        payload = jwt.decode(token, key=JWT_KEY, algorithms=[ALGORITHM]) #type:ignore
        return payload

    except jwt.ExpiredSignatureError:
        return {"error":"Token has been expired!"}

    except jwt.PyJWTError as err:
        return {"error":f"Invalid token {err}"}
