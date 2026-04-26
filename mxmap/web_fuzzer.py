#!/usr/bin/env python3
import requests
import threading
from urllib.parse import urljoin

class WebFuzzer:
    def __init__(self, target_url, wordlist=None, threads=10):
        self.target = target_url
        self.wordlist = wordlist or [
            "admin", "login", "wp-admin", "backup", "config", 
            "phpmyadmin", "api", "v1", "docs", "dashboard",
            "user", "private", ".git", ".env", "robots.txt"
        ]
        self.threads = threads
        self.found = []
        self.lock = threading.Lock()

    def check_directory(self, directory):
        """Verifica si el directorio existe"""
        url = urljoin(self.target, directory)
        try:
            response = requests.get(url, timeout=3, allow_redirects=False)
            if response.status_code in [200, 201, 403, 401]:
                size = len(response.content)
                with self.lock:
                    self.found.append({
                        "path": url,
                        "status": response.status_code,
                        "size": size
                    })
                    print(f"  [+] DIRECTOIO ENCONTRADO: {url} (Status: {response.status_code})")
        except:
            pass

    def run(self):
        print(f"\n[🌐] Fuzzing web en {self.target}")
        threads_list = []
        
        for directory in self.wordlist:
            t = threading.Thread(target=self.check_directory, args=(directory,))
            threads_list.append(t)
            t.start()
            
            if len(threads_list) >= self.threads:
                for t in threads_list:
                    t.join()
                threads_list = []
        
        for t in threads_list:
            t.join()
        
        print(f"\n  [+] Total encontrados: {len(self.found)}")
        return self.found
