# Checklist — Network tab (reconocimiento del reset)

Objetivo: sacar del navegador los 4 datos que necesita `exploit_generico.py`
(**BASE, endpoints, nombres de campo, formato del token**) sin adivinar nada.

## 0. Preparar
- [ ] Abrí la URL del sistema en Chrome/Firefox.
- [ ] `F12` → pestaña **Network**.
- [ ] Marcá **Preserve log** (que no se borre al recargar/redirigir).
- [ ] Filtro en **Fetch/XHR** (esconde imágenes, css, etc.).
- [ ] Creá 2 cuentas propias si podés (una "atacante", una "víctima" tuya) para
      capturar tokens y comparar.

## 1. Pedir el reset (endpoint EP_PEDIR)
- [ ] Usá el formulario "olvidé mi contraseña" con **tu** email.
- [ ] En Network aparece un request nuevo. Clic en él y mirá:
  - [ ] **Request URL** → esto es tu `BASE` + `EP_PEDIR`.
  - [ ] **Request Method** (POST casi siempre).
  - [ ] Pestaña **Payload / Request** → cómo se llama el campo del email
        (`email`? `correo`? `user`?) → va en `CAMPO_EMAIL`.
  - [ ] Pestaña **Response** → ¿devuelve algo? ¿el token viene acá o solo al mail?

### Detectar enumeración (punto 7 del plan) — hacelo ya, es gratis
- [ ] Repetí con un email que NO existe (`nada123@x.com`).
- [ ] Compará las dos respuestas (status y cuerpo) y el **tiempo** (columna Time).
  - Distintas → **vulnerable a enumeración**. Guardá captura de ambas.

## 2. Conseguir el token
- [ ] ¿Llega por email? Copiá el token o el link completo.
- [ ] ¿El link es `...?token=ABC123` o `.../reset/ABC123`? Anotá el formato.
- [ ] Pedí 2-3 resets seguidos y guardá **todos** los tokens en orden
      (esto alimenta `analizar_token.py` para ver si es timestamp/secuencial).

## 3. Confirmar / cambiar la contraseña (endpoint EP_CONFIRMAR)
- [ ] Abrí el link del reset y completá el form con Network abierto.
- [ ] Al enviar, mirá el request:
  - [ ] **Request URL** → `EP_CONFIRMAR`.
  - [ ] **Payload** → nombre del campo token (`token`? `code`? `oobCode`?) → `CAMPO_TOKEN`.
  - [ ] Nombre del campo de la nueva password → `CAMPO_PASS`.
  - [ ] **Response** en el éxito → qué texto/status devuelve (para ajustar `exito()`).

## 4. ¿Firebase nativo o casero?
Mirá el **dominio** de los requests de reset:
- [ ] `identitytoolkit.googleapis.com` → reset **nativo de Firebase = fuerte**.
      El bug está en otra parte, no acá.
- [ ] `*.cloudfunctions.net`, `*.run.app`, `/api/...`, Firestore, o el mismo dominio
      → flujo **casero = donde vive la vulnerabilidad**. Esa URL es tu `BASE`.

## 5. Botín para el exploit (copiá esto al CONFIG)
```
BASE         = ______________________________
EP_PEDIR     = ______________________________
EP_CONFIRMAR = ______________________________
CAMPO_EMAIL  = ______________________________
CAMPO_TOKEN  = ______________________________
CAMPO_PASS   = ______________________________
formato token= (numérico 6? hex largo? link con ?token=)
tokens capturados (en orden): ________________
```

## Tips
- Clic derecho en un request → **Copy → Copy as cURL**: te da la petición
  completa (headers, cookies, body). Pasámela y armo el exploit exacto.
- Si el form redirige y perdés el request, es por no tener **Preserve log**.
- Si hay **cookies/CSRF token** en el request, anotalo: puede que el exploit
  necesite mandarlos también (te ayudo a agregarlo si aparece).
