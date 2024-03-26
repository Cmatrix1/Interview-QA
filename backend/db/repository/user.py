from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
from db.models.user import User
from schemas.user import UserCreate
from utils.security import hashing
from utils.exceptions.user import UserAlreadyExistsException, UserNotFoundException


def create_new_user(user: UserCreate, db: Session):
    user = User(
        username=user.username,
        password=hashing.get_password_hash(user.password),
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        raise UserAlreadyExistsException()
    return user


def get_user_for_authentication(username: str, db: Session, raise_exceptions: bool = True) -> User | None:
    user = db.query(User.id, User.username).filter(User.username == username).first()
    if user is None and raise_exceptions:
        raise UserNotFoundException()
    return user


def get_user(username: str, db: Session, raise_exceptions: bool = True) -> User | None:
    user = db.query(User.id, User.username, User.password).filter(User.username == username).first()
    if user is None and raise_exceptions:
        raise UserNotFoundException()
    return user