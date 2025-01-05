from fastapi import APIRouter, File, UploadFile, Request
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
BACK_URL = ""
@router.post("/upload/")
async def upload_images(request: Request, files: List[UploadFile] = File(...)):
    """
    Subir una o más imágenes al servidor.
    """
    uploaded_images = []
    #global uploaded_images
    for file in files:
        file_location = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # Obtener el host dinámicamente
        base_url = str(request.base_url).rstrip("/")  # "https://<tu-cloud-run-url>"
        # Agregar la ruta de la imagen a la lista de imágenes subidas
        uploaded_images.append({
            "filename": file.filename,
            "url": f"{base_url}/uploads/{file.filename}"#"filepath": file_location
        })

    return {"message": f"{len(files)} imágenes subidas correctamente.", "uploaded_files": uploaded_images}
