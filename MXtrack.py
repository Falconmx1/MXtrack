#!/usr/bin/env python3
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
