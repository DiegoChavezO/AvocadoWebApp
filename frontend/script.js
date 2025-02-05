let uploadedImages = [];
let currentIndex = 0;

let processedImages = []; // Lista de URLs de imágenes procesadas
let currentProcessedIndex = 0; // Índice actual de la imagen procesada

//colocar 1 para el local, 2 para el final
const BACKEND_URL = "https://aplicacion-backend-v2-565329448277.us-central1.run.app"//"https://b8edfad75318-565329448277.us-central1.run.app"; //http://127.0.0.1:8080
const dec = 0

//dec = 0 ? BACKEND_URL="http://127.0.0.1:8000" : BACKEND_URL="https://<tu-backend-url>.run.app";

// Función para mostrar una imagen en el placeholder
function displayImage(index) {
    const imageDisplay = document.getElementById("image-display");
    imageDisplay.style.backgroundImage = `url(${uploadedImages[index]})`;
}
// Función para mostrar la segunda imagen (segmentada)en el segundo placeholder
// Actualizar la vista del segundo placeholder
function updateProcessedImageDisplay() {
    if (processedImages.length > 0) {
        const imageDisplay2 = document.getElementById("image-display2");
        imageDisplay2.style.backgroundImage = `url(${processedImages[currentProcessedIndex]})`;

        // Habilitar/deshabilitar botones de navegación
        document.getElementById("prevButton2").disabled = false;
        document.getElementById("nextButton2").disabled = false;
    } else {
        // Si no hay imágenes, deshabilitar los botones
        document.getElementById("prevButton2").style.backgroundImage = '';
        document.getElementById("nextButton2").disabled = true;
        document.getElementById("prevButton2").disabled = true;
    }
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
        const response = await fetch(`https://aplicacion-backend-v2-565329448277.us-central1.run.app/api/upload/`, { //fetch("http://127.0.0.1:8000/api/upload/"
            method: "POST",
            body: formData,
        });

        const result = await response.json();
        console.log(result);  // Manejo de resultado en la consola
        alert(result.message);

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

            // Habilitar el botón de analizar y los demas
            document.getElementById("analyzeButton").disabled = false;
            document.getElementById("histograma").disabled = false;
            document.getElementById("reset-button").disabled = false;
            document.getElementById("maturity-button").disabled = false;
            document.getElementById("analysis-button").disabled = false
            document.getElementById("modelButton").disabled = false
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
    ///
    const hMin = document.getElementById("h-min").value;
    const hMax = document.getElementById("h-max").value;
    const sMin = document.getElementById("s-min").value;
    const sMax = document.getElementById("s-max").value;
    const vMin = document.getElementById("v-min").value;
    const vMax = document.getElementById("v-max").value;
    ////
    try {
        const response = await fetch(`${BACKEND_URL}/api/analyze/`, { //MODIFICADO "http://127.0.0.1:8000/api/analyze/"
            method: "POST",
           /////////
            eaders: { "Content-Type": "application/json" },
            body: JSON.stringify({
                h_min: parseInt(hMin),
                h_max: parseInt(hMax),
                s_min: parseInt(sMin),
                s_max: parseInt(sMax),
                v_min: parseInt(vMin),
                v_max: parseInt(vMax),
            }),
        });

        const result = await response.json();
        console.log(result);  // Manejo de resultado en la consola
        alert(result.message); //experimento

        // Mostrar resultados en el frontend
        const resultContainer = document.getElementById("result");
        resultContainer.innerHTML = ""; // Limpiar resultados previos
        // Limpiar y actualizar la lista de imágenes procesadas
        processedImages = [];
        
        
        result.analyzed_images.forEach((image) => {
            const div = document.createElement("div");

            if (image.error) {
                div.innerText = `Error con la imagen ${image.filename}: ${image.error}`;
            } else {
                div.innerText = `Imagen: ${image.filename}, Área dañada: ${image.damage_percentage}%`;
                processedImages.push(`${BACKEND_URL}${image.processed_image_url}`); //`http://127.0.0.1:8000${image.processed_image_url}`
            }

            resultContainer.appendChild(div);
        });

        document.getElementById("result").style.display = "block";
        // Mostrar la primera imagen procesada
        currentProcessedIndex = 0;
        updateProcessedImageDisplay();

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

// Eventos para navegación entre imágenes procesadas
document.getElementById("prevButton2").addEventListener("click", () => {
    if (processedImages.length > 0) {
        currentProcessedIndex = (currentProcessedIndex - 1 + processedImages.length) % processedImages.length;
        updateProcessedImageDisplay();
    }
});

document.getElementById("nextButton2").addEventListener("click", () => {
    if (processedImages.length > 0) {
        currentProcessedIndex = (currentProcessedIndex + 1) % processedImages.length;
        updateProcessedImageDisplay();
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

/*
document.getElementById("comboBox-histogramas").addEventListener("change", () => {
    document.getElementById("histograma").disabled = false;
});
*/
// Función para mostrar la imagen generada
function showHistogramPopup(histogramUrl,imageTitle) {
    const popupWindow = window.open("", "_blank", "width=800,height=600");
    popupWindow.document.write(`
        <html>
        <head>
            <title>Histograma</title>
        </head>
        <body>
            <h2>Titulo: ${imageTitle}</h2>
            <br>
            <img src="${histogramUrl}" alt="Histograma" style="width:100%; height:auto;">
            <br>
            <a href="${histogramUrl}" download>Descargar Histograma</a>
        </body>
        </html>
    `);
    popupWindow.document.close();
}

// Manejo del botón para generar histogramas
document.getElementById("histograma").addEventListener("click", async () => {
    const mode = document.getElementById("comboBox-histogramas").value.toLowerCase();
    try {
        const response = await fetch(`${BACKEND_URL}/api/histograms/`, { //"http://127.0.0.1:8000/api/histograms/" CHECKAR EH 
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ mode }),
        });

        const result = await response.json();
        if (response.ok) {
            // Mostrar cada histograma en el pop-up
            result.histograms.forEach((histogramUrl) => {
                const imageTitle = histogramUrl.split("/").pop(); // Extrae el nombre del archivo
                showHistogramPopup(`${BACKEND_URL}/${histogramUrl}`,imageTitle); //(`http://127.0.0.1:8000/${histogramUrl}
            });
        } else {
            alert("Error al generar histogramas: " + result.detail);
        }
    } catch (error) {
        console.error("Error al generar histogramas:", error);
    }
});

document.getElementById("reset-button").addEventListener("click", async () => {
    if (!confirm("¿Estás seguro de que deseas reiniciar? Se eliminarán todas las imágenes subidas y generadas.")) {
        return;
    }
    try {
        const response = await fetch(`${BACKEND_URL}/api/reset/`, { //fetch("http://127.0.0.1:8000/api/reset/",
            method: "POST",
        });

        const result = await response.json();
        console.log(result.message);

        // Limpiar los resultados en el frontend
        const resultContainer = document.getElementById("result");
        if (resultContainer) {
            resultContainer.innerHTML = ""; // Limpia el contenido del área de resultados
        }

        // Restablecer los placeholders de las imágenes
        const placeholders = document.querySelectorAll(".image-placeholder");
        placeholders.forEach((placeholder) => {
            if (placeholder) {
                placeholder.style.backgroundImage = "none"; // Quitar la imagen
            }
        });

        // Desactivar botones nuevamente
        document.getElementById("analyzeButton").disabled = true;
        document.getElementById("histograma").disabled = true;
        document.getElementById("prevButton").disabled = true;
        document.getElementById("nextButton").disabled = true;
        document.getElementById("prevButton2").disabled = true;
        document.getElementById("nextButton2").disabled = true;

        document.getElementById("reset-button").disabled = false;
        document.getElementById("maturity-button").disabled = true;
        document.getElementById("analysis-button").disabled = true;
        document.getElementById("modelButton").disabled = true;


        alert("Aplicación reiniciada con éxito.");
    } catch (error) {
        console.error("Error al reiniciar:", error);
        alert("Hubo un error al intentar reiniciar la aplicación.");
    }
});


// Evento para clasificar imágenes
document.getElementById("modelButton").addEventListener("click", async () => {
    const comboBox = document.getElementById("comboBox");
    const selectedModel = comboBox.value === "opcion1" ? "VGG16" : "MobileNetV2";

    try {
        const response = await fetch(`${BACKEND_URL}/api/classify/?model_type=${selectedModel}`, { //`http://127.0.0.1:8000/api/classify/?model_type=${selectedModel}`,
            method: "POST",
        });

        const result = await response.json();
        console.log(result);

        // Mostrar resultados en el área de resultados
        const resultContainer = document.getElementById("result");
        resultContainer.innerHTML = ""; // Limpiar resultados previos

        if (result.error) {
            resultContainer.innerHTML = `<p>Error: ${result.error}</p>`;
        } else {
            result.results.forEach((res) => {
                const div = document.createElement("div");
                div.innerHTML = `Imagen: <strong>${res.filename}</strong>, Clase: <strong>${res.class}</strong>, Probabilidad: <strong>${res.probability}%</strong>`;
                resultContainer.appendChild(div);
            });
        }

        document.getElementById("result").style.display = "block";
    } catch (error) {
        console.error("Error al clasificar imágenes:", error);
    }
});


document.getElementById("maturity-button").addEventListener("click", async () => {
    
    //const response = "http://127.0.0.1:8000/api/maturity/"
    const response = await fetch(`${BACKEND_URL}/api/maturity/`, { // http://127.0.0.1:8000/api/maturity/
        method: "post",
    })
    try {
        const result = await response.json();
        console.log(result);

        // Mostrar resultados en el área de resultados
        const resultContainer = document.getElementById("result");
        resultContainer.innerHTML = ""; // Limpiar resultados previos

        if (result.error) {
            resultContainer.innerHTML = `<p>Error: ${result.error}</p>`;
        } else {
            result.results.forEach((res) => {
                const div = document.createElement("div");
                div.innerHTML = `Imagen: <strong>${res.filename}</strong>, Clase: <strong>${res.class}</strong>, Probabilidad: <strong>${res.probability}%</strong>`;
                resultContainer.appendChild(div);
            });
        }

        document.getElementById("result").style.display = "block";
    } catch (error) {
        console.error("Error al clasificar imágenes:", error);
    }
});

// Botón para análisis completo
document.getElementById("analysis-button").addEventListener("click", async () => {
    try {
        const response = await fetch(`${BACKEND_URL}/api/analysis/`, { // fetch("http://127.0.0.1:8000/api/analysis/"
            method: "POST",
        });

        if (!response.ok) {
            throw new Error("Error al generar el análisis completo");
        }

        // Descargar el PDF generado
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.style.display = "none";
        a.href = url;
        a.download = "analysis_report.pdf";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error("Error al generar el análisis completo:", error);
        alert("Hubo un error al generar el análisis completo.");
    }
});
