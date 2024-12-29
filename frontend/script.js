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

        // Mostrar mensaje de éxito
        alert(result.message);

        document.getElementById("analyzeButton").disabled = false;

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
