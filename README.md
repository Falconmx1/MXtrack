# 🔥 MXtrack - Supera a GhostTrack

[![Version](https://img.shields.io/badge/version-2.0-red)](https://github.com/Falconmx1/MXtrack)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![OS](https://img.shields.io/badge/OS-Linux%20%7C%20Windows%20%7C%20Termux-lightgrey)]()

> **Herramienta OSINT para rastreo de números móviles y geolocalización.**

## ⚡ Características
- 📍 Geolocalización aproximada por número
- 🕵️ OSINT en redes sociales
- 📞 Spoofing de caller ID (experimental)
- 🌍 Soporte multi-SIM (MX, US, EU)
- 🛡️ Modo anónimo con proxys

## 🚀 Instalación

### Linux / Termux
```bash
git clone https://github.com/Falconmx1/MXtrack
cd MXtrack
bash setup.sh
python3 MXtrack.py

git clone https://github.com/Falconmx1/MXtrack
cd MXtrack
pip install -r requirements.txt
python MXtrack.py

# Termux específico
pkg update && pkg upgrade
pkg install python git nmap
git clone https://github.com/Falconmx1/MXtrack
cd MXtrack
pip install -r requirements.txt
python MXtrack.py


## 🚀 Instrucciones finales
# 1. Clonar o crear el proyecto
mkdir MXtrack && cd MXtrack

# 2. Crear estructura de carpetas
mkdir modules logs

# 3. Crear todos los archivos (copia los códigos de arriba)
# - MXtrack.py (el completo)
# - modules/utils.py
# - modules/tracker.py (del mensaje anterior)
# - modules/osint.py (del mensaje anterior)
# - modules/geoip.py (del mensaje anterior)
# - modules/sms_spoof.py (del mensaje anterior)
# - modules/vuln_scan.py (del mensaje anterior)
# - requirements.txt
# - proxys.txt (se crea automático)

# 4. Instalar y ejecutar
pip install -r requirements.txt
python3 MXtrack.py

🚀 Probarlo en tu máquina

# Escaneo SYN (requiere sudo)
sudo python mxmap.py -t 192.168.1.1 --syn-scan -p 22,80,443 --stealth

# Detectar OS
python mxmap.py -t google.com --detect-os

# Fuzzing web
python mxmap.py --web-fuzz https://ejemplo.com

# Shodan
python mxmap.py --shodan 8.8.8.8 --shodan-key TU_API_KEY
