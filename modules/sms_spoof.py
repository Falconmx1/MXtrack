#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from colorama import Fore, Style, init

init(autoreset=True)

def check_twilio_config():
    """Verifica si existe configuración de Twilio"""
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    phone_number = os.getenv('TWILIO_PHONE_NUMBER')
    
    if not all([account_sid, auth_token, phone_number]):
        print(f"{Fore.RED}❌ Twilio no configurado{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Para usar SMS spoofing:{Style.RESET_ALL}")
        print("1. Regístrate en https://twilio.com (consigues $15 gratis)")
        print("2. Verifica un número telefónico")
        print("3. Configura variables de entorno:")
        print(f"   {Fore.CYAN}export TWILIO_ACCOUNT_SID='tu_sid'{Style.RESET_ALL}")
        print(f"   {Fore.CYAN}export TWILIO_AUTH_TOKEN='tu_token'{Style.RESET_ALL}")
        print(f"   {Fore.CYAN}export TWILIO_PHONE_NUMBER='+1234567890'{Style.RESET_ALL}")
        return False
    return True

def send_sms_twilio(to_number, message, from_spoof=None):
    """
    Envía SMS usando Twilio
    NOTA: Twilio NO permite spoofing real de números no verificados
    """
    try:
        from twilio.rest import Client
        
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        from_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
            body=message,
            from_=from_number,
            to=to_number
        )
        
        print(f"{Fore.GREEN}✅ SMS enviado exitosamente!{Style.RESET_ALL}")
        print(f"   SID: {message.sid}")
        print(f"   Estado: {message.status}")
        return True
        
    except ImportError:
        print(f"{Fore.RED}❌ Instala twilio: pip install twilio{Style.RESET_ALL}")
        return False
    except Exception as e:
        print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        return False

def spoofing_alternatives():
    """Métodos alternativos sin Twilio"""
    print(f"\n{Fore.CYAN}📡 MÉTODOS ALTERNATIVOS DE SMS SPOOFING:{Style.RESET_ALL}")
    print("""
    1️⃣  SERVICIOS WEB GRATIS:
       - textnow.com (numero temporal)
       - smsreceivefree.com
       - receive-sms.cc
    
    2️⃣  EMAIL A SMS (operadores MX):
       - Telcel: 5512345678@sms.telcel.com
       - Movistar: 5512345678@correo.movistar.com.mx
       - AT&T: 5512345678@mms.att.net
    
    3️⃣  APIs GRATIS CON LIMITACIONES:
       - sms-manager (10 SMS/día)
       - smsgateway.me (con publicidad)
    
    4️⃣  SMS SPOOFING REAL (avanzado):
       - Configurar servidor SMTP propio
       - Usar gateways SMS antiguos
       - Kali Linux: social engineering toolkit (SET)
    """)

def sms_campaign_menu():
    """Menú principal de SMS spoofing"""
    print(f"\n{Fore.MAGENTA}═══════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.GREEN}📱 MÓDULO DE SMS SPOOFING{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}═══════════════════════════════════════════{Style.RESET_ALL}")
    
    print("\n1️⃣  Enviar SMS con Twilio (requiere cuenta)")
    print("2️⃣  Métodos alternativos gratis")
    print("3️⃣  Plantillas de ingeniería social")
    print("4️⃣  Volver")
    
    opcion = input("\n👉 Opción: ")
    
    if opcion == '1':
        if check_twilio_config():
            to = input("📱 Número destino (+código país): ")
            msg = input("💬 Mensaje a enviar: ")
            send_sms_twilio(to, msg)
    elif opcion == '2':
        spoofing_alternatives()
    elif opcion == '3':
        print(f"\n{Fore.CYAN}📝 PLANTILLAS PARA PHISHING/TESTING:{Style.RESET_ALL}")
        print("""
        [BANCO] 🏦
        "Bancoppel: Se detectó un cargo no reconocido de $2,500 MXN. 
        Si no reconoces, ingresa aquí: http://bit.ly/verificar-cargo"
        
        [PAQUETERÍA] 📦
        "DHL: Tu paquete #MX9823 no pudo entregarse. 
        Programa nueva entrega: https://dhl-mx.verificar.com"
        
        [REDES SOCIALES] 📱
        "Instagram: Alguien intentó acceder a tu cuenta desde CDMX.
        Verifica aquí: https://ig-seguridad.confirmar.com"
        
        [SORTEO] 🎁
        "Felicidades! Ganaste $5,000 MXN en sorteo Telcel.
        Reclama aquí antes de 24h: https://telcel-premios.win"
        """)
        print(f"{Fore.RED}⚠️ Estas plantillas son SOLO para pruebas autorizadas{Style.RESET_ALL}")

if __name__ == "__main__":
    sms_campaign_menu()
