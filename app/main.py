from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware  # <--- IMPORTANTE
from .database import engine
from . import models
from .routers import auth, posts, uploads, admin, users

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Daily Update Shit News API",
    description="Backend Modular O.R.I.O.N. - v1.0",
    version="1.0.0"
)

# --- CONFIGURACIÓN CORS (EL PUENTE AL FRONTEND) ---
origins = [
    "http://localhost",
    "http://localhost:3000", # Puerto típico de React local
    "http://localhost:5173", # Puerto típico de Vite (React moderno)
    "*"                      # (Opcional: Permitir todo para desarrollo rápido)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción real, cambia esto por la lista 'origins'
    allow_credentials=True,
    allow_methods=["*"], # Permitir GET, POST, PUT, DELETE, etc.
    allow_headers=["*"], # Permitir todos los headers (Authorization, etc.)
)
# --------------------------------------------------

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(uploads.router)
app.include_router(admin.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"O.R.I.O.N.": "Backend Listo. CORS Habilitado."}