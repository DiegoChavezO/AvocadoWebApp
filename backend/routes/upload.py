from fastapi import APIRouter, File, UploadFile
from typing import List
import os
import sys
from fastapi.staticfiles import StaticFiles

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

router = APIRouter()

# Carpeta para almacenar imágenes subidas
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
router.mount("/uploads", StaticFiles(directory=UPLOAD_FOLDER), name="uploads")
# Lista global para almacenar rutas de imágenes subidas
#uploaded_images = []

@router.post("/upload/")
async def upload_images(files: List[UploadFile] = File(...)):
    """
    Subir una o más imágenes al servidor.
    """
    uploaded_images = []
    #global uploaded_images
    for file in files:
        file_location = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # Agregar la ruta de la imagen a la lista de imágenes subidas
        uploaded_images.append({
            "filename": file.filename,
            "url": f"http://127.0.0.1:8000/uploads/{file.filename}"#"filepath": file_location
        })

    return {"message": f"{len(files)} imágenes subidas correctamente.", "uploaded_files": uploaded_images}
