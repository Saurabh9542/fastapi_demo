from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import database, models, oath, schemas

router = APIRouter(
    prefix="/vote",
    tags=["VOTE"]
)


@router.post("/")
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), curr_user: int = Depends(oath.get_current_user)):
 
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == curr_user.id)

    vote_found = vote_query.first()
    if (vote.dir == 1):
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {curr_user.id} has already voted on the post {vote.post_id} ")
        
        new_vote = models.Vote(post_id = vote.post_id, user_id = curr_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
    
    else:
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        
        vote_query.delete()
        db.commit()

        return {"message": "successfully deleted vote"}
        




