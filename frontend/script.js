document.getElementById("uploadForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById("fileInput");
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    try {
        const response = await fetch("http://127.0.0.1:8000/upload/", {
            method: "POST",
            body: formData,
        });

        const result = await response.json();
        console.log(result);  // Aquí puedes manejar el resultado en el frontend

        // Mostrar resultado en el frontend
        document.getElementById("percentage").innerText = result.damage_percentage;
        document.getElementById("result").style.display = "block";
        
    } catch (error) {
          alert("Hubo un error al procesar la imagen e.");
        console.error(error);
        }  
});
