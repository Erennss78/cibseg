# 🌅 Empezar aquí mañana — Black-box testing de Avisarás (local)

> Sesión que dejaste el 29-jul ~4am (hiperfoco épico, pero le hiciste caso a la
> razón y te fuiste a dormir — bien ahí). Acá está TODO para retomar sin perder tiempo.
>
> Regla de siempre: SOLO tus apps, en LOCAL. Nada sin permiso escrito. Es tuyo
> (repo Erennss78/avisaras-web + tu Cloudflare), así que estás cubierto.

## Dónde quedaste

- avisaras.com (producción) → lo escaneaste desde afuera: **superficie limpia**,
  cero vulns reales, solo mejoras menores (CSP unsafe-inline, headers cross-origin,
  DMARC p=none). Ya empezaste a arreglar el CSP en la rama `feat/aws-migration`.
- Conclusión: la capa EXTERIOR (scanners) está limpia. Falta la capa PROFUNDA
  (lógica, autenticado) → que es la que de verdad prueba tu app.
- Hoy toca: levantar la app en LOCAL y hacer black-box de la lógica interna.

## Paso 1 — Levantar la app (desde ~/Documents/Eventshow/web)

Necesitás Docker + Node corriendo.

```bash
cd ~/Documents/Eventshow/web

cp .env.example .env
# editá .env → AUTH_SECRET con:  openssl rand -base64 32
# (DATABASE_URL ya apunta a localhost, dejalo)

npm install
npm run db:up          # Postgres en Docker (puerto 5433)
npm run db:migrate     # crea las tablas
npm run db:seed:demo   # siembra datos + cuenta de prueba
npm run dev            # → http://localhost:3000
```

## Paso 2 — Las cuentas de prueba

- El seed crea: **`demo-ofertante@avisaras.com`** (rol ofertante/offerer).
- **Auth es passwordless (magic link):** al loguearte, el link/token de acceso
  se **imprime en la consola** donde corre `npm run dev` (no manda email real en dev).
  → Copiás ese link de la terminal y lo abrís para entrar. Ideal para testear.
- Para IDOR necesitás DOS cuentas: usá la demo (A) y **registrá una segunda** (B)
  con otro email cualquiera (el magic link también sale por consola).
- Panel admin en **`/admin`** → probá si un usuario normal llega ahí (autorización).

## Paso 3 — El testing (seguí `02-comandos/TESTING_LOGICA_interno.md`)

Orden recomendado (de más fácil a más jugoso):

1. **Setup Burp:** Proxy → Open Browser, navegá localhost:3000 logueado como A.
2. **IDOR** (empezá acá): hacé una acción tuya (ver reserva/perfil), capturá la
   petición en Burp Repeater, cambiá el ID por uno de B. ¿Ves datos de B? → BUG.
3. **Autorización:** logueado como usuario normal, intentá `/admin` y rutas de
   ofertante que no te correspondan. ¿Te deja? → BUG.
4. **Reset de contraseña (tu especialidad):** pedí reset, mirá el token en la
   consola, analizalo con `analizar_token.py` — ¿es fuerte? ¿single-use? ¿expira?
5. **Lógica de negocio:** valores negativos en precio/aforo, saltar pasos de un
   flujo, reservar evento lleno o con fecha pasada, cupón dos veces.
6. **Manipulación:** cambiar precios/totales que vengan del cliente, tipos raros.

## Paso 4 — Validar (NO reportar sin PoC)

Cada cosa "rara" que encuentres:
- Reproducila a mano en Burp (petición exacta + respuesta).
- Confirmala en el código (whitebox): ¿el endpoint chequea dueño/rol o confía en
  el input? → `grep -rn "params" src/app/api/`
- Solo entonces es un bug real. Anotalo con su PoC.

## Recordatorio para tu cabeza de pentester

- "No encontrar nada" en los scanners fue NORMAL — tu app está bien hecha en la
  superficie. Los bugs reales (si los hay) están en la LÓGICA, que recién vas a
  probar ahora. Ahí viene la frustración y los hallazgos REALES que buscás.
- Frustrarte es parte del oficio: vas a probar 20 cosas y 19 no van a dar nada.
  La 20 que sí, vale por las 19. Eso es pentesting de verdad.
- Sos programador Y atacante a la vez: cada bug que encuentres te hace mejor en
  las dos cosas.

Dormí bien. Mañana rompés tu propia app (con permiso, en local 😄).
