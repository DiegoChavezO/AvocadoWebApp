from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from rembg import remove
import sys
import os
from pathlib import Path

#sys.path.append(os.path.dirname(os.path.abspath(__file__)))
router = APIRouter()
# Directorio para guardar imágenes procesadas
PROCESSED_FOLDER = "processed"
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
UPLOAD_FOLDER = "uploads"

@router.post("/analyze/")
async def analyze_images(request:Request):
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

     # Leer valores de los sliders del frontend
    body = await request.json() ####
    rango_min = np.array([body["h_min"], body["s_min"], body["v_min"]], np.uint8) ####
    rango_max = np.array([body["h_max"], body["s_max"], body["v_max"]], np.uint8)####
    
    results = []
    for image_file in image_files: #uploaded_images     
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
            #lower_bound = np.array([18, 0, 0])  # Valores mínimos de HSV
            #upper_bound = np.array([23, 255, 255])  # Valores máximos de HSV
            ###mask_damage = cv2.inRange(hsv_img, lower_bound, upper_bound)
            mask_damage = cv2.inRange(hsv_img, rango_min, rango_max) ####
            # Calcular píxeles dañados
            pixels_damaged = np.sum(mask_damage == 255)

            # Calcular porcentaje de área dañada
            damage_percentage = (pixels_damaged / pixels_total) * 100 if pixels_total > 0 else 0

            ################################################################
            # Crear imagen segmentada con fondo conservado y área dañada marcada
            mask_damage_3ch = cv2.cvtColor(mask_damage, cv2.COLOR_GRAY2RGB)  # Convertir la máscara de daño a 3 canales
            segmentada_con_fondo = cv2.bitwise_and(img, img, mask=mask_damage)  # Aplicar máscara de daño sobre la imagen original

            # Superponer la máscara sobre la imagen original para conservar el fondo y resaltar el daño
            segmentada_con_fondo = cv2.addWeighted(img, 0.7, mask_damage_3ch, 0.3, 0)  # Mezcla con transparencia
             # Guardar imagen segmentada
            processed_image_path = os.path.join(PROCESSED_FOLDER, f"processed_{image_file}")
            cv2.imwrite(processed_image_path, cv2.cvtColor(segmentada_con_fondo, cv2.COLOR_RGB2BGR))


            # Agregar resultado
            results.append({
                "filename": image_file,
                "damage_percentage": round(damage_percentage, 2),
                "processed_image_url": f"/{PROCESSED_FOLDER}/{Path(processed_image_path).name}" ###
            })
        except Exception as e:
            results.append({"filename": image_file, "error": str(e)})

    return {"analyzed_images": results}
