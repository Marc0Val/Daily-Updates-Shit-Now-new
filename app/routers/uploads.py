from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
import uuid

router = APIRouter(prefix="/upload", tags=["Uploads"])

UPLOAD_DIR = "static/images"

# Asegurar que el directorio existe
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/image/")
async def upload_image(file: UploadFile = File(...)):
    # Validar extensión
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")

    # Generar nombre único (para evitar colisiones si suben dos veces "foto.jpg")
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = f"{UPLOAD_DIR}/{unique_filename}"

    # Guardar en disco
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar imagen: {str(e)}")

    # Devolver URL accesible (usaremos localhost por ahora, luego la IP del Pi)
    # Nota: En el frontend, concatenarán el dominio base.
    return {"url": f"/static/images/{unique_filename}"}