

```markdown
# 🚌 Análisis y Visualización de Viajes de Buses

Este proyecto analiza y visualiza los viajes realizados por buses entre terminales, utilizando **Python** y **Streamlit**. Se procesan datos brutos de telemetría para identificar viajes, calcular métricas operativas y detectar anomalías.

---

## 📂 Estructura del Proyecto

```

bus-viajes-proyecto/
├── app/
│   └── dashboard.py           \# App principal de Streamlit
├── data/                      \# Archivos de datos originales
│   ├── bus\_data.xlsx
│   ├── coordenadas\_1.xlsx
│   └── origen-destino.xlsx
├── notebooks/                 \# Archivos de análisis y experimentación
│   └── analisis.ipynb
├── output/                    \# Datasets procesados y resultados
│   └── trip\_summary.csv       \# Dataset final de viajes
├── src/                       \# Código fuente de las herramientas
│   ├── detect\_viajes.py       \# Lógica principal de detección de viajes
│   └── utils.py               \# Funciones auxiliares
├── requirements.txt           \# Dependencias del proyecto
└── README.md                  \# Este archivo

````

---

🛠️ Requisitos

Asegúrate de tener instalado **Python 3.9** o una versión superior.

---
 ▶️ Cómo ejecutar el proyecto

Sigue estos pasos para configurar y ejecutar el dashboard en tu máquina local.

### 1. Clonar el repositorio

```bash
git clone [https://github.com/tu_usuario/bus-viajes-proyecto.git](https://github.com/tu_usuario/bus-viajes-proyecto.git)
cd bus-viajes-proyecto
````

### 2. Crear y activar el entorno virtual

Es una buena práctica usar entornos virtuales para aislar las dependencias del proyecto.

```bash
# Crea el entorno virtual
python -m venv .venv

# Activa el entorno virtual (el comando depende de tu SO)
# En macOS/Linux:
source .venv/bin/activate
# En Windows (CMD):
.venv\Scripts\activate
# En Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

### 3\. Instalar las dependencias

Con el entorno virtual activado, instala todas las librerías necesarias.

```bash
pip install -r requirements.txt
```

### 4\. Ejecutar el dashboard

Ahora puedes iniciar la aplicación de Streamlit.

```bash
streamlit run app/dashboard.py
```

Tu dashboard se abrirá automáticamente en tu navegador web.

```
```
