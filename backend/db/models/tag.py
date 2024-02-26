from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship, mapped_column, Mapped

from db.models.refrence import Reference
from db.base_class import Base


class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    url = Column(String)
