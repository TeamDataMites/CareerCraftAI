from database.hashing import Hash
from database.models import DbUser
from schemas.user import UserBase, UserDisplay
from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status


def create_user(db: Session, request: UserBase):
    """

    :param db: Session
    :type request: object
    """
    pwd = Hash(request.password)
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=pwd.bcrypt()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_username(db: Session, username: str):
    username = db.query(DbUser).filter(username == DbUser.username).first()
    if not username:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with username {username} not found"
        )
    return username
