import enum
from sqlalchemy import Column, Integer, Text, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped
from db.models.refrence import Reference
from db.models.tag import Tag
from db.base_class import Base



class Levels(enum.Enum):
    junior = "junior"
    midlevel = "midlevel"
    senior = "senior"

tags_association_table = Table(
    "tags_association_table",
    Base.metadata,
    Column(f"tag_id", ForeignKey(f"{Tag.__tablename__}.id")),
    Column("question_id", ForeignKey("questions.id")),
    extend_existing=True
)

references_association_table = Table(
    "references_association_table",
    Base.metadata,
    Column(f"reference_id", ForeignKey(f"{Reference.__tablename__}.id")),
    Column("question_id", ForeignKey("questions.id")),
    extend_existing=True
)

class Question(Base):
    __tablename__ = 'questions'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    question_text = Column(Text, nullable=False)
    answer = Column(Text)
    level = Column(Enum(Levels), nullable=False, default=Levels.midlevel)

    tags: Mapped[list[Tag]] = relationship(secondary=tags_association_table)
    references: Mapped[list[Reference]] = relationship(secondary=references_association_table) 

    def as_dict(self):
        data = super(Question, self).as_dict()
        data['level'] = self.level.value
        return data
    
    @property
    def str_level(self):
        print(self.level, "sadf")
        return self.level.value