#!/usr/bin/env python3
import argparse
import sys
from mxmap.banner import show_banner
from mxmap.syn_scanner import SYNScanner
from mxmap.os_detector import OSDetector
from mxmap.web_fuzzer import WebFuzzer
from mxmap.shodan_lookup import ShodanLookup
from mxmap.stealth import StealthMode

def main():
    show_banner()
    
    parser = argparse.ArgumentParser(description="MX-map - El reemplazo definitivo de Nmap")
    parser.add_argument("-t", "--target", help="IP o dominio objetivo")
    parser.add_argument("-p", "--ports", default="1-1000", help="Rango de puertos")
    parser.add_argument("--syn-scan", action="store_true", help="Escaneo SYN raw (requiere sudo)")
    parser.add_argument("--detect-os", action="store_true", help="Detección de sistema operativo")
    parser.add_argument("--web-fuzz", help="URL para fuzzing web (ej: http://ejemplo.com/)")
    parser.add_argument("--shodan", help="Consulta información en Shodan (requiere API key)")
    parser.add_argument("--stealth", action="store_true", help="Modo sigiloso con retardos aleatorios")
    parser.add_argument("--shodan-key", help="Tu API key de Shodan", default="")
    
    args = parser.parse_args()
    
    # Parsear puertos
    if "-" in args.ports:
        start, end = map(int, args.ports.split("-"))
        ports = list(range(start, end + 1))
    else:
        ports = [int(p) for p in args.ports.split(",")]
    
    # Modo sigiloso
    stealth = StealthMode(base_delay=0.5, jitter=0.3, decoy_mode=args.stealth) if args.stealth else None
    
    # Ejecutar módulos según argumentos
    if args.syn_scan and args.target:
        scanner = SYNScanner(args.target, ports)
        if args.stealth:
            open_ports = stealth.scan_with_stealth(scanner.syn_scan_port, ports)
        else:
            open_ports = scanner.scan()
        print(f"\n[✅] Escaneo completado: {len(open_ports)} puertos abiertos")
    
    if args.detect_os and args.target:
        os_detector = OSDetector(args.target)
        os_detector.run()
    
    if args.web_fuzz:
        fuzzer = WebFuzzer(args.web_fuzz)
        fuzzer.run()
    
    if args.shodan:
        shodan = ShodanLookup(args.shodan_key or args.shodan)
        shodan.run(args.shodan)
    
    if not any([args.syn_scan, args.detect_os, args.web_fuzz, args.shodan]):
        parser.print_help()

if __name__ == "__main__":
    main()
