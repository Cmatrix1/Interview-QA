from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base


class Reference(Base):
    __tablename__ = 'references'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    url = Column(String)
