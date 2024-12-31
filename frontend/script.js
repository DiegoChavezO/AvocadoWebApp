let uploadedImages = [];
let currentIndex = 0;

// Función para mostrar una imagen en el placeholder
function displayImage(index) {
    const imageDisplay = document.getElementById("image-display");
    imageDisplay.style.backgroundImage = `url(${uploadedImages[index]})`;
}
// Evento para subir imágenes
document.getElementById("uploadForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById("fileInput");
    const formData = new FormData();

    // Agregar múltiples archivos al FormData
    for (const file of fileInput.files) {
        formData.append("files", file);
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/api/upload/", {
            method: "POST",
            body: formData,
        });

        const result = await response.json();
        console.log(result);  // Manejo de resultado en la consola

        // Guardar las URLs de las imágenes subidas
        uploadedImages = result.uploaded_files.map((file) => file.url);

        if (uploadedImages.length > 0) {
            currentIndex = 0;
            displayImage(currentIndex);

            // Habilitar los botones si hay más de una imagen
            if (uploadedImages.length > 1) {
                document.getElementById("prevButton").disabled = false;
                document.getElementById("nextButton").disabled = false;
            }

            // Habilitar el botón de analizar
            document.getElementById("analyzeButton").disabled = false;
        } else {
            alert("No se subieron imágenes.");
        }

    } catch (error) {
        alert("Hubo un error al subir las imágenes.");
        console.error(error);
    }
});

// Evento para analizar las imágenes subidas
document.getElementById("analyzeButton").addEventListener("click", async () => {
    try {
        const response = await fetch("http://127.0.0.1:8000/api/analyze/", {
            method: "POST",
        });

        const result = await response.json();
        console.log(result);  // Manejo de resultado en la consola

        // Mostrar resultados en el frontend
        const resultContainer = document.getElementById("result");
        resultContainer.innerHTML = ""; // Limpiar resultados previos

        result.analyzed_images.forEach((image) => {
            const div = document.createElement("div");

            if (image.error) {
                div.innerText = `Error con la imagen ${image.filename}: ${image.error}`;
            } else {
                div.innerText = `Imagen: ${image.filename}, Área dañada: ${image.damage_percentage}%`;
            }

            resultContainer.appendChild(div);
        });

        document.getElementById("result").style.display = "block";

    } catch (error) {
        alert("Hubo un error al analizar las imágenes.");
        console.error(error);
    }
});
// Navegación entre imágenes
document.getElementById("prevButton").addEventListener("click", () => {
    if (currentIndex > 0) {
        currentIndex--;
        displayImage(currentIndex);
    }
});

document.getElementById("nextButton").addEventListener("click", () => {
    if (currentIndex < uploadedImages.length - 1) {
        currentIndex++;
        displayImage(currentIndex);
    }
});

//deslizadores
// Actualiza el campo numérico cuando el slider cambia
function updateSliderValue(inputId, value) {
    const inputElement = document.getElementById(inputId);
    inputElement.value = value;
}

// Actualiza el slider cuando el valor del campo numérico cambia
function updateInputValue(sliderId, value) {
    const sliderElement = document.getElementById(sliderId);
    const parsedValue = parseInt(value, 10);

    // Validar que el valor esté dentro del rango del slider
    if (parsedValue >= parseInt(sliderElement.min, 10) && parsedValue <= parseInt(sliderElement.max, 10)) {
        sliderElement.value = parsedValue;
    } else {
        alert(`El valor debe estar entre ${sliderElement.min} y ${sliderElement.max}.`);
    }

    // Sincronizar el valor del slider con el input
    sliderElement.dispatchEvent(new Event("input"));
}