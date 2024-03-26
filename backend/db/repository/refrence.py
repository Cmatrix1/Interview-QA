from sqlalchemy.orm import Session
from sqlalchemy import or_
from db.models.refrence import Reference


def get_mulitiple_references(references: list[str], db: Session):
    return db.query(
        Reference
        ).filter(
            or_(*[
                    Reference.url == url for url in references
                ])
        ).all()
        
def create_mulitiple_references(references: list[str], db: Session):
    new_references = [Reference(url=url) for url in references] 
    db.add_all(new_references)
    db.commit()
    return new_references