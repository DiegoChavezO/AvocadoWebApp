from fastapi import APIRouter, File, UploadFile
from typing import List
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

router = APIRouter()

# Carpeta para almacenar imágenes subidas
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Lista global para almacenar rutas de imágenes subidas
uploaded_images = []

@router.post("/upload/")
async def upload_images(files: List[UploadFile] = File(...)):
    """
    Subir una o más imágenes al servidor.
    """
    global uploaded_images
    for file in files:
        file_location = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # Agregar la ruta de la imagen a la lista de imágenes subidas
        uploaded_images.append({
            "filename": file.filename,
            "filepath": file_location
        })

    return {"message": f"{len(files)} imágenes subidas correctamente.", "uploaded_files": uploaded_images}
