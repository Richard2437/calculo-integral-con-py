import os
import sys
import json
import socket
import webbrowser
import tempfile
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

# Configurar cache de matplotlib de forma segura en carpeta temporal existente
cache_dir = os.path.join(tempfile.gettempdir(), "matplotlib_cache")
os.makedirs(cache_dir, exist_ok=True)
os.environ["MPLCONFIGDIR"] = cache_dir

import calculo_core

DIRECTORIO_WEB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")

class CalculoIntegralServerHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORIO_WEB, **kwargs)

    def do_GET(self):
        url_parsed = urllib.parse.urlparse(self.path)
        path = url_parsed.path

        if path == "/api/presets":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(calculo_core.PREAJUSTES).encode("utf-8"))
            return

        if path == "/" or path == "":
            self.path = "/index.html"

        return super().do_GET()

    def do_POST(self):
        url_parsed = urllib.parse.urlparse(self.path)
        path = url_parsed.path

        if path == "/api/calculate":
            content_length = int(self.headers.get("Content-Length", 0))
            body_bytes = self.rfile.read(content_length)
            
            try:
                params = json.loads(body_bytes.decode("utf-8"))
                expr_str = params.get("expr", "exp(-x**2)")
                a = params.get("a", 0.0)
                b = params.get("b", 1.0)
                n = int(params.get("n", 4))
                
                # Ejecutar análisis numérico
                resultado = calculo_core.calcular_analisis_completo(expr_str, a, b, n)
                # Generar imagen gráfica en Base64
                resultado["imagen_grafico"] = calculo_core.generar_imagen_base64(resultado)
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(resultado).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):
        # Silenciar logs ruidosos de peticiones estáticas
        pass

def encontrar_puerto_libre(puerto_preferido=5000):
    for puerto in [puerto_preferido, 5001, 5050, 8000, 8080]:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(('127.0.0.1', puerto))
                return puerto
        except Exception:
            continue
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', 0))
            return s.getsockname()[1]
    except Exception:
        return puerto_preferido

def iniciar_servidor_web(puerto=None, auto_abrir=True):
    ruta_index = os.path.abspath(os.path.join(DIRECTORIO_WEB, "index.html"))
    
    if puerto is None:
        puerto = encontrar_puerto_libre(5000)
        
    try:
        server = HTTPServer(("127.0.0.1", puerto), CalculoIntegralServerHandler)
        url = f"http://127.0.0.1:{puerto}/"
        
        print("=" * 65)
        print("  SIMULADOR WEB DE INTEGRACIÓN NUMÉRICA · CÁLCULO INTEGRAL")
        print("=" * 65)
        print(f" Servidor iniciado con éxito en: {url}")
        print(" Abre este enlace en tu navegador o proyector para mostrar la demo.")
        print(" Presiona Ctrl+C en la terminal para detener el servidor.")
        print("=" * 65)
        
        if auto_abrir:
            try:
                webbrowser.open(url)
            except Exception:
                pass
                
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido por el usuario.")
        finally:
            server.server_close()
            
    except Exception as e:
        print(f"\nNota: No se pudo enlazar el socket del servidor local ({e}).")
        print("Abriendo la interfaz web directamente en tu navegador...")
        file_url = f"file:///{ruta_index.replace(os.sep, '/')}"
        print(f"Ruta: {file_url}")
        try:
            webbrowser.open(file_url)
        except Exception:
            pass

if __name__ == "__main__":
    iniciar_servidor_web()
