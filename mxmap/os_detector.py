#!/usr/bin/env python3
from scapy.all import IP, TCP, sr1, ICMP
import socket

class OSDetector:
    def __init__(self, target):
        self.target = target
        self.os_signatures = {
            (64, 8192): "Linux (kernel 2.4-2.6)",
            (64, 5840): "Linux (kernel 3.x-5.x)",
            (128, 8192): "Windows 10/11/Server",
            (128, 16384): "Windows 7/8",
            (64, 65535): "FreeBSD/OpenBSD",
            (255, 4128): "Cisco Router IOS",
            (64, 32768): "macOS/OS X"
        }

    def detect_by_ttl_and_window(self):
        """Analiza TTL y ventana TCP de un puerto abierto"""
        try:
            # Escanear puertos comunes para respuesta
            test_ports = [80, 443, 22, 25, 8080]
            for port in test_ports:
                pkt = IP(dst=self.target)/TCP(dport=port, flags="S")
                response = sr1(pkt, timeout=2, verbose=0)
                
                if response and response.haslayer(TCP):
                    ttl = response.ttl
                    window = response.getlayer(TCP).window
                    
                    # Normalizar TTL (valores comunes: 64, 128, 255)
                    if ttl <= 64:
                        norm_ttl = 64
                    elif ttl <= 128:
                        norm_ttl = 128
                    else:
                        norm_ttl = 255
                    
                    key = (norm_ttl, window)
                    return self.os_signatures.get(key, f"Desconocido (TTL:{ttl}, Win:{window})")
        except:
            pass
        return "No determinado"

    def detect_by_ping(self):
        """Usa ICMP echo request para detectar OS"""
        try:
            pkt = IP(dst=self.target)/ICMP()
            response = sr1(pkt, timeout=2, verbose=0)
            if response:
                ttl = response.ttl
                if ttl <= 64:
                    return "Linux/Unix"
                elif ttl <= 128:
                    return "Windows"
                elif ttl <= 255:
                    return "Router/Switch"
        except:
            pass
        return None

    def run(self):
        print(f"\n[🖥️] Detectando OS en {self.target}")
        
        # Método 1: ICMP
        os_icmp = self.detect_by_ping()
        if os_icmp:
            print(f"  [ICMP] OS probable: {os_icmp}")
        
        # Método 2: TCP fingerprint
        os_tcp = self.detect_by_ttl_and_window()
        print(f"  [TCP]  Fingerprint: {os_tcp}")
        
        return {"icmp": os_icmp, "tcp_fingerprint": os_tcp}
