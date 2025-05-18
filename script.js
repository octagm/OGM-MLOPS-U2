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
    document.getElementById("resultado").textContent = Diagnóstico: ${data.resultado};
  } catch (error) {
    console.error("Error:", error);
    document.getElementById("resultado").textContent = "Error al conectar con el servidor.";
  }
});

// Función para generar el reporte
document.getElementById("generarReporte").addEventListener("click", async function() {
  try {
    const response = await fetch("http://localhost:5000/reporte", {
      method: "GET",
      headers: { "Content-Type": "application/json" }
    });

    const reporte = await response.json();
    mostrarReporte(reporte);
  } catch (error) {
    console.error("Error al generar reporte:", error);
    alert("Error al generar el reporte. Verifique la conexión con el servidor.");
  }
});

// Función para mostrar el reporte en la interfaz
function mostrarReporte(reporte) {
  // Mostrar el contenedor del reporte
  document.getElementById("reporteContainer").style.display = "block";

  // Mostrar categorías
  const categoriasContainer = document.getElementById("categorias");
  categoriasContainer.innerHTML = "";

  for (const [categoria, cantidad] of Object.entries(reporte.predicciones_por_categoria)) {
    const categoriaElement = document.createElement("span");
    categoriaElement.className = "category-stat";
    categoriaElement.textContent = ${categoria}: ${cantidad};
    categoriasContainer.appendChild(categoriaElement);
  }

  // Mostrar últimas predicciones
  const prediccionesContainer = document.getElementById("ultimasPredicciones");
  prediccionesContainer.innerHTML = "";

  if (reporte.ultimas_predicciones.length === 0) {
    prediccionesContainer.textContent = "No hay predicciones registradas.";
  } else {
    reporte.ultimas_predicciones.forEach(prediccion => {
      const prediccionElement = document.createElement("div");
      prediccionElement.className = "reporte-item";

      prediccionElement.innerHTML = `
        <span class="prediccion-fecha">[${prediccion.fecha}]</span>
        <span class="prediccion-resultado">${prediccion.resultado}</span>
        <div>Temperatura: ${prediccion.datos.temperatura}°C | 
             Ritmo Cardíaco: ${prediccion.datos.ritmo_cardiaco} ppm | 
             Saturación: ${prediccion.datos.saturacion_oxigeno}%</div>
      `;

      prediccionesContainer.appendChild(prediccionElement);
    });
  }

  // Mostrar fecha de última predicción
  document.getElementById("ultimaFecha").textContent = reporte.ultima_prediccion_fecha;
}