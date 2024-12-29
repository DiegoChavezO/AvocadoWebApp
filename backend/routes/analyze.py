from fastapi import APIRouter
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from rembg import remove
import sys
import os
UPLOAD_FOLDER = "uploads"
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))
router = APIRouter()

@router.post("/analyze/")
def analyze_images():
    """
    Procesar el área dañada para las imágenes subidas.
    
    if not uploaded_images:
        return JSONResponse(status_code=400, content={"error": "No hay imágenes subidas para analizar."})
    """
    if not os.path.exists(UPLOAD_FOLDER):
        return JSONResponse(status_code=400, content={"error": "La carpeta 'uploads' no existe."})

    # Obtener la lista de archivos en la carpeta `uploads`
    image_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.lower().endswith((".png", ".jpg", ".jpeg"))]

    if not image_files:
        return JSONResponse(status_code=400, content={"error": "No hay imágenes para analizar en 'uploads'."})

    
    results = []
    for image_file in image_files: #uploaded_images
        #filepath = image_info["filepath"]
        #filename = image_info["filename"]

        try:
            image_path = os.path.join(UPLOAD_FOLDER, image_file)
            # Leer la imagen
            img = cv2.imread(image_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Remover el fondo
            img_no_bg = remove(img)

            # Aplicar un filtro Gaussiano
            img_gaussian = cv2.GaussianBlur(img_no_bg, (15, 15), 0)

            # Convertir a escala de grises
            img_gray = cv2.cvtColor(img_gaussian, cv2.COLOR_BGR2GRAY)

            # Umbralización para detectar el área del fruto
            _, mask = cv2.threshold(img_gray, 1, 255, cv2.THRESH_BINARY)
            pixels_total = np.sum(mask == 255)

            # Detectar área dañada (HSV)
            hsv_img = cv2.cvtColor(img_gaussian, cv2.COLOR_RGB2HSV)
            lower_bound = np.array([18, 0, 0])  # Valores mínimos de HSV
            upper_bound = np.array([23, 255, 255])  # Valores máximos de HSV
            mask_damage = cv2.inRange(hsv_img, lower_bound, upper_bound)

            # Calcular píxeles dañados
            pixels_damaged = np.sum(mask_damage == 255)

            # Calcular porcentaje de área dañada
            damage_percentage = (pixels_damaged / pixels_total) * 100 if pixels_total > 0 else 0

            # Agregar resultado
            results.append({
                "filename": image_file,
                "damage_percentage": round(damage_percentage, 2),
            })
        except Exception as e:
            results.append({"filename": image_file, "error": str(e)})

    return {"analyzed_images": results}
