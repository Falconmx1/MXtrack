#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de utilidades: CSV logging, proxys rotatorios, user-agents
"""

import csv
import random
import requests
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

# Lista de User-Agents comunes para rotar
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
]

def setup_logger():
    """Configura el logger básico"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def save_to_csv(log_file, tipo, objetivo, resultado, ip_origen="N/A"):
    """Guarda un escaneo en el archivo CSV"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        with open(log_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, tipo, objetivo, resultado, ip_origen])
        print(f"{Fore.GREEN}[✓] Escaneo registrado en {log_file}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error al guardar log: {e}{Style.RESET_ALL}")

def load_proxies():
    """Carga la lista de proxys desde archivo"""
    proxies = []
    try:
        with open('proxys.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    proxies.append(line)
    except FileNotFoundError:
        print(f"{Fore.YELLOW}[!] No se encontró proxys.txt{Style.RESET_ALL}")
    return proxies

def get_random_proxy():
    """Obtiene un proxy aleatorio de la lista"""
    proxies = load_proxies()
    if proxies:
        proxy = random.choice(proxies)
        return {
            'http': f'http://{proxy}',
            'https': f'https://{proxy}'
        }
    return None

def test_proxy(proxy_str, timeout=5):
    """Prueba si un proxy funciona"""
    try:
        proxy_dict = {
            'http': f'http://{proxy_str}',
            'https': f'https://{proxy_str}'
        }
        response = requests.get('http://httpbin.org/ip', 
                               proxies=proxy_dict, 
                               timeout=timeout)
        return response.status_code == 200
    except:
        return False

def rotate_user_agent():
    """Retorna un User-Agent aleatorio"""
    return random.choice(USER_AGENTS)

def anonymous_request(url, method='GET', data=None, headers=None):
    """
    Realiza una request anónima con proxy rotatorio y User-Agent aleatorio
    """
    proxy = get_random_proxy()
    user_agent = rotate_user_agent()
    
    default_headers = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    if headers:
        default_headers.update(headers)
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=default_headers, 
                                   proxies=proxy, timeout=10)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=default_headers, 
                                    data=data, proxies=proxy, timeout=10)
        else:
            return None
        
        return response
    except Exception as e:
        print(f"{Fore.RED}[!] Error en request anónima: {e}{Style.RESET_ALL}")
        return None

def get_external_ip():
    """Obtiene la IP pública actual"""
    try:
        response = requests.get('http://httpbin.org/ip', timeout=5)
        return response.json()['origin']
    except:
        return "Desconocida"
