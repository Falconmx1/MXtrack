#!/usr/bin/env python3
import random
import time
from scapy.all import IP, TCP, sr1, conf

conf.verb = 0  # Modo silencioso

class SYNScanner:
    def __init__(self, target, ports, timeout=2):
        self.target = target
        self.ports = ports
        self.timeout = timeout
        self.open_ports = []

    def syn_scan_port(self, port):
        """Envía un paquete SYN raw y analiza la respuesta"""
        src_port = random.randint(1024, 65535)
        ip_packet = IP(dst=self.target)
        tcp_packet = TCP(sport=src_port, dport=port, flags="S", seq=1000)
        
        response = sr1(ip_packet/tcp_packet, timeout=self.timeout, verbose=0)
        
        if response:
            if response.haslayer(TCP):
                if response.getlayer(TCP).flags == 0x12:  # SYN-ACK
                    self.open_ports.append(port)
                    # Enviar RST para cerrar conexión sigilosa
                    rst_packet = IP(dst=self.target)/TCP(sport=src_port, dport=port, flags="R")
                    sr1(rst_packet, timeout=1, verbose=0)
                    return True
        return False

    def scan(self):
        print(f"\n[🔥] Escaneo SYN Raw en {self.target}")
        for port in self.ports:
            if self.syn_scan_port(port):
                print(f"  [+] Puerto {port} ABIERTO (SYN scan)")
            else:
                print(f"  [-] Puerto {port} cerrado/filtrado")
        return self.open_ports
