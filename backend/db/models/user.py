from sqlalchemy import Column, DateTime, Integer, String, Text, Enum
from sqlalchemy.sql import func

from db.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    username = Column(String(255), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    role = Column(Enum("admin", "writer", "user", name="user_role_type"), default="user")
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<User id={self.id}, username={self.username}, role={self.role}>"