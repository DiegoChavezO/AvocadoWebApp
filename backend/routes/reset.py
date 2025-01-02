from fastapi import APIRouter
import os
import shutil

router = APIRouter()

# Carpeta de imágenes subidas y procesadas
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
HISTOGRAM_FOLDER = "histograms"

@router.post("/reset/")
def reset_application():
    """
    Eliminar todas las imágenes subidas y procesadas.
    """
    try:
        # Eliminar imágenes subidas
        if os.path.exists(UPLOAD_FOLDER):
            shutil.rmtree(UPLOAD_FOLDER)
            os.makedirs(UPLOAD_FOLDER)

        # Eliminar imágenes procesadas
        if os.path.exists(PROCESSED_FOLDER):
            shutil.rmtree(PROCESSED_FOLDER)
            os.makedirs(PROCESSED_FOLDER)

        # Eliminar histogramas
        if os.path.exists(HISTOGRAM_FOLDER):
            shutil.rmtree(HISTOGRAM_FOLDER)
            os.makedirs(HISTOGRAM_FOLDER)

        return {"message": "Aplicación reiniciada con éxito."}
    except Exception as e:
        return {"error": str(e)}
