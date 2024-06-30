from firebase_admin import auth, credentials, initialize_app
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import firebase_admin
from schemas.user import UserBase


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

cred = credentials.Certificate("auth/careercraftai-96e2b-firebase-adminsdk-viemq-c5dd6364ba.json")
firebase_admin.initialize_app(cred)

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")


@router.get("/protected")
def protected_route(token: dict = Depends(verify_token)):
    return {"message": "This is a protected route", "user_id": token["uid"]}

@router.post("/login")
async def login(user: UserBase):
    try:
        user = auth.get_user_by_email(user.email)
        
        custom_token = auth.create_custom_token(user.uid)
        
        return {"token": custom_token.decode(), "uid": user.uid}
    except auth.AuthError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/logout")
async def logout(token: dict = Depends(verify_token)):
    try:
        # Revoke refresh tokens for the user
        auth.revoke_refresh_tokens(token["uid"])
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Logout failed")
