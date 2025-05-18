document.getElementById("healthForm").addEventListener("submit", async function(event) {
    event.preventDefault();
  
    const temperatura = parseFloat(document.getElementById("temperatura").value);
    const ritmo = parseInt(document.getElementById("ritmo").value);
    const saturacion = parseInt(document.getElementById("saturacion").value);
  
    try {
      const response = await fetch("http://localhost:5000/diagnostico", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ temperatura, ritmo_cardiaco: ritmo, saturacion_oxigeno: saturacion })
      });
  
      const data = await response.json();
      document.getElementById("resultado").textContent = `Diagnóstico: ${data.resultado}`;
    } catch (error) {
      console.error("Error:", error);
      document.getElementById("resultado").textContent = "Error al conectar con el servidor.";
    }
  });
  