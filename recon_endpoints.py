"""
Recon de endpoints de reset — descubre las rutas del sistema del docente.
Prueba nombres comunes de rutas y metodos (GET/POST) y reporta cuales existen
(o sea, cuales NO devuelven 404). Es el paso previo a configurar el exploit.

Uso:
  1. Pone la URL base del sistema en BASE.
  2. python3 recon_endpoints.py
  3. Con lo que aparezca, llena EP_PEDIR / EP_CONFIRMAR en exploit_generico.py.

Solo hace requests a rutas; no envia datos de ataque. Correr solo contra un
sistema que estas autorizado a probar.
"""
import urllib.parse
import urllib.request

# ============================= CONFIG =============================
BASE = "http://127.0.0.1:8000"
# Nombres candidatos de rutas (es/en, con y sin prefijos comunes).
RUTAS = [
    "/reset", "/reset/pedir", "/reset/confirmar", "/reset/request", "/reset/confirm",
    "/forgot", "/forgot-password", "/forgot_password", "/password/reset",
    "/password/forgot", "/recover", "/recuperar", "/olvide", "/olvide-password",
    "/restablecer", "/cambiar-password", "/reset-password", "/reset_password",
    "/api/reset", "/api/forgot", "/api/password/reset", "/auth/reset",
    "/auth/forgot", "/user/reset", "/account/reset",
]
METODOS = ["GET", "POST"]
# =================================================================


def probar(ruta, metodo):
    url = BASE + ruta
    data = b"probe=1" if metodo == "POST" else None
    req = urllib.request.Request(url, data=data, method=metodo)
    try:
        with urllib.request.urlopen(req, timeout=4) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code          # 400/405/etc. => la ruta EXISTE, no es 404
    except Exception as e:
        return f"err:{type(e).__name__}"


def recon():
    print(f"== Recon de endpoints en {BASE} ==\n")
    encontrados = []
    # 404 = ruta no existe; 501 = el server no implementa ese metodo (ruido global).
    RUIDO = (404, 501, "err:URLError", "err:timeout")
    for ruta in RUTAS:
        for metodo in METODOS:
            codigo = probar(ruta, metodo)
            if codigo not in RUIDO:
                marca = "  <-- CANDIDATO" if isinstance(codigo, int) and codigo != 404 else ""
                print(f"  {metodo:4} {ruta:28} -> {codigo}{marca}")
                if isinstance(codigo, int):
                    encontrados.append((metodo, ruta, codigo))

    print("\n== Resumen ==")
    if not encontrados:
        print("  Nada respondio distinto de 404. Revisa BASE o el puerto,")
        print("  o agrega mas nombres de ruta a la lista RUTAS.")
        return
    # 405 (metodo no permitido) es una pista fuerte: la ruta existe pero con otro metodo.
    for metodo, ruta, codigo in encontrados:
        pista = ""
        if codigo == 405: pista = "  (existe, probar el otro metodo)"
        elif codigo == 400: pista = "  (existe, espera parametros -> este es el endpoint)"
        elif codigo == 200: pista = "  (responde OK)"
        print(f"  {metodo:4} {ruta:28} {codigo}{pista}")
    print("\n  Copia el que reciba parametros a EP_PEDIR / EP_CONFIRMAR en exploit_generico.py")


if __name__ == "__main__":
    recon()
