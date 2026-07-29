"""
Portal de admisiones VULNERABLE — laboratorio de CWE-640 / CWE-330 / CWE-384.
Solo para uso educativo en un sistema que controlas.

Bugs intencionales (los que pide el plan de pruebas):
  1. Token derivado del timestamp   -> PREDECIBLE  (CWE-330)
  2. Token corto (6 digitos)        -> FUERZA BRUTA (keyspace chico)
  3. Sin rate limiting              -> se puede probar millones de veces
  4. Token reusable                 -> no es single-use (CWE-384)
  5. Sin expiracion (TTL)           -> vive para siempre
  6. Enumeracion de usuarios        -> respuesta distinta si el email existe

Correr:  python3 app_vulnerable.py   (escucha en http://127.0.0.1:8000)
"""
import time
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# "Base de datos" en memoria: email -> datos de la cuenta
USUARIOS = {
    "atacante@mail.com": {"password": "yo123", "cedula": None},
    "victima@portal.edu": {"password": "secreto-de-la-victima", "cedula": "0102030405"},
}
# tokens activos: token -> email
TOKENS = {}


def generar_token(email):
    # BUG 1+2: el token es el timestamp en milisegundos, recortado a 6 digitos.
    #          Predecible (depende del reloj) y corto (keyspace = 1.000.000).
    ms = int(time.time() * 1000)
    token = str(ms)[-6:]
    TOKENS[token] = email
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

        # --- Endpoint 1: pedir reset ---
        if ruta == "/reset/pedir":
            email = cuerpo.get("email", [""])[0]
            if email in USUARIOS:
                token = generar_token(email)
                # En la vida real el token va SOLO al email. Aca lo devolvemos
                # para simular el correo que el atacante recibe de SU cuenta.
                return self._json(200, {"msg": "token enviado", "_email_simulado": token})
            # BUG 6: respuesta distinta => enumeracion de usuarios
            return self._json(404, {"msg": "ese email no existe"})

        # --- Endpoint 2: validar token y cambiar password ---
        if ruta == "/reset/confirmar":
            token = cuerpo.get("token", [""])[0]
            nueva = cuerpo.get("password", [""])[0]
            # BUG 3: sin rate limiting -> cada request se procesa igual.
            # BUG 5: sin chequeo de expiracion.
            email = TOKENS.get(token)
            if email:
                USUARIOS[email]["password"] = nueva
                # BUG 4: NO borramos el token -> se puede reusar.
                return self._json(200, {"msg": f"password de {email} cambiada"})
            return self._json(400, {"msg": "token invalido"})

        self._json(404, {"msg": "ruta desconocida"})

    def log_message(self, *a):
        pass  # silenciar logs para ver mejor el ataque


if __name__ == "__main__":
    print("Portal VULNERABLE en http://127.0.0.1:8000  (Ctrl+C para parar)")
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
