// Validación y envío del formulario
document.getElementById("healthForm").addEventListener("submit", async function(event) {
  event.preventDefault();

  const temperaturaInput = document.getElementById("temperatura");
  const ritmoInput = document.getElementById("ritmo");
  const saturacionInput = document.getElementById("saturacion");

  const temperatura = parseFloat(temperaturaInput.value);
  const ritmo = parseInt(ritmoInput.value);
  const saturacion = parseInt(saturacionInput.value);

  // Limpiar errores anteriores
  clearErrors();

  let hayError = false;

  if (isNaN(temperatura) || temperatura < 30 || temperatura > 45) {
    showError("temperatura", "Ingrese un valor entre 30°C y 45°C");
    hayError = true;
  }

  if (isNaN(ritmo) || ritmo < 30 || ritmo > 200) {
    showError("ritmo", "Ingrese un valor entre 30 y 200 ppm");
    hayError = true;
  }

  if (isNaN(saturacion) || saturacion < 50 || saturacion > 100) {
    showError("saturacion", "Ingrese un valor entre 50% y 100%");
    hayError = true;
  }

  if (hayError) return;

  try {
    const response = await fetch("http://localhost:5000/diagnostico", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        temperatura,
        ritmo_cardiaco: ritmo,
        saturacion_oxigeno: saturacion
      })
    });

    const data = await response.json();
    document.getElementById("resultado").textContent = `Diagnóstico: ${data.resultado}`;
  } catch (error) {
    console.error("Error:", error);
    document.getElementById("resultado").textContent = "Error al conectar con el servidor.";
  }
});

// Mostrar mensaje de error en campo
function showError(campo, mensaje) {
  const input = document.getElementById(campo);
  const errorSpan = document.getElementById("error-" + campo);
  input.classList.add("input-error");
  errorSpan.textContent = mensaje;
  input.focus(); // Foco en el campo inválido
}

// Limpiar todos los errores
function clearErrors() {
  ["temperatura", "ritmo", "saturacion"].forEach(campo => {
    document.getElementById(campo).classList.remove("input-error");
    document.getElementById("error-" + campo).textContent = "";
  });
}

// Función para generar el reporte
document.getElementById("generarReporte").addEventListener("click", async function() {
  try {
    const response = await fetch("http://localhost:5000/reporte", {
      method: "GET",
      headers: { "Content-Type": "application/json" }
    });

    const reporte = await response.json();
    mostrarReporte(reporte);

    // Mostrar el contenedor de reporte y el botón de cerrar
    document.getElementById("reporteContainer").style.display = "block";
    document.getElementById("cerrarReporte").style.display = "inline-block";

    // Ocultar el botón de generar reporte mientras el reporte está visible
    document.getElementById("generarReporte").style.display = "none";

  } catch (error) {
    console.error("Error al generar reporte:", error);
    alert("Error al generar el reporte. Verifique la conexión con el servidor.");
  }
});

// Función para mostrar el reporte en la interfaz
function mostrarReporte(reporte) {
  const categoriasContainer = document.getElementById("categorias");
  categoriasContainer.innerHTML = "";

  for (const [categoria, cantidad] of Object.entries(reporte.predicciones_por_categoria)) {
    const categoriaElement = document.createElement("span");
    categoriaElement.className = "category-stat";
    categoriaElement.textContent = `${categoria}: ${cantidad}`;
    categoriasContainer.appendChild(categoriaElement);
  }

  const prediccionesContainer = document.getElementById("ultimasPredicciones");
  prediccionesContainer.innerHTML = "";

  if (!reporte.ultimas_predicciones || reporte.ultimas_predicciones.length === 0) {
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

  document.getElementById("ultimaFecha").textContent = reporte.ultima_prediccion_fecha || "N/A";
}

// Evento para cerrar el reporte
document.getElementById("cerrarReporte").addEventListener("click", function() {
  document.getElementById("reporteContainer").style.display = "none";
  this.style.display = "none"; // Ocultar botón cerrar
  document.getElementById("generarReporte").style.display = "inline-block"; // Mostrar botón generar reporte
});