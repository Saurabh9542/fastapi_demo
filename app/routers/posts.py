from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func

from typing import Optional, List


from ..database import get_db

from .. import models, schemas, utils, oath

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)



@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), curr_user: int = Depends(oath.get_current_user)):
    # posts = db.query(models.Post).all()

    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).outerjoin(models.Vote, models.Post.id == models.Vote.post_id).group_by(models.Post.id).all()
    print(result)


    return result
    # return list(result)



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db:Session=Depends(get_db), curr_user: int = Depends(oath.get_current_user)):
    new_post = models.Post(owner_id=curr_user.id, **post.dict())
    print(curr_user)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), curr_user: int = Depends(oath.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id :{id} does not exist")
    
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), curr_user: int = Depends(oath.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    if post.owner_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorised to perform this action.")
    

    post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

        
@router.put("/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), response_model=schemas.Post,
    curr_user: int = Depends(oath.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id :{id} does not exist")
    
    if post.owner_id != curr_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorised to perform this action.")

    post_query.update(updated_post.dict(), synchronize_session = False)
    db.commit()

    return post_query.first()
