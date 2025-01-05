from fastapi import APIRouter, HTTPException
import os
import cv2
from typing import List
import matplotlib.pyplot as plt
from io import BytesIO
from fastapi.responses import FileResponse
from pydantic import BaseModel

router = APIRouter()

# Carpeta para almacenar los histogramas generados
OUTPUT_FOLDER = "histograms"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

UPLOAD_FOLDER = "uploads"

# Modelo para la solicitud
class HistogramRequest(BaseModel):
    mode: str

def save_histogram(image, mode, filename):
    plt.figure(figsize=(8, 4))
    if mode == "rgb":
        colors = ("r", "g", "b")
        for i, color in enumerate(colors):
            plt.hist(image[:, :, i].ravel(), bins=256, color=color, alpha=0.5, label=color)
    elif mode == "hsv":
        colors = ("purple", "orange", "blue")
        labels = ["Hue", "Saturation", "Value"]
        for i, color in enumerate(colors):
            plt.hist(image[:, :, i].ravel(), bins=256, color=color, alpha=0.5, label=labels[i])
    elif mode == "lab":
        labels = ["Lightness", "A (Red-Green)", "B (Blue-Yellow)"]
        colors = ("gray", "red", "yellow")
        for i, color in enumerate(colors):
            plt.hist(image[:, :, i].ravel(), bins=256, color=color, alpha=0.5, label=labels[i])

    plt.legend()
    plt.title(f"Histogram for {mode.upper()}")
    output_path = os.path.join(OUTPUT_FOLDER, f"{filename}_{mode}.png")
    plt.savefig(output_path)
    plt.close()
    return output_path

@router.post("/histograms/")
def generate_histograms(request: HistogramRequest):
    mode = request.mode.lower()
    if mode not in ["rgb", "hsv", "lab"]:
        raise HTTPException(status_code=400, detail="Modo no válido. Debe ser 'rgb', 'hsv' o 'lab'.")

    image_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    if not image_files:
        raise HTTPException(status_code=400, detail="No hay imágenes para procesar.")

    histogram_paths = []
    for image_file in image_files:
        image_path = os.path.join(UPLOAD_FOLDER, image_file)
        image = cv2.imread(image_path)
        if mode == "hsv":
            image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        elif mode == "lab":
            image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

        histogram_path = save_histogram(image, mode, os.path.splitext(image_file)[0])
        histogram_paths.append(histogram_path)

    return {"histograms": histogram_paths}
