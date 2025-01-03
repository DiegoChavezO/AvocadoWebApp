from fastapi import APIRouter, Query
from typing import List
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np
import os

router = APIRouter()

# Carpeta de imágenes subidas
UPLOAD_FOLDER = "uploads"
# Modelos preentrenados

@router.post("/maturity/")
def classify_images():
    """
    Clasificar imágenes subidas utilizando el modelo seleccionado.
    """
 
    # Verificar que existan imágenes subidas
    image_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    if not image_files:
        return {"error": "No hay imágenes cargadas para clasificar."}

    # Cargar el modelo correspondiente
    model_path = "backend/models/modelo_entrenado_VGG16_nivel_maduración.keras"
    model = load_model(model_path)

    # Clases del modelo
    classes = ['Maduro', 'Inmaduro']
    results = []
    for img_file in image_files:
        img_path = os.path.join(UPLOAD_FOLDER, img_file)

        # Preprocesar la imagen
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        # Predicción
        predictions = model.predict(img_array)
        predicted_class_idx = int(np.argmax(predictions[0]))
        predicted_class = classes[predicted_class_idx]
        probability = float(np.max(predictions[0]))

        # Agregar resultado
        results.append({
            "filename": img_file,
            "class": predicted_class,
            "probability": round(probability * 100, 2)
        })

    return {"results": results}
