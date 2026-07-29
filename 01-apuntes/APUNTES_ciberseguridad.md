# Apuntes de Ciberseguridad — conceptos clave

> Materia que me interesa. Conceptos aprendidos trabajando el deber de
> reset de contraseña débil (CWE-640 / CWE-330 / CWE-384).

## 1. La vulnerabilidad de reset de contraseña

El token de reset es una llave temporal que autoriza el cambio de contraseña.
Falla si es débil en **5 dimensiones** (y es multiplicativo — peor si fallan varias):

| Dimensión | Ataque si falla |
|---|---|
| Entropía (aleatorio y largo) | Fuerza bruta / adivinar |
| Predecibilidad (tiempo/ID/secuencia) | Calcular el token, no adivinarlo |
| Rate limiting | Fuerza bruta automatizada |
| Un solo uso | Token filtrado = acceso repetido |
| Expiración (TTL) | Token viejo sigue sirviendo |

**El ataque estrella — predicción:** si el token deriva del reloj, pido un reset
de mi cuenta (veo token T), pido el de la víctima un instante después → su token
es T ± delta chico → lo acierto en pocos intentos.

## 2. El fix (remediación)

- Token **CSPRNG de 256 bits** (`secrets.token_urlsafe(32)`) — no predecible.
- **Un solo uso**: invalidar atómicamente al usarse.
- **TTL corto** (15-60 min).
- Guardar el **hash** del token, no el token; comparar en **tiempo constante**
  (`hmac.compare_digest`).
- **Rate limiting** + respuesta **genérica** (anti-enumeración de usuarios).

## 3. Modus operandi del atacante

Fases: reconocimiento → análisis del token → explotación → toma de control.

**Anonimato (ocultar origen):** VPN, Tor, cadenas de proxy, redes ajenas.
Cada capa sube el costo de rastreo pero ninguna es perfecta.

## 4. Rastros: los conceptos que más me marcaron

- **Los logs del ISP NO se pueden borrar** — están en la infraestructura de la
  compañía de internet, fuera del alcance del atacante. Solo se **ofuscan**
  (VPN hace que registren "conexión a VPN" en vez del ataque).
- **Ofuscar ≠ borrar.** Ofuscar se hace desde afuera (cliente HTTP). Borrar logs
  del servidor requiere **haber comprometido el servidor** (root/shell) — es un
  ataque aparte, mucho más profundo. El exploit de reset solo da acceso a una
  **cuenta de la app**, no al servidor.
- **La RAM es volátil** — tokens en memoria, procesos, conexiones se pierden al
  apagar. En forense se captura primero (orden de volatilidad).
- **El rastro no se elimina, se fragmenta.** Se reparte en ISP, backups, RAM de
  terceros, syslog central. Basta reconstruir un fragmento para romper el anonimato.

## 5. ¿Existe ser irrastreable?

- **Absoluta: NO existe.** Siempre generás datos en lugares que no controlás.
- **Práctica: SÍ, pero frágil.** Se logra apilando capas independientes (red
  ajena + Tor + hardware desechable + cuentas desechables + cero mezcla con la
  vida real + operar en RAM). Cae con **un solo error humano de OPSEC** — el
  eslabón débil nunca es la tecnología, es la persona sostenida en el tiempo
  (casos reales: Silk Road, LulzSec — la cripto aguantó, el humano falló).

**Frase clave:** "La irrastreabilidad absoluta no existe; solo la práctica, que
se pierde con un único error de OPSEC. El rastro no se elimina, se fragmenta."

## 6. Conexión con la defensa

El defensor no apuesta a que el atacante no deje rastro — apuesta a **recolectar
suficientes fragmentos** (logs centralizados e inmutables, monitoreo, retención,
captura de RAM) para reconstruir el incidente aunque el atacante sea cuidadoso.
Por eso la remediación no es solo bloquear, sino **detectar y registrar**.
