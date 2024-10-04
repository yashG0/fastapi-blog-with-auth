from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db import getDB
from .user_routes import getUserInfo
from ..schemas import UserOut


adminRoutes = APIRouter(prefix="/api/admin", tags=["My Admin Routes"])


def adminRoleCheck(userInfo: UserOut = Depends(getUserInfo)):
    if userInfo.role is not 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not an admin")
    return userInfo
    
@adminRoutes.get("/check-admin")
async def checkAdmin(userInfo: UserOut = Depends(adminRoleCheck)):
    return userInfo
