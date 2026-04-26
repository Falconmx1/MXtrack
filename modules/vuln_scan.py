#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading
import requests
from colorama import Fore, Style, init

init(autoreset=True)

def scan_port(ip, port, timeout=2):
    """Escanea un puerto específico"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        
        if result == 0:
            return True
        return False
    except:
        return False

def get_service_name(port):
    """Obtiene nombre del servicio por puerto"""
    common_ports = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
        53: "DNS", 80: "HTTP", 110: "POP3", 111: "RPC",
        135: "RPC", 139: "NetBIOS", 143: "IMAP", 443: "HTTPS",
        445: "SMB", 993: "IMAPS", 995: "POP3S", 1433: "MSSQL",
        3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 5900: "VNC",
        6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt", 27017: "MongoDB"
    }
    return common_ports.get(port, "Unknown")

def scan_ports_range(ip, start_port=1, end_port=1024, threads=50):
    """Escanea rango de puertos con multithreading"""
    print(f"\n{Fore.GREEN}[+] Escaneando {ip} desde puerto {start_port} hasta {end_port}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Usando {threads} hilos...{Style.RESET_ALL}\n")
    
    open_ports = []
    
    def scan_worker(port):
        if scan_port(ip, port):
            service = get_service_name(port)
            print(f"{Fore.GREEN}[+] PUERTO {port} ABIERTO ({service}){Style.RESET_ALL}")
            open_ports.append((port, service))
    
    # Crear hilos
    thread_list = []
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_worker, args=(port,))
        thread_list.append(t)
        t.start()
        
        # Controlar número de hilos
        if len(thread_list) >= threads:
            for t in thread_list:
                t.join()
            thread_list = []
    
    # Esperar hilos restantes
    for t in thread_list:
        t.join()
    
    return open_ports

def check_vulnerabilities(ip, open_ports):
    """Busca vulnerabilidades comunes en puertos abiertos"""
    print(f"\n{Fore.YELLOW}[*] Analizando vulnerabilidades...{Style.RESET_ALL}")
    
    vulns_found = []
    
    for port, service in open_ports:
        if port == 21:  # FTP
            vulns_found.append(f"FTP (21) - Posible anónimo, CVE-2015-2857")
        elif port == 22:  # SSH
            vulns_found.append(f"SSH (22) - Versión débil, fuerza bruta posible")
        elif port == 80:  # HTTP
            vulns_found.append(f"HTTP (80) - Revisar si es vulnerable a inyección SQL, XSS")
        elif port == 445:  # SMB
            vulns_found.append(f"SMB (445) - CVE-2017-0144 (EternalBlue), CVE-2020-0796")
        elif port == 3306:  # MySQL
            vulns_found.append(f"MySQL (3306) - Credenciales por defecto root:root")
        elif port == 3389:  # RDP
            vulns_found.append(f"RDP (3389) - CVE-2019-0708 (BlueKeep), fuerza bruta")
        elif port == 5900:  # VNC
            vulns_found.append(f"VNC (5900) - Autenticación débil o sin contraseña")
    
    if vulns_found:
        print(f"\n{Fore.RED}⚠️ VULNERABILIDADES DETECTADAS:{Style.RESET_ALL}")
        for vuln in vulns_found:
            print(f"   - {vuln}")
    else:
        print(f"{Fore.GREEN}[+] No se encontraron vulnerabilidades conocidas en puertos comunes{Style.RESET_ALL}")
    
    return vulns_found

def web_vulnerability_scan(url):
    """Escanea vulnerabilidades web básicas"""
    print(f"\n{Fore.YELLOW}[*] Escaneando web: {url}{Style.RESET_ALL}")
    
    # Verificar si existe robots.txt
    try:
        robots = requests.get(f"{url}/robots.txt", timeout=5)
        if robots.status_code == 200:
            print(f"{Fore.CYAN}[+] robots.txt encontrado:{Style.RESET_ALL}")
            print(robots.text[:300])
    except:
        pass
    
    # Verificar servidor
    try:
        headers = requests.get(url, timeout=5).headers
        server = headers.get('Server', 'No especificado')
        print(f"{Fore.CYAN}[+] Servidor: {server}{Style.RESET_ALL}")
        print(f"   Headers: X-Powered-By: {headers.get('X-Powered-By', 'N/A')}")
    except:
        pass
    
    print(f"\n{Fore.YELLOW}[!] Escaneo básico - Para análisis profundo:{Style.RESET_ALL}")
    print("   - Nikto: nikto -h " + url)
    print("   - Nmap: nmap -sV --script vuln " + url)
    print("   - WhatWeb: whatweb " + url)

def nmap_integration(ip):
    """Integración opcional con nmap (si está instalado)"""
    import subprocess
    
    print(f"\n{Fore.GREEN}[+] Ejecutando nmap en {ip}...{Style.RESET_ALL}")
    try:
        result = subprocess.run(['nmap', '-sV', '--script', 'vuln', ip], 
                               capture_output=True, text=True, timeout=60)
        print(result.stdout)
    except FileNotFoundError:
        print(f"{Fore.RED}❌ Nmap no instalado. Instálalo con: sudo apt install nmap{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")

def vulnerability_menu():
    """Menú principal de escaneo"""
    print(f"\n{Fore.MAGENTA}═══════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.GREEN}🔒 MÓDULO DE ESCANEO Y VULNERABILIDADES{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}═══════════════════════════════════════════{Style.RESET_ALL}")
    
    print("\n1️⃣  Escaneo de puertos (rápido)")
    print("2️⃣  Escaneo completo + vulnerabilidades")
    print("3️⃣  Escaneo web básico")
    print("4️⃣  Integración con nmap")
    print("5️⃣  Volver")
    
    opcion = input("\n👉 Opción: ")
    
    ip = None
    
    if opcion == '1':
        ip = input("🌐 IP o dominio: ")
        # Resolver dominio
        try:
            ip = socket.gethostbyname(ip)
            open_ports = scan_ports_range(ip, 1, 1024, 100)
        except:
            print(f"{Fore.RED}❌ No se pudo resolver{Style.RESET_ALL}")
    
    elif opcion == '2':
        ip = input("🌐 IP o dominio: ")
        try:
            ip = socket.gethostbyname(ip)
            open_ports = scan_ports_range(ip, 1, 10000, 200)
            if open_ports:
                check_vulnerabilities(ip, open_ports)
        except:
            print(f"{Fore.RED}❌ Error{Style.RESET_ALL}")
    
    elif opcion == '3':
        url = input("🌐 URL (ej: https://example.com): ")
        web_vulnerability_scan(url)
    
    elif opcion == '4':
        ip = input("🌐 IP para nmap: ")
        nmap_integration(ip)

if __name__ == "__main__":
    vulnerability_menu()
