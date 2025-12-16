import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Daily Update Shit News"
    PROJECT_VERSION: str = "1.0.0"
    
    # En producción (Pi 4), usaremos variables de entorno reales
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super_secreto_007_orion_v1")
    ALGORITHM: str = "HS256"    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 2  # 2 horas

settings = Settings()