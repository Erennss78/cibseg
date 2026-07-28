# cibseg — Toolkit de reset de contraseña (deber de ciberseguridad)

Herramientas para **vulnerar** (Fase 1) y **arreglar** (Fase 2) un flujo de
recuperación de contraseña débil (CWE-640 / CWE-330 / CWE-384).

> ⚠️ Solo para uso educativo contra sistemas que estás autorizado a probar
> (el lab local o el sistema del docente para el deber).

## Requisitos
- **Python 3** (ya viene en Mac/Linux). Comprobá con `python3 --version`.
- Nada más: todo usa la librería estándar, no hay que instalar dependencias.

## Archivos
| Archivo | Para qué |
|---|---|
| `app_vulnerable.py` | Sistema de práctica con los bugs. Para entrenar. |
| `atacante.py` | Exploit ya funcionando contra `app_vulnerable.py`. |
| `recon_endpoints.py` | Descubre las rutas `/reset...` de un sistema. |
| `analizar_token.py` | Dice qué debilidad tiene un token (timestamp, secuencial…). |
| `exploit_generico.py` | Exploit configurable para el sistema real. |
| `app_seguro.py` | Versión parcheada. Referencia para la Fase 2. |
| `checklist_network.md` | Qué mirar en el Network tab del navegador. |

---

## Practicar primero (local, recomendado)

Abrí **dos terminales** en la carpeta del repo.

**Terminal 1 — levantar el sistema vulnerable:**
```bash
python3 app_vulnerable.py
```
Queda escuchando en `http://127.0.0.1:8000`. Dejalo corriendo.

**Terminal 2 — lanzar el ataque:**
```bash
python3 atacante.py
```
Vas a ver la toma de control: enumeración, predicción del token y reuso.
Con eso confirmás que todo funciona en tu máquina.

Para parar el servidor: `Ctrl+C` en la Terminal 1.

---

## Atacar el sistema real (Fase 1 del deber)

### Paso 1 — Reconocer con el navegador
Seguí `checklist_network.md`. Abrí la URL del profe, `F12` → **Network**,
marcá **Preserve log**, usá el formulario de "olvidé mi contraseña" y anotá:
- La URL a la que se envía → tu `BASE`
- Los endpoints y nombres de campo (`email`, `token`, `password`)
- El formato del token

### Paso 2 — (opcional) descubrir rutas
Si no las ves claras en el Network, editá `BASE` en `recon_endpoints.py` y:
```bash
python3 recon_endpoints.py
```

### Paso 3 — Identificar la debilidad del token
Pedí 2-3 resets de **tu** cuenta, copiá los tokens dentro de la lista `TOKENS`
en `analizar_token.py`, y corré:
```bash
python3 analizar_token.py
```
Te dirá si es corto, timestamp, secuencial o hash de un dato conocido.
Eso define el `MODO` de ataque.

### Paso 4 — Explotar
Editá el bloque `CONFIG` arriba de `exploit_generico.py` con los datos del
Paso 1, poné el `MODO` según el Paso 3 (`"prediccion"`, `"fuerza_bruta"` o
`"reuso"`) y corré:
```bash
python3 exploit_generico.py
```

### Paso 5 — Guardar evidencia
Copiá la salida de los scripts (antes/después de la contraseña, el token
acertado). Es lo que mostrás cuando te revisen el estado de vulneración.

---

## Arreglar (Fase 2 del deber)
`app_seguro.py` muestra cada corrección: token CSPRNG de 256 bits, un solo uso,
expiración (TTL), comparación en tiempo constante, rate limiting y respuesta
genérica anti-enumeración. Usalo como mapa de qué cambiar en el código real.

Para verificar el parche, apuntá el mismo exploit contra el sistema arreglado
(en el lab: cambiá `BASE` a `http://127.0.0.1:8001` y corré `app_seguro.py`):
la predicción falla, el brute-force choca con `429` y el reuso da error.
