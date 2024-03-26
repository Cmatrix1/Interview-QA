from sqlalchemy.orm import Session
from sqlalchemy import or_
from db.models.tag import Tag 


def get_mulitiple_tags(tags: list[str], db: Session) -> list[Tag]:
    return db.query(
        Tag
        ).filter(
            or_(*[
                    Tag.name == name for name in tags
                ])
        ).all()
        
def create_mulitiple_tags(tags: list[str], db: Session) -> list[Tag]:
    new_tags = [Tag(name=name) for name in tags] 
    db.add_all(new_tags)
    db.commit()
    return new_tags