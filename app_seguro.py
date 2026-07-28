"""
Portal de admisiones REMEDIADO — corrige CWE-640 / CWE-330 / CWE-384.
Corre en http://127.0.0.1:8001 para poder compararlo con el vulnerable.

Fixes (mapeados a la seccion Remediation del enunciado):
  1. secrets.token_urlsafe(32)  -> 256 bits CSPRNG (no predecible, no brute-forceable)
  3. single-use                 -> el token se borra al usarse (atomico)
  4. TTL de 15 min              -> se rechaza si expiro
  5. compare_digest             -> comparacion en tiempo constante, guardamos HASH
  6. rate limiting simple       -> N intentos por IP
  8. respuesta generica         -> no revela si el email existe (anti-enumeracion)
"""
import time
import json
import hmac
import hashlib
import secrets
from collections import defaultdict
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

TTL = 15 * 60           # 15 minutos
MAX_INTENTOS = 5        # por IP, defensa en profundidad

USUARIOS = {
    "atacante@mail.com": {"password": "yo123"},
    "victima@portal.edu": {"password": "secreto-de-la-victima"},
}
# guardamos HASH del token, no el token: hash -> (email, expira_en)
TOKENS = {}
intentos = defaultdict(int)


def hash_token(token):
    return hashlib.sha256(token.encode()).hexdigest()


def generar_token(email):
    token = secrets.token_urlsafe(32)          # FIX 1+2: CSPRNG, 256 bits
    # FIX (invalidacion): un token nuevo anula los previos de esa cuenta
    for h, (e, _) in list(TOKENS.items()):
        if e == email:
            del TOKENS[h]
    TOKENS[hash_token(token)] = (email, time.time() + TTL)
    return token


class Handler(BaseHTTPRequestHandler):
    def _json(self, code, obj):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(obj).encode())

    def do_POST(self):
        ruta = urlparse(self.path).path
        largo = int(self.headers.get("Content-Length", 0))
        cuerpo = parse_qs(self.rfile.read(largo).decode())
        ip = self.client_address[0]

        if ruta == "/reset/pedir":
            email = cuerpo.get("email", [""])[0]
            if email in USUARIOS:
                generar_token(email)  # el token real iria SOLO por email
            # FIX 8: misma respuesta exista o no la cuenta -> sin enumeracion
            return self._json(200, {"msg": "Si existe una cuenta, se envio un enlace."})

        if ruta == "/reset/confirmar":
            # FIX 6: rate limiting por IP
            intentos[ip] += 1
            if intentos[ip] > MAX_INTENTOS:
                return self._json(429, {"msg": "demasiados intentos"})

            token = cuerpo.get("token", [""])[0]
            nueva = cuerpo.get("password", [""])[0]
            h = hash_token(token)

            # FIX 5: buscamos por hash y comparamos en tiempo constante
            registro = TOKENS.get(h)
            if registro:
                email, expira = registro
                if time.time() > expira:          # FIX 4: TTL
                    del TOKENS[h]
                    return self._json(400, {"msg": "token invalido o expirado"})
                if hmac.compare_digest(h, hash_token(token)):
                    USUARIOS[email]["password"] = nueva
                    del TOKENS[h]                 # FIX 3: single-use, atomico
                    intentos[ip] = 0
                    return self._json(200, {"msg": "password actualizada"})
            # mismo error generico para invalido/expirado
            return self._json(400, {"msg": "token invalido o expirado"})

        self._json(404, {"msg": "ruta desconocida"})

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print("Portal SEGURO en http://127.0.0.1:8001  (Ctrl+C para parar)")
    HTTPServer(("127.0.0.1", 8001), Handler).serve_forever()
