from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from .. import models, schemas
from ..dependencies import get_db, get_current_user # Importamos la nueva dependencia

router = APIRouter(prefix="/posts", tags=["Posts"])

# --- CREAR NOTICIA (Protegido) ---
@router.post("/", response_model=schemas.PostResponse)
def create_post(
    post: schemas.PostCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user) # <--- AQUÍ LA MAGIA
):
    if current_user.is_silenced:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para crear noticias."
        )
    # Usamos el ID del usuario logueado automáticamente
    db_post = models.Post(**post.dict(), author_id=current_user.id)
    db.add(db_post)
    
    try:
        db.commit()
        db.refresh(db_post)
    except IntegrityError:
        db.rollback() # Es buena práctica deshacer la transacción fallida
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El slug '{post.slug}' ya existe. Por favor, elige uno único."
        )
        
    return db_post

# --- LEER NOTICIAS (Público) ---
@router.get("/", response_model=List[schemas.PostResponse])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Solo mostramos las visibles
    return db.query(models.Post).filter(models.Post.is_visible == True).offset(skip).limit(limit).all()

# --- ELIMINAR NOTICIA (Soft Delete - Protegido) ---
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")
    
    # Solo el autor o un admin pueden borrar
    if post.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esto")

    # Eliminación suave (Soft Delete)
    post.is_visible = False
    db.commit()
    return None