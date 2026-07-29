"""
Analizador de tokens de reset — reconocimiento a ciegas.
No ataca nada: solo caracteriza tokens que capturaste de TU cuenta y te dice
QUE debilidad tienen, para saber por donde atacar.

Uso:
  1. En el sistema del docente, pedi 2-3 resets seguidos de TU cuenta.
  2. Copia los tokens que llegan (al email o a la respuesta) aca abajo.
  3. python3 analizar_token.py

Responde a los puntos 1 y 2 del plan de pruebas:
  - longitud, charset, entropia efectiva
  - si es timestamp / secuencial / hash de un dato conocido (email, id)
"""
import re
import math
import time
import base64
import hashlib
from datetime import datetime

# ====== PEGA AQUI LOS TOKENS QUE CAPTURASTE (en orden de emision) ======
TOKENS = [
    # "495127",
    # "495431",
]
# Datos conocidos de TU cuenta, para probar tokens derivados de identificadores:
MI_EMAIL = "atacante@mail.com"
MI_ID = "1"
# =======================================================================


def charset(t):
    tipos = []
    if re.fullmatch(r"[0-9]+", t):            tipos.append("numerico")
    if re.fullmatch(r"[0-9a-fA-F]+", t):      tipos.append("hex")
    if re.fullmatch(r"[A-Za-z0-9_\-]+", t):   tipos.append("base64url")
    return tipos or ["mixto/desconocido"]


def entropia_bits(t):
    # bits = longitud * log2(tamano del alfabeto)  (cota superior optimista)
    if re.fullmatch(r"[0-9]+", t):        alfabeto = 10
    elif re.fullmatch(r"[0-9a-fA-F]+", t): alfabeto = 16
    elif re.fullmatch(r"[A-Za-z0-9_\-]+", t): alfabeto = 64
    else: alfabeto = 95
    return len(t) * math.log2(alfabeto)


def parece_timestamp(t):
    """Intenta leer el token (o su decode) como epoch en s / ms."""
    candidatos = []
    # como numero directo
    if t.isdigit():
        candidatos.append(int(t))
    # decodificando hex/base64 a numero
    try:
        candidatos.append(int(t, 16))
    except ValueError:
        pass
    ahora = time.time()
    for n in candidatos:
        for escala, unidad in ((1, "s"), (1000, "ms")):
            seg = n / escala
            # ventana razonable: entre 2015 y 2035
            if 1.42e9 < seg < 2.05e9:
                fecha = datetime.utcfromtimestamp(seg)
                return f"epoch en {unidad} -> {fecha} UTC (diferencia con ahora: {ahora - seg:.0f}s)"
    return None


def es_hash_de_dato_conocido(t):
    """Prueba si el token = hash(dato) para datos que el atacante conoce."""
    datos = {
        "mi_email": MI_EMAIL,
        "mi_id": MI_ID,
        "mi_email+id": MI_EMAIL + MI_ID,
    }
    algos = {"md5": hashlib.md5, "sha1": hashlib.sha1, "sha256": hashlib.sha256}
    hallazgos = []
    for nombre_dato, valor in datos.items():
        for nombre_algo, fn in algos.items():
            h = fn(valor.encode()).hexdigest()
            if t.lower() == h or t.lower() == h[:len(t)]:
                hallazgos.append(f"{nombre_algo}({nombre_dato})")
    return hallazgos


def analizar():
    if len(TOKENS) < 1:
        print("Pega al menos 1 token en la lista TOKENS.")
        return

    for i, t in enumerate(TOKENS):
        print(f"\n=== Token #{i+1}: {t!r} ===")
        print(f"  longitud   : {len(t)}")
        print(f"  charset    : {', '.join(charset(t))}")
        bits = entropia_bits(t)
        print(f"  entropia   : ~{bits:.0f} bits", end="")
        if bits < 120:
            print("  <-- DEBIL (bajo 120 bits, revisar)")
        else:
            print("  (fuerte por tamano)")

        ts = parece_timestamp(t)
        if ts:
            print(f"  TIMESTAMP  : {ts}  <-- PREDECIBLE (CWE-330)")

        hs = es_hash_de_dato_conocido(t)
        if hs:
            print(f"  DERIVADO   : coincide con {', '.join(hs)}  <-- CALCULABLE")

    # secuencialidad entre tokens
    if len(TOKENS) >= 2 and all(t.isdigit() for t in TOKENS):
        difs = [int(TOKENS[i+1]) - int(TOKENS[i]) for i in range(len(TOKENS)-1)]
        print(f"\n=== Correlacion entre tokens ===")
        print(f"  diferencias consecutivas: {difs}")
        if all(0 < d < 100000 for d in difs):
            print("  <-- SECUENCIAL / MONOTONICO: el token de la victima esta cerca del tuyo")


if __name__ == "__main__":
    analizar()
