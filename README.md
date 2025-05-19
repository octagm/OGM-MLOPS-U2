# 🩺 Diagnóstico de Salud con Flask y Docker

Este proyecto es una aplicación web simple que permite realizar un diagnóstico médico básico en función de tres parámetros fisiológicos: temperatura corporal, ritmo cardíaco y saturación de oxígeno en la sangre. Está compuesto por un backend en Flask, un frontend en HTML/CSS/JS, y es totalmente contenedorizado usando Docker.

---

## 📋 Características

- ✔️ Diagnóstico automático basado en signos vitales.
- 🌐 Comunicación entre frontend y backend mediante peticiones HTTP POST.
- 🔓 Habilitado para CORS.
- 🐳 Fácil despliegue con Docker.
- 💻 Interfaz limpia y responsiva.

---

## 🧠 Lógica del Diagnóstico

La lógica utilizada clasifica el estado de salud en las siguientes categorías:

| Temperatura (°C) | Ritmo Cardíaco (ppm) | Saturación O₂ (%) | Resultado             |
|------------------|-----------------------|--------------------|------------------------|
| 36 - 37.4        | 60 - 100              | ≥ 95               | NO ENFERMO             |
| 37.5 - 38.4      | 101 - 120             | 92 - 95            | ENFERMO LEVE           |
| 38.5 - 40        | > 120                 | 90 - 92            | ENFERMEDAD AGUDA       |
| > 40             | 60 - 99               | 85 - 90            | ENFERMEDAD CRÓNICA     |
| > 40             | < 60                  | < 85               | ENFERMEDAD TERMINAL    |
| —                | —                     | —                  | Valores Fuera de Rango |

---

## 🚀 Ejecución rápida con Docker

### 📦 Requisitos

- Tener instalado [Docker](https://www.docker.com/).

### ⚙️ Construir la imagen

```bash
docker build -t diagnostico-api .
````
![image](https://github.com/user-attachments/assets/5fa99005-7e75-4c4b-a767-c7d521bc88dc)


### ▶️ Ejecutar el contenedor

```bash
docker run -p 5000:5000 diagnostico-api
```

El backend estará disponible en `http://localhost:5000`.

---
![image](https://github.com/user-attachments/assets/2c8a5b72-78b1-4623-afa6-68629252c35c)


## 🖥 Interfaz Web

Abre el archivo `index.html` directamente en tu navegador.
<img width="957" alt="image" src="https://github.com/user-attachments/assets/d3a8e3ea-acad-472a-9e4b-1d6c8f0ee377" />

El usuario tiene dos (2) opciones:

1. Formulario de entrada:

* Temperatura en grados Celsius. Ingrese un valor entre 30°C y 45°C.
* Ritmo cardíaco en pulsaciones por minuto. Ingrese un valor entre 30 y 200 ppm.
* Saturación de oxígeno en porcentaje. Ingrese un valor entre 50% y 100%.

Al hacer clic en **Enviar**, el formulario se comunica con el backend y muestra el diagnóstico.

<img width="959" alt="image" src="https://github.com/user-attachments/assets/5e4c604b-f626-4c3c-9d2c-04e201d18f92" />



2. Generar Reporte: 

Dar Clic en el Boton **Generar Reporte**, y aparece en la pagina:
- El Total de Predicciones por categoría
- Las cinco (5) últimas predicciones en salud realizadas
- La fecha de la última predicción realizada

Una vez revisado el Reporte, se puede dar Clic en **Cerrar Reporte** para que se remueva el reporte en la Página.

<img width="959" alt="image" src="https://github.com/user-attachments/assets/25803f7a-6432-40d1-aee7-73d94ac6e3f0" />



---

## 📁 Estructura del Proyecto

```
.
├── app.py             # Servidor Flask con API REST
├── Dockerfile         # Imagen Docker
├── index.html         # Interfaz web
├── script.js          # Lógica del frontend
├── styles.css         # Estilos
└── README.md          # Documentación
```

---

## 🔒 CORS

El backend tiene habilitado CORS mediante `flask-cors` para permitir el acceso desde el frontend que se ejecuta en otro origen (por ejemplo, `127.0.0.1:5500`).

---

## 📦 Dependencias

Instaladas automáticamente en el contenedor Docker:

* `Flask`
* `flask-cors`

---

## 🛠 Recomendaciones para uso local (sin Docker)

Si deseas ejecutar este proyecto localmente sin Docker:

1. Crea un entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. Instala las dependencias:

   ```bash
   pip install flask flask-cors
   ```

3. Ejecuta la app:

   ```bash
   python app.py
   ```

---

## ✍️ Autor

Desarrollado por Octavio Guerra Munive.

---

## ⚠️ Aviso Legal

> ⚠️ Esta aplicación no reemplaza el diagnóstico médico profesional. Los resultados deben ser interpretados con precaución y, ante dudas, se recomienda consultar a un profesional de la salud.

