from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    avatar_url = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    
    # Roles: "admin" o "publisher"
    role = Column(String, default="publisher")
    
    # Para control de aprobación de nuevos publicadores
    is_active = Column(Boolean, default=False) 
    is_silenced = Column(Boolean, default=False)
    
    posts = relationship("Post", back_populates="author")
    

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    slug = Column(String, unique=True, index=True) # URL amigable
    content = Column(Text)
    image_url = Column(String, nullable=True) # Ruta a /static/...
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Si es False o Null, es un borrador o está "eliminado" (soft delete)
    is_visible = Column(Boolean, default=True)
    
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")