#librerias del servidor
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
#librerias de la aplicacion
from rembg import remove
import cv2
import numpy as np
import os
#librerias internas
#from utils.image_processing import calculate_damage_area


# Crear la aplicación FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Cambia esto al puerto de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Carpeta para guardar las imágenes subidas
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    """
    Carga una imagen, procesa el área dañada y devuelve el porcentaje.
    """
    # Guardar el archivo en el servidor
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Leer la imagen
    try:
        img = cv2.imread(file_location)
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

        # Eliminar el archivo procesado (opcional)
        os.remove(file_location)

        # Retornar el resultado
        # return {
        #    "filename": file.filename,
            ##   "pixels_total": pixels_total,
            #  "pixels_damaged": pixels_damaged,
            #  "damage_percentage": round(damage_percentage, 2),
        #}
        return {
            "filename": file.filename,
            "pixels_total": int(pixels_total),  # Convertir a int
            "pixels_damaged": int(pixels_damaged),  # Convertir a int
            "damage_percentage": float(round(damage_percentage, 2)),  # Asegurarse de que sea float
            }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
