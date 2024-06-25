from sqlalchemy.orm import relationship

from database.database import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey


class DbUser(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    items = relationship('DbPost', back_populates='user')