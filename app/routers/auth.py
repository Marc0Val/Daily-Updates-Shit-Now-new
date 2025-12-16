from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, models, schemas
from ..core import security

router = APIRouter(prefix="/auth", tags=["Authentication"])
get_db = database.get_db

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. Verificar existencia
    user_exists = db.query(models.User).filter(models.User.email == user.email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    # 2. Hashear password (AQUÍ ESTABA EL ERROR 500, AHORA CORREGIDO EN SECURITY)
    hashed_password = security.get_password_hash(user.password)
    
    # 3. Crear usuario
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role="publisher",
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(
        data={"sub": user.username, "id": user.id, "role": user.role}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/staff", response_model=list[schemas.UserResponse])
def get_staff(db: Session = Depends(get_db)):
    """
    Devuelve una lista de el personal (admins y publishers).
    Endpoint público para créditos o páginas de "quiénes somos".
    """
    staff = db.query(models.User).filter(models.User.role.in_(["admin","publisher"])).all()
    return staff