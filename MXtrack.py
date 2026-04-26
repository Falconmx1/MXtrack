#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MXtrack v3.0 - Herramienta OSINT de rastreo telefónico y geolocalización
Más potente que GhostTrack | By: @tu_usuario
"""

import os
import sys
import platform
import subprocess
import json
import csv
import random
import threading
from datetime import datetime
from colorama import Fore, Style, init

# Importar módulos propios
from modules.tracker import track_number
from modules.osint import osint_search
from modules.geoip import track_by_ip_menu
from modules.sms_spoof import sms_campaign_menu
from modules.vuln_scan import vulnerability_menu
from modules.utils import (
    setup_logger, 
    save_to_csv, 
    get_random_proxy, 
    test_proxy,
    rotate_user_agent,
    anonymous_request
)

init(autoreset=True)

# ==================== CONFIGURACIÓN ====================
VERSION = "3.0"
AUTHOR = "@tu_usuario"
LOG_FILE = "logs/escaneos.csv"

# ==================== FUNCIONES PRINCIPALES ====================

def clear_screen():
    """Limpia la pantalla según el SO"""
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def show_banner():
    """Muestra el banner chingón"""
    banner = f"""
    {Fore.RED}╔═══════════════════════════════════════════════════════════════════════╗
    ║  {Fore.YELLOW}███╗   ███╗ ██╗  ██╗████████╗██████╗  █████╗  ██████╗██╗  {Fore.RED}║
    ║  {Fore.YELLOW}████╗ ████║ ╚██╗██╔╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║  {Fore.RED}║
    ║  {Fore.YELLOW}██╔████╔██║  ╚███╔╝    ██║   ██████╔╝███████║██║     ██║  {Fore.RED}║
    ║  {Fore.YELLOW}██║╚██╔╝██║  ██╔██╗    ██║   ██╔══██╗██╔══██║██║     ██║  {Fore.RED}║
    ║  {Fore.YELLOW}██║ ╚═╝ ██║ ██╔╝ ██╗   ██║   ██║  ██║██║  ██║╚██████╗██████╗{Fore.RED}║
    ║  {Fore.YELLOW}╚═╝     ╚═╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═════╝{Fore.RED}║
    ╠═══════════════════════════════════════════════════════════════════════╣
    ║  {Fore.CYAN}🔥 MXtrack v{VERSION} | OSINT + Tracking + Spoof + Proxy Rotator{Fore.RED}          ║
    ║  {Fore.GREEN}🧠 Más potente que GhostTrack | By: {AUTHOR}{Fore.RED}                          ║
    ║  {Fore.MAGENTA}🛡️ Modo anónimo | Proxy rotatorio | CSV logging{Fore.RED}                    ║
    ╚═══════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(banner)

def proxy_config_menu():
    """Menú de configuración de proxys rotatorios"""
    print(f"\n{Fore.MAGENTA}═══════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.GREEN}🛡️ CONFIGURACIÓN DE PROXY ROTATORIO{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}═══════════════════════════════════════════{Style.RESET_ALL}")
    
    print("\n1️⃣  Usar proxy aleatorio (automático)")
    print("2️⃣  Listar proxys disponibles")
    print("3️⃣  Agregar proxy manualmente")
    print("4️⃣  Testear conectividad de proxy")
    print("5️⃣  Modo anónimo completo (proxy + User-Agent rotatorio)")
    print("6️⃣  Volver")
    
    opcion = input("\n👉 Opción: ")
    
    if opcion == '1':
        proxy = get_random_proxy()
        if proxy:
            print(f"{Fore.GREEN}[+] Proxy seleccionado: {proxy}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] No hay proxys configurados{Style.RESET_ALL}")
    
    elif opcion == '2':
        try:
            with open('proxys.txt', 'r') as f:
                proxys = f.readlines()
            print(f"\n{Fore.CYAN}📡 Proxys disponibles ({len(proxys)}):{Style.RESET_ALL}")
            for p in proxys[:10]:  # Mostrar primeros 10
                print(f"   - {p.strip()}")
            if len(proxys) > 10:
                print(f"   ... y {len(proxys)-10} más")
        except FileNotFoundError:
            print(f"{Fore.RED}[!] No existe archivo proxys.txt{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[*] Crea uno con formato: ip:puerto o user:pass@ip:puerto{Style.RESET_ALL}")
    
    elif opcion == '3':
        new_proxy = input("📡 Ingresa proxy (ip:puerto o user:pass@ip:puerto): ")
        with open('proxys.txt', 'a') as f:
            f.write(f"{new_proxy}\n")
        print(f"{Fore.GREEN}[+] Proxy agregado!{Style.RESET_ALL}")
    
    elif opcion == '4':
        proxy = input("📡 Proxy a testear: ")
        if test_proxy(proxy):
            print(f"{Fore.GREEN}[+] Proxy funciona correctamente{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] Proxy no responde{Style.RESET_ALL}")
    
    elif opcion == '5':
        print(f"{Fore.GREEN}[+] Modo anónimo ACTIVADO{Style.RESET_ALL}")
        print(f"{Fore.CYAN}   - Proxy rotatorio por cada request{Style.RESET_ALL}")
        print(f"{Fore.CYAN}   - User-Agent rotatorio{Style.RESET_ALL}")
        print(f"{Fore.CYAN}   - Headers aleatorios{Style.RESET_ALL}")
        input("\nPresiona Enter para continuar...")

def view_logs_menu():
    """Menú para ver registros de escaneos"""
    print(f"\n{Fore.MAGENTA}═══════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.GREEN}📊 REGISTRO DE ESCANEOS (CSV){Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}═══════════════════════════════════════════{Style.RESET_ALL}")
    
    print("\n1️⃣  Ver últimos 10 escaneos")
    print("2️⃣  Exportar todo a JSON")
    print("3️⃣  Limpiar logs")
    print("4️⃣  Volver")
    
    opcion = input("\n👉 Opción: ")
    
    if opcion == '1':
        try:
            with open(LOG_FILE, 'r') as f:
                reader = csv.reader(f)
                rows = list(reader)
                print(f"\n{Fore.CYAN}📋 Últimos {min(10, len(rows)-1)} escaneos:{Style.RESET_ALL}")
                for i, row in enumerate(rows[-11:]):  # Mostrar últimos 10 + header
                    if i == 0:
                        print(f"\n{Fore.YELLOW}{' | '.join(row)}{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}{'-'*60}{Style.RESET_ALL}")
                    else:
                        print(f"{' | '.join(row)}")
        except FileNotFoundError:
            print(f"{Fore.RED}[!] No hay logs aún{Style.RESET_ALL}")
    
    elif opcion == '2':
        try:
            import json
            with open(LOG_FILE, 'r') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            with open('logs/export.json', 'w') as f:
                json.dump(data, f, indent=2)
            print(f"{Fore.GREEN}[+] Exportado a logs/export.json{Style.RESET_ALL}")
        except:
            print(f"{Fore.RED}[!] Error al exportar{Style.RESET_ALL}")
    
    elif opcion == '3':
        confirm = input("⚠️ ¿Seguro que quieres limpiar todos los logs? (s/n): ")
        if confirm.lower() == 's':
            with open(LOG_FILE, 'w') as f:
                f.write("timestamp,tipo,objetivo,resultado,ip_origen\n")
            print(f"{Fore.GREEN}[+] Logs limpiados{Style.RESET_ALL}")

def install_dependencies():
    """Instala todas las dependencias necesarias"""
    print(f"{Fore.YELLOW}[*] Instalando dependencias...{Style.RESET_ALL}")
    
    dependencies = [
        "requests", "beautifulsoup4", "phonenumbers", 
        "colorama", "pyfiglet", "twilio"
    ]
    
    for dep in dependencies:
        print(f"{Fore.CYAN}[*] Instalando {dep}...{Style.RESET_ALL}")
        subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                      capture_output=True)
    
    print(f"{Fore.GREEN}[✓] Dependencias instaladas{Style.RESET_ALL}")

def info_module():
    """Muestra información del módulo y capacidades"""
    print(f"\n{Fore.MAGENTA}═══════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.GREEN}📚 ACERCA DE MXtrack{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}═══════════════════════════════════════════{Style.RESET_ALL}")
    
    print(f"""
{Fore.CYAN}🎯 OBJETIVO:{Style.RESET_ALL}
   Herramienta OSINT para rastreo telefónico y geolocalización

{Fore.CYAN}🔧 MÓDULOS DISPONIBLES:{Style.RESET_ALL}
   1. Rastreo de números - Carrier, ubicación aproximada
   2. OSINT en redes - Facebook, Instagram, Twitter, Telegram
   3. Geolocalización IP - Múltiples APIs + Google Maps
   4. SMS Spoofing - Twilio + métodos alternativos
   5. Escaneo puertos - Multi-thread + vulnerabilidades (CVE)
   6. Proxy rotatorio - Anonimato completo
   7. CSV Logging - Registro automático de escaneos

{Fore.CYAN}⚠️ DISCLAIMER:{Style.RESET_ALL}
   {Fore.RED}Esta herramienta es SOLO para fines educativos y
   pruebas de seguridad autorizadas. El mal uso puede
   ser ilegal. El desarrollador no se hace responsable.{Style.RESET_ALL}

{Fore.CYAN}📡 VERSIONES SOPORTADAS:{Style.RESET_ALL}
   - Linux (Ubuntu/Debian/Kali/Parrot)
   - Windows 10/11 (con Python 3.8+)
   - Termux (Android)

{Fore.CYAN}📂 LOGS:{Style.RESET_ALL}
   Todos los escaneos se guardan en: logs/escaneos.csv
    """)
    
    input("\nPresiona Enter para continuar...")

def main_menu():
    """Menú principal de la herramienta"""
    while True:
        clear_screen()
        show_banner()
        
        print(f"\n{Fore.CYAN}┌─────────────────────────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Fore.YELLOW}            MENÚ PRINCIPAL                 {Fore.CYAN}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}├─────────────────────────────────────────┤{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Fore.GREEN} 1  {Style.RESET_ALL}📍 Rastrear número móvil            {Fore.CYAN}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Fore.GREEN} 2  {Style.RESET_ALL}🕵️  OSINT en número/redes           {Fore.CYAN}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Fore.GREEN} 3  {Style.RESET_ALL}🌍 Geolocalización por IP            {Fore.CYAN}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Fore.GREEN} 4  {Style.RESET_ALL}📱 SMS Spoofing (Twilio)            {Fore.CYAN}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Fore.GREEN} 5  {Style.RESET_ALL}🔒 Escaneo puertos y vulnerabilidades{Fore.CYAN}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Fore.GREEN} 6  {Style.RESET_ALL}🛡️  Modo anónimo + Proxy rotatorio   {Fore.CYAN}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Fore.GREEN} 7  {Style.RESET_ALL}📊 Ver logs de escaneos              {Fore.CYAN}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Fore.GREEN} 8  {Style.RESET_ALL}🛠️  Instalar dependencias            {Fore.CYAN}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Fore.GREEN} 9  {Style.RESET_ALL}📚 Acerca de / Info                 {Fore.CYAN}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{Fore.GREEN} 0  {Style.RESET_ALL}🚪 Salir                            {Fore.CYAN}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}└─────────────────────────────────────────┘{Style.RESET_ALL}")
        
        opcion = input(f"\n{Fore.YELLEN}👉 Elige una opción: {Style.RESET_ALL}")
        
        if opcion == '1':
            numero = input(f"{Fore.CYAN}📱 Número a rastrear (+código país): {Style.RESET_ALL}")
            track_number(numero)
            save_to_csv(LOG_FILE, "tracking", numero, "completado", "N/A")
        
        elif opcion == '2':
            target = input(f"{Fore.CYAN}🎯 Número o usuario: {Style.RESET_ALL}")
            osint_search(target)
            save_to_csv(LOG_FILE, "osint", target, "búsqueda realizada", "N/A")
        
        elif opcion == '3':
            track_by_ip_menu()
        
        elif opcion == '4':
            sms_campaign_menu()
        
        elif opcion == '5':
            vulnerability_menu()
        
        elif opcion == '6':
            proxy_config_menu()
        
        elif opcion == '7':
            view_logs_menu()
        
        elif opcion == '8':
            install_dependencies()
        
        elif opcion == '9':
            info_module()
        
        elif opcion == '0':
            print(f"{Fore.GREEN}[+] Saliendo de MXtrack...{Style.RESET_ALL}")
            print(f"{Fore.RED}⚠️ Recuerda usar esta herramienta con responsabilidad{Style.RESET_ALL}")
            sys.exit(0)
        
        else:
            print(f"{Fore.RED}❌ Opción no válida{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Presiona Enter para continuar...{Style.RESET_ALL}")

# ==================== EJECUCIÓN PRINCIPAL ====================

if __name__ == "__main__":
    # Crear directorio de logs si no existe
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Crear archivo CSV si no existe
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            f.write("timestamp,tipo,objetivo,resultado,ip_origen\n")
    
    # Crear archivo de proxys si no existe
    if not os.path.exists('proxys.txt'):
        with open('proxys.txt', 'w') as f:
            # Agregar algunos proxys públicos de ejemplo
            f.write("# Agrega tus proxys aquí (uno por línea)\n")
            f.write("# Formato: ip:puerto o usuario:contraseña@ip:puerto\n")
            f.write("185.199.229.156:7497\n")
            f.write("138.68.60.8:3128\n")
            f.write("159.203.61.169:3128\n")
    
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Interrupción detectada. Saliendo...{Style.RESET_ALL}")
        sys.exit(0)#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import platform
from modules.tracker import track_number
from modules.osint import osint_search
from modules.spoof import spoof_call

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def show_banner():
    banner = '''
    ╔═══════════════════════════════════════════════════════╗
    ║  ███╗   ███╗ ██╗  ██╗████████╗██████╗  █████╗  ██████╗██╗  ║
    ║  ████╗ ████║ ╚██╗██╔╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║  ║
    ║  ██╔████╔██║  ╚███╔╝    ██║   ██████╔╝███████║██║     ██║  ║
    ║  ██║╚██╔╝██║  ██╔██╗    ██║   ██╔══██╗██╔══██║██║     ██║  ║
    ║  ██║ ╚═╝ ██║ ██╔╝ ██╗   ██║   ██║  ██║██║  ██║╚██████╗██████╗
    ║  ╚═╝     ╚═╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═════╝
    ╠═══════════════════════════════════════════════════════╣
    ║   🔥 MXtrack v2.0 | OSINT + Tracking + Spoof         ║
    ║   🧠 Más potente que GhostTrack | By: @Falconmx1     ║
    ╚═══════════════════════════════════════════════════════╝
    '''
    print(banner)

def main_menu():
    while True:
        show_banner()
        print("\n[1] 📍 Rastrear número móvil")
        print("[2] 🕵️  OSINT en número/redes")
        print("[3] 📞 Spoof caller ID (experimental)")
        print("[4] 🛠️  Instalar dependencias")
        print("[5] 🚪 Salir")
        
        opcion = input("\n👉 Elige una opción: ")
        
        if opcion == '1':
            numero = input("📱 Número a rastrear (+código país): ")
            track_number(numero)
        elif opcion == '2':
            target = input("🎯 Número o usuario: ")
            osint_search(target)
        elif opcion == '3':
            spoof_call()
        elif opcion == '4':
            os.system('pip install -r requirements.txt')
        elif opcion == '5':
            sys.exit(0)
        else:
            print("❌ Opción no válida")
        input("\nPresiona Enter para continuar...")
        clear_screen()

if __name__ == "__main__":
    clear_screen()
    main_menu()
