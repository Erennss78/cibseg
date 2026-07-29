"""
Recon de endpoints — descubre rutas de un sistema web.

Mejoras vs. version basica:
  - Wordlist externa (archivo) ademas de la lista incorporada.
  - Concurrencia (varias rutas a la vez) -> mucho mas rapido.
  - Fingerprinting: detecta la tecnologia por headers (Server, X-Powered-By).
  - Deteccion por status + TAMANO de respuesta -> evita falsos positivos de
    "soft 404" (paginas de error que devuelven 200).
  - Pausa configurable entre lotes (buena practica, evita bloqueos).
  - Guarda hallazgos en JSON para el informe.

USO SOLO en tu lab o en sistemas publicos de practica autorizados
(ver PRACTICA.md). Apuntar BASE a un sistema ajeno sin permiso es ilegal.

Correr:  python3 recon_endpoints.py
"""
import json
import time
import random
import string
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============================= CONFIG =============================
BASE = "http://testphp.vulnweb.com"     # objetivo (lab o sitio de practica)
WORDLIST_FILE = None                     # ruta a un archivo de rutas, o None
HILOS = 12                               # peticiones concurrentes
PAUSA = 0.0                              # segundos de pausa tras cada lote
GUARDAR = "recon_hallazgos.json"         # archivo de salida, o None
METODOS = ["GET", "POST"]
RUIDO = (404, 501)                       # codigos que se consideran "no existe"

# Lista incorporada (fallback si no hay wordlist externa)
RUTAS_BASE = [
    "/reset", "/reset/pedir", "/reset/confirmar", "/forgot", "/forgot-password",
    "/password/reset", "/recover", "/recuperar", "/restablecer", "/reset-password",
    "/api/reset", "/api/forgot", "/auth/reset", "/auth/forgot", "/login", "/admin",
    "/user", "/account", "/api", "/dashboard", "/config", "/backup", "/uploads",
]
# =================================================================


def cargar_rutas():
    if WORDLIST_FILE:
        try:
            with open(WORDLIST_FILE) as f:
                rutas = [l.strip() for l in f if l.strip() and not l.startswith("#")]
            return [r if r.startswith("/") else "/" + r for r in rutas]
        except OSError as e:
            print(f"[!] no pude leer la wordlist ({e}); uso la incorporada")
    return RUTAS_BASE


def pedir(ruta, metodo):
    """Devuelve (status, tamano, headers) o (None, 0, {}) si falla."""
    url = BASE + ruta
    data = b"probe=1" if metodo == "POST" else None
    req = urllib.request.Request(url, data=data, method=metodo,
                                 headers={"User-Agent": "Mozilla/5.0 (recon-lab)"})
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            cuerpo = r.read()
            return r.status, len(cuerpo), dict(r.headers)
    except urllib.error.HTTPError as e:
        cuerpo = e.read()
        return e.code, len(cuerpo), dict(e.headers)
    except Exception:
        return None, 0, {}


def baseline_soft404():
    """Pide una ruta que seguro NO existe para conocer el tamano del 'error tipo'.
    Si una ruta real devuelve el mismo status y tamano, es un falso positivo."""
    aleatoria = "/" + "".join(random.choices(string.ascii_lowercase, k=16))
    status, tam, _ = pedir(aleatoria, "GET")
    return status, tam


def fingerprint():
    _, _, headers = pedir("/", "GET")
    pistas = {}
    for h in ("Server", "X-Powered-By", "X-AspNet-Version", "Via"):
        if h in headers:
            pistas[h] = headers[h]
    return pistas


def es_hallazgo(status, tam, base_status, base_tam):
    if status is None or status in RUIDO:
        return False
    # mismo status Y tamano que el soft-404 => misma pagina de error => no cuenta
    if status == base_status and abs(tam - base_tam) < 16:
        return False
    return True


def recon():
    print(f"== Recon en {BASE} ==\n")

    fp = fingerprint()
    if fp:
        print("[*] Fingerprint (tecnologia detectada):")
        for k, v in fp.items():
            print(f"    {k}: {v}")
        print()

    base_status, base_tam = baseline_soft404()
    print(f"[*] Baseline soft-404: status={base_status}, tamano={base_tam}\n")

    tareas = [(r, m) for r in cargar_rutas() for m in METODOS]
    hallazgos = []

    with ThreadPoolExecutor(max_workers=HILOS) as pool:
        futuros = {pool.submit(pedir, r, m): (r, m) for r, m in tareas}
        for fut in as_completed(futuros):
            ruta, metodo = futuros[fut]
            status, tam, _ = fut.result()
            if es_hallazgo(status, tam, base_status, base_tam):
                pista = ""
                if status == 400: pista = "  (existe, espera parametros)"
                elif status == 405: pista = "  (existe, otro metodo)"
                elif status == 200: pista = "  (responde OK)"
                elif status in (301, 302): pista = "  (redirige)"
                print(f"  {metodo:4} {ruta:24} -> {status} [{tam}b]{pista}")
                hallazgos.append({"metodo": metodo, "ruta": ruta,
                                  "status": status, "tamano": tam})
    if PAUSA:
        time.sleep(PAUSA)

    print(f"\n== {len(hallazgos)} hallazgos ==")
    if GUARDAR and hallazgos:
        with open(GUARDAR, "w") as f:
            json.dump({"base": BASE, "fingerprint": fp, "hallazgos": hallazgos}, f, indent=2)
        print(f"   guardados en {GUARDAR}")
    if not hallazgos:
        print("   nada distinto del baseline. Proba otra wordlist o revisa BASE.")


if __name__ == "__main__":
    recon()
