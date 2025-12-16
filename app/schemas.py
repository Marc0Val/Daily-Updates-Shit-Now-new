from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- Esquemas de POSTS (Noticias) ---

class PostBase(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None
    slug: str

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    is_visible: bool
    author_id: int

    class Config:
        orm_mode = True

# --- Esquemas de USUARIOS ---

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str  # Solo pedimos password al crear, nunca la devolvemos

class UserResponse(UserBase):
    id: int
    is_active: bool
    role: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    posts: List[PostResponse] = []

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None

class Config:
        from_attributes = True