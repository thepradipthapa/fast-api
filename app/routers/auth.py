from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, oauth2
from .. import utils

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)
@router.post("/login", status_code=status.HTTP_200_OK)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session= Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email==user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Create Access Token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"sms": "Login successfull", "access_token": access_token, "token_type": "bearer"}