# 🩺 Proyecto  - Diagnóstico de Salud

Este proyecto esta enfocado en el desarrollo de una aplicación web simple que permite realizar un diagnóstico médico básico en función de tres parámetros fisiológicos: Temperatura Corporal, Ritmo cardíaco y Saturación de oxígeno en la sangre.

---

## 🧠 Lógica del Diagnóstico

La lógica utilizada clasifica el estado de salud en las siguientes categorías:

| Temperatura (°C) | Ritmo Cardíaco (ppm) | Saturación O₂ (%) | Resultado             |
|------------------|-----------------------|--------------------|------------------------|
| 36 - 37.4        | 60 - 100              | ≥ 95               | NO ENFERMO             |
| 37.5 - 38.4      | 101 - 120             | ≥ 92               | ENFERMO LEVE           |
| ≥ 38.5           | > 120                 | < 92               | ENFERMEDAD AGUDA       |
| 37 - 38          | 60 - 99               | < 90               | ENFERMEDAD CRÓNICA     |
| —                | —                     | —                  | Valores Fuera de Rango |

---

