from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db import getDB
from .user_routes import getUserInfo
from ..schemas import UserOut


adminRoutes = APIRouter(prefix="/api/admin", tags=["My Admin Routes"])

@adminRoutes.get("/check-admin")
async def checkAdmin(db:Session = Depends(getDB), userInfo:UserOut = Depends(getUserInfo)):
    if not userInfo.role == "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not Admin!")
    return userInfo
