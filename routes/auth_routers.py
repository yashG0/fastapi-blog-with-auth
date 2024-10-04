from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from ..utils import decodeJwtToken, decodePasswd, encodePasswd, generateJwtToken
from ..db import getDB
from ..schemas import UserIn, UserOut
from ..models import User



authRouters = APIRouter(prefix="/api/auth", tags=["My Auth Routes"])

oAuthBear = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

@authRouters.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(userModel:UserIn, db:Session = Depends(getDB)):
    
    isUser = db.query(User).filter(User.username == userModel.username).first()
    if isUser:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User Already Exists! Please sign-in")
    
    hashPassword = encodePasswd(userModel.password)
    
    try:
        newUser = User(
            username = userModel.username,
            email = userModel.email,
            password = hashPassword,
        )
        db.add(newUser)
        db.commit()
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User failed to sign up: {e}")

        
@authRouters.post("/login", status_code=status.HTTP_200_OK)
async def login(userForm:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(getDB)):
    isUser = db.query(User).filter(User.username == userForm.username).first()
    
    if isUser is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User does'nt exists! please sign-up")
    
    if not decodePasswd(userForm.password, str(isUser.password)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User or password is invalid! please login again")
    
    try:
        token = generateJwtToken(username=userForm.username)
        return {"access_token":token, "token_type":"Bearer"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User failed to login {e}")


def getUser(token:str = Depends(oAuthBear), db:Session = Depends(getDB)) -> UserOut:
    payload = decodeJwtToken(token)
    
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=payload["error"]) 
        
    username = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserOut(id=user.id, username=str(user.username), role=user.role) # type:ignore
   
