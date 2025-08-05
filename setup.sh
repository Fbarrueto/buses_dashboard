#!/bin/bash

echo " Creando entorno virtual '.venv'..."
python3 -m venv .venv

echo " Entorno creado. Activando entorno..."
source .venv/bin/activate

echo "Instalando dependencias desde requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo " ¡Entorno listo!"
echo ""
echo "👉 Para activar el entorno manualmente más tarde, ejecuta:"
echo "   source .venv/bin/activate"
echo ""
echo "👉  📊. Para correr el dashboard ejecuta:"
echo "   🔭 📊  streamlit run app/dashboard.py"
