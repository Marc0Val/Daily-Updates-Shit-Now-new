from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database
from ..dependencies import get_db, get_current_active_admin

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(get_current_active_admin)] # ¡Bloqueo total para no admins!
)

# --- GESTIÓN DE USUARIOS ---

@router.get("/users", response_model=List[schemas.UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@router.patch("/users/{user_id}/status")
def update_user_status(
    user_id: int, 
    is_active: bool, 
    role: str = "publisher", # Opcional: cambiar rol
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user.is_active = is_active
    user.role = role
    db.commit()
    db.refresh(user)
    return {"message": f"Usuario {user.username} actualizado: Activo={is_active}, Rol={role}"}

@router.patch("/users/{user_id}/silence")
def silence_user(user_id: int, silence: bool, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user.is_silenced = silence
    db.commit()
    return {"message": f"Usuario {user.username} silenciado: {silence}"}
# --- GESTIÓN DE CONTENIDO (OJO DE SAURON) ---

@router.get("/posts", response_model=List[schemas.PostResponse])
def read_all_posts_admin(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # A diferencia del endpoint público, aquí NO filtramos por is_visible
    # Vemos todo: borradores y eliminados.
    return db.query(models.Post).offset(skip).limit(limit).all()

@router.patch("/posts/{post_id}/visibility")
def update_post_visibility(post_id: int, is_visible: bool, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")
        
    post.is_visible = is_visible
    db.commit()
    return {"message": f"Visibilidad de la noticia '{post.title}' actualizada a: {is_visible}"}

@router.patch("/posts/{post_id}/restore")
def restore_post(post_id: int, db: Session = Depends(get_db)):
    # Revivir un post eliminado
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")
    
    post.is_visible = True
    db.commit()
    return {"message": "Noticia restaurada y visible al público"}