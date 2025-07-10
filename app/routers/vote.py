from fastapi import APIRouter, status, Depends, HTTPException
from ..database import get_db
from .. import schemas, oauth2, models
from sqlalchemy.orm import session

router = APIRouter(
    prefix="/vote",
    tags=['Votes']  
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: schemas.Vote, db: session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    query_vote = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_post = query_vote.first()
    if (vote.dir == 1):
        if found_post:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User {current_user.id}  has been alresdy voted on post {vote.post_id}"
        )
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="vote does not exit!"
            )
        query_vote.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully removed vote"}