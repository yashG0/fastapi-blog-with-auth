from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from ..models import Comment, Post
from ..db import getDB
from .auth_routers import getUser
from ..schemas import CommentBase, UserOut


commentRouters = APIRouter(prefix="/api/comment", tags=["My Comment Routes"])

@commentRouters.get("/all", status_code=status.HTTP_200_OK)
async def allComments(postId:int, db:Session = Depends(getDB)):
    try:
        allComments = db.query(Comment).filter(Comment.postId == postId).all()
        return allComments
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to fetch comments {e}")

@commentRouters.post("/add", status_code=status.HTTP_201_CREATED)
async def addComment(comment:CommentBase, db:Session = Depends(getDB), userInfo:UserOut = Depends(getUser)):
    if not userInfo:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authorized!")
        
    # print(userInfo)
    isPost = db.query(Post).filter(Post.id == comment.postId).first()
    if not isPost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {comment.postId} not found!")
        
    try:
        newComment = Comment(
            content = comment.content,
            authorId = userInfo.id,
            postId = comment.postId
        )
        db.add(newComment)
        db.commit()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to add comment {e}")

@commentRouters.delete("/remove", status_code=status.HTTP_204_NO_CONTENT)
async def deleteComment(postId:int = Query(gt=0), commentId:int = Query(gt=0), db:Session = Depends(getDB), userInfo:UserOut = Depends(getUser)):
    isComment = db.query(Comment).filter(Comment.postId == postId).filter(Comment.id == commentId).first()
    print(isComment)
    if not isComment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found!")

    try:
        db.delete(isComment)
        db.commit()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to delete comment: {e}")
