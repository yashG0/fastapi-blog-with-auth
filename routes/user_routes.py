from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .auth_routers import getUser
from ..schemas import UserOut
from ..db import getDB


userRouters = APIRouter(prefix="/api/user", tags=["My User Routes"])


@userRouters.get("/userInfo", status_code=status.HTTP_200_OK, response_model=UserOut)
async def getUserInfo(db:Session = Depends(getDB), userInfo:UserOut = Depends(getUser)):
    if not userInfo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user is not valid!")
    return userInfo