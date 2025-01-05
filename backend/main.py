import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import matplotlib
matplotlib.use("Agg")
#aqui comienza el codigo jeje
from fastapi import FastAPI
from routes.upload import router as upload_router
from routes.analyze import router as analyze_router
from routes.histograms import router as histograms_router
from routes.reset import router as reset_router
from routes.classification_model import router as classification_router
from routes.maturity import router as maturity_router
from routes.report import router as report_router

from fastapi.middleware.cors import CORSMiddleware
# Crear la aplicación FastAPI
from fastapi.staticfiles import StaticFiles
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #allow_origins=["http://127.0.0.1:5500"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Incluir los routers para los diferentes endpoints
app.include_router(upload_router, prefix="/api", tags=["Upload"])
app.include_router(analyze_router, prefix="/api", tags=["Analyze"])
app.include_router(histograms_router, prefix="/api")
app.include_router(reset_router, prefix="/api", tags=["Reset"])
app.include_router(classification_router, prefix="/api")
app.include_router(maturity_router, prefix="/api")
app.include_router(report_router, prefix="/api")

# Configuración para servir archivos estáticos
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/processed", StaticFiles(directory="processed"), name="processed")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/histograms", StaticFiles(directory="histograms"), name="histograms")
app.mount("/models", StaticFiles(directory="models"), name="models")
# Ruta principal para verificar el estado de la API
@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}

# Punto de entrada para ejecutar la aplicación
if __name__ == "__main__":
    import uvicorn

    # Usar el puerto definido en la variable de entorno PORT o 5500 por defecto
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)