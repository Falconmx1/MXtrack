#!/usr/bin/env python3
import requests
import json

class ShodanLookup:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.shodan.io"

    def search_host(self, ip):
        """Obtiene información de Shodan para una IP"""
        if not self.api_key:
            print("  [!] Shodan API key no configurada")
            return None
            
        try:
            url = f"{self.base_url}/shodan/host/{ip}?key={self.api_key}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "ip": ip,
                    "os": data.get("os", "Desconocido"),
                    "ports": data.get("ports", []),
                    "vulns": data.get("vulns", {}),
                    "hostnames": data.get("hostnames", []),
                    "org": data.get("org", "Desconocida")
                }
            else:
                print(f"  [!] Error Shodan: {response.status_code}")
                return None
        except Exception as e:
            print(f"  [!] Error conectando a Shodan: {e}")
            return None

    def search_censys(self, ip):
        """Censys search (requiere API keys de Censys)"""
        # Versión simplificada - la completa requiere censys python library
        print("  [*] Censys requiere configuración adicional")
        return None

    def run(self, ip):
        print(f"\n[🔍] Consultando Shodan para {ip}")
        result = self.search_host(ip)
        if result:
            print(f"  [+] Organización: {result['org']}")
            print(f"  [+] OS detectado: {result['os']}")
            print(f"  [+] Puertos abiertos: {', '.join(map(str, result['ports'][:20]))}")
            if result['vulns']:
                print(f"  [+] CVEs encontrados: {list(result['vulns'].keys())}")
        return result
