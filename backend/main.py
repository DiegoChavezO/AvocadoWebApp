import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#aqui comienza el codigo jeje
from fastapi import FastAPI
from routes.upload import router as upload_router
from routes.analyze import router as analyze_router
from fastapi.middleware.cors import CORSMiddleware
# Crear la aplicación FastAPI
from fastapi.staticfiles import StaticFiles
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Cambia esto al puerto de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Incluir los routers para los diferentes endpoints
app.include_router(upload_router, prefix="/api", tags=["Upload"])
app.include_router(analyze_router, prefix="/api", tags=["Analyze"])
# Configuración para servir archivos estáticos
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
# Ruta principal para verificar el estado de la API
@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}
