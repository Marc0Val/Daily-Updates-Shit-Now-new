from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

# Configuración de Hashing (Seguridad Básica)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# --- USUARIOS ---

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    # Por defecto, el primer usuario podría ser admin, pero por ahora todos son 'publisher'
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role="publisher", 
        is_active=True # Lo activamos directo para pruebas rápidas
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- POSTS ---

def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(**post.dict(), author_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    # Solo traemos los visibles
    return db.query(models.Post).filter(models.Post.is_visible == True).offset(skip).limit(limit).all()