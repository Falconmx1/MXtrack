#!/usr/bin/env python3
import random
import time
from functools import wraps

class StealthMode:
    def __init__(self, base_delay=0.5, jitter=0.3, decoy_mode=False):
        self.base_delay = base_delay
        self.jitter = jitter
        self.decoy_mode = decoy_mode
        self.packet_counter = 0
        self.decoy_ips = [
            "8.8.8.8", "1.1.1.1", "208.67.222.222", "9.9.9.9"
        ] if decoy_mode else []

    def random_delay(self):
        """Retardo aleatorio entre paquetes"""
        delay = self.base_delay + random.uniform(0, self.jitter)
        time.sleep(delay)
        return delay

    def jitter_timing(self):
        """Timing jitter para evadir detección"""
        if random.random() < 0.3:  # 30% de probabilidad de pausa extra
            extra_delay = random.uniform(0.1, 0.5)
            time.sleep(extra_delay)
            return extra_delay
        return 0

    def scan_with_stealth(self, scan_function, ports):
        """Wrapper para escaneos sigilosos"""
        print(f"\n[🥷] Modo sigiloso activado")
        print(f"  - Delay base: {self.base_delay}s")
        print(f"  - Jitter: ±{self.jitter}s")
        print(f"  - Decoys: {len(self.decoy_ips)} activos" if self.decoy_ips else "  - Decoys: desactivados")
        
        results = []
        for port in ports:
            delay = self.random_delay()
            self.jitter_timing()
            result = scan_function(port)
            if result:
                results.append(result)
            self.packet_counter += 1
            
            if self.packet_counter % 10 == 0:
                # Cada 10 paquetes, pausa más larga
                time.sleep(random.uniform(1, 3))
                
        return results

    def get_proxy_chain(self):
        """Configuración de proxys (para futura implementación)"""
        # Aquí se podría integrar Tor, proxies SOCKS5, etc
        return None

# Decorador para aplicar sigilo automáticamente
def stealth_wrapper(stealth_instance):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            stealth_instance.random_delay()
            stealth_instance.jitter_timing()
            return func(*args, **kwargs)
        return wrapper
    return decorator
