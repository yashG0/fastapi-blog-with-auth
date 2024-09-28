from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..models import Post
from .auth_routers import getUser
from ..schemas import PostBase, UserOut
from ..db import getDB


postRouters = APIRouter(prefix="/api/post", tags=["My Post Routes"])

@postRouters.get("/all", status_code=status.HTTP_200_OK)
async def allPosts(db:Session = Depends(getDB), userInfo:UserOut = Depends(getUser)):
    if not userInfo:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authorized!")

    try:
        allPosts = db.query(Post).filter(Post.authorId == userInfo.id).all()
        return allPosts
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to fetch all posts: {e}")


@postRouters.post("/create", status_code=status.HTTP_201_CREATED)
async def createPost(newPost:PostBase, db:Session = Depends(getDB), userInfo:UserOut = Depends(getUser)):
    if not userInfo:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authorized!")

    try:
        post = Post(
            title = newPost.title,
            content = newPost.content,
            authorId = userInfo.id
        )
        db.add(post)
        db.commit()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to create new post: {e}")


@postRouters.delete("/remove", status_code=status.HTTP_204_NO_CONTENT)
async def deletePost(postId:int = Query(gt=0), db:Session = Depends(getDB), userInfo:UserOut = Depends(getUser)):
    if not postId:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Please provide the post id!")
        
    if not userInfo:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authorized!")
    
    isUser = db.query(Post).filter(Post.authorId == postId).first()
    
    if not isUser:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!") 
    
    try:
        db.delete(isUser)
        db.commit()
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to delete post: {e}")
