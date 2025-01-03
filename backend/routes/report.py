from fastapi import APIRouter
from fastapi.responses import FileResponse
from reportlab.pdfgen import canvas
import os

router = APIRouter()

# Carpeta donde se guardarán los PDFs generados
PDF_FOLDER = "reports"
os.makedirs(PDF_FOLDER, exist_ok=True)

@router.post("/analysis/")
def generate_analysis():
    """
    Generar un análisis completo en formato PDF.
    """
    # Verificar que existan imágenes subidas
    UPLOAD_FOLDER = "uploads"
    PROCESSED_FOLDER = "processed"
    uploaded_images = [f for f in os.listdir(UPLOAD_FOLDER) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    processed_images = [f for f in os.listdir(PROCESSED_FOLDER) if f.lower().endswith((".png", ".jpg", ".jpeg"))]

    if not uploaded_images:
        return {"error": "No hay imágenes cargadas para analizar."}

    # Archivo PDF
    pdf_filename = os.path.join(PDF_FOLDER, "analysis_report.pdf")
    c = canvas.Canvas(pdf_filename)

    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 800, "Reporte de Análisis Completo")
    c.setFont("Helvetica", 12)
    c.drawString(50, 780, f"Total de imágenes cargadas: {len(uploaded_images)}")

    y_position = 760
    for idx, img_file in enumerate(uploaded_images):
        c.drawString(50, y_position, f"{idx+1}. Imagen: {img_file}")

        # Resultados ficticios (en tu implementación, estos deben obtenerse de las funciones reales)
        damage_result = "10% área dañada"  # Aquí debes incluir el cálculo real
        classification_result = "Clasificación: Sano, Probabilidad: 85.00%"  # Aquí debes incluir la clasificación real
        c.drawString(50, y_position - 20, f"   {damage_result}")
        c.drawString(50, y_position - 40, f"   {classification_result}")

        # Agregar imágenes
        try:
            image_path = os.path.join(PROCESSED_FOLDER, img_file)
            c.drawImage(image_path, 50, y_position - 150, width=200, height=150)
            y_position -= 200
        except Exception as e:
            c.drawString(50, y_position, f"   (Error al cargar la imagen: {e})")
            y_position -= 40

        # Salto de página si es necesario
        if y_position < 100:
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = 760

    # Guardar PDF
    c.save()

    # Devolver el PDF generado
    return FileResponse(pdf_filename, media_type="application/pdf", filename="analysis_report.pdf")
