from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    password: str


class UserDisplay(BaseModel):
    email: str

    class Config:
        from_attributes = True


class UserAuth(BaseModel):
    email: str
