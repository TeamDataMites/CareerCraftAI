from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth.oauth2 import create_access_token
from database.database import get_db
from database.hashing import Hash
from database.models import DbUser

router = APIRouter(
    tags=['authentication']
)


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(request.username == DbUser.username).first()
    if not user:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
        )
    if not Hash(request.password).verify(user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect password"
        )

    access_token = create_access_token(data={"username": user.username})

    return {
        'access_token': access_token,
        'access_type': 'bearer',
        'id': user.id,
        'username': user.username
    }
