#!/bin/bash

echo "[*] Instalando MXtrack..."

if command -v python3 &>/dev/null; then
    echo "[✓] Python3 encontrado"
else
    echo "[✗] Instala Python3 primero"
    exit 1
fi

pip3 install -r requirements.txt

chmod +x MXtrack.py

echo "[✓] Instalación completa"
echo "[*] Ejecuta: python3 MXtrack.py"
