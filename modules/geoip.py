#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import socket
import json
from colorama import Fore, Style, init

init(autoreset=True)

def get_ip_from_number(numero):
    """
    Intenta obtener IP pública asociada al número (modo demostración)
    En realidad necesitarías acceso a logs de operador o ingeniería social
    """
    print(f"{Fore.YELLOW}[!] No es posible obtener IP directa de un número móvil{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[*] Métodos alternativos:{Style.RESET_ALL}")
    print("  1. Enviar enlace tracker vía SMS (Social Engineering)")
    print("  2. Si el objetivo usa datos móviles y visitó tu sitio/web")
    print("  3. Datos de operador (solo con orden judicial)\n")
    
    return None

def geoip_by_address(ip_address):
    """Geolocaliza una dirección IP usando múltiples APIs"""
    
    print(f"{Fore.GREEN}[+] Geolocalizando IP: {ip_address}{Style.RESET_ALL}")
    
    # API 1: ip-api.com (gratis, 45 requests/min)
    try:
        url = f"http://ip-api.com/json/{ip_address}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data['status'] == 'success':
            print(f"\n{Fore.CYAN}📍 IP-API.COM - Datos:{Style.RESET_ALL}")
            print(f"   País: {data['country']} ({data['countryCode']})")
            print(f"   Región: {data['regionName']}")
            print(f"   Ciudad: {data['city']}")
            print(f"   Lat/Lon: {data['lat']}, {data['lon']}")
            print(f"   ISP: {data['isp']}")
            print(f"   Organización: {data['org']}")
            print(f"   AS: {data['as']}")
            
            # Generar Google Maps link
            maps_link = f"https://www.google.com/maps?q={data['lat']},{data['lon']}"
            print(f"   {Fore.GREEN}🗺️ Maps: {maps_link}{Style.RESET_ALL}")
            
            return data
    except Exception as e:
        print(f"{Fore.RED}❌ Error con ip-api: {e}{Style.RESET_ALL}")
    
    # API 2: ipinfo.io (requiere token gratis)
    try:
        token = "TU_TOKEN_GRATIS_IPINFO"  # Regístrate en ipinfo.io
        url = f"https://ipinfo.io/{ip_address}/json?token={token}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if 'city' in data:
            print(f"\n{Fore.CYAN}📍 IPINFO.IO - Datos adicionales:{Style.RESET_ALL}")
            print(f"   Ciudad: {data.get('city', 'N/A')}")
            print(f"   Región: {data.get('region', 'N/A')}")
            print(f"   País: {data.get('country', 'N/A')}")
            print(f"   Locación: {data.get('loc', 'N/A')}")
            print(f"   Org: {data.get('org', 'N/A')}")
            print(f"   Postal: {data.get('postal', 'N/A')}")
            print(f"   Timezone: {data.get('timezone', 'N/A')}")
    except Exception as e:
        print(f"{Fore.RED}❌ Error con ipinfo: {e}{Style.RESET_ALL}")
    
    return None

def scan_network_range(ip_range):
    """Escanea rango de red para encontrar dispositivos"""
    print(f"{Fore.YELLOW}[*] Escaneando red: {ip_range}{Style.RESET_ALL}")
    # Integración con nmap o scapy
    print(f"{Fore.RED}[!] Módulo en desarrollo - Usa nmap manualmente{Style.RESET_ALL}")

def track_by_ip_menu():
    """Menú principal de geolocalización IP"""
    print(f"\n{Fore.MAGENTA}═══════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.GREEN}🌍 MÓDULO DE GEOLOCALIZACIÓN POR IP{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}═══════════════════════════════════════════{Style.RESET_ALL}")
    
    print("\n1️⃣  Geolocalizar IP específica")
    print("2️⃣  Explicación: IP desde número móvil")
    print("3️⃣  Generar enlace tracker (ngrok + log)")
    print("4️⃣  Volver")
    
    opcion = input("\n👉 Opción: ")
    
    if opcion == '1':
        ip = input("📡 Ingresa la IP: ")
        geoip_by_address(ip)
    elif opcion == '2':
        print(f"\n{Fore.CYAN}📱 ¿Cómo obtener IP de un número móvil?{Style.RESET_ALL}")
        print("""
        🔹 Los operadores (Telcel, Movistar, AT&T) asignan IPs dinámicas.
        🔹 Para obtenerla necesitas:
           - Enviar un enlace a un servidor propio (tracker.php)
           - Usar servicios como grabify.link o IP logger
           - La persona debe hacer clic mientras usa datos móviles
        
        ⚠️ Un número NO revela IP directamente sin interacción.
        """)
    elif opcion == '3':
        print(f"\n{Fore.GREEN}[+] Generando enlace tracker...{Style.RESET_ALL}")
        print("1. Crea un webhook en https://webhook.site")
        print("2. Usa https://grabify.link para acortar")
        print("3. Envía el enlace: 'Mira tu foto aquí' o similar")
        print("4. Cuando abran, verás su IP en logs")
        print(f"\n{Fore.RED}⚠️ Esto es ingeniería social - Usa con responsabilidad{Style.RESET_ALL}")

if __name__ == "__main__":
    track_by_ip_menu()
