from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..dependencies import get_db, get_current_user
from ..core import security

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.patch("/me", response_model=schemas.UserResponse)
def update_current_user(
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Obtener los datos del body que no son None
    update_data = user_update.dict(exclude_unset=True)

    # Si se envía 'username', verificar que no esté en uso por otro usuario
    if "username" in update_data and update_data["username"] != current_user.username:
        user_exists = db.query(models.User).filter(models.User.username == update_data["username"]).first()
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya está en uso."
            )
    
    # Si se envía 'password', hashearlo
    if "password" in update_data:
        hashed_password = security.get_password_hash(update_data["password"])
        update_data["hashed_password"] = hashed_password
        del update_data["password"] # No guardar la contraseña en texto plano

    # Actualizar los campos del usuario actual
    for key, value in update_data.items():
        setattr(current_user, key, value)

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    return current_user