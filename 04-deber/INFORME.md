# Informe — Vulnerabilidad en el flujo de recuperación de contraseña

**Autor:** Christian Guamán
**Materia:** Ciberseguridad
**Vulnerabilidad:** Mecanismo débil de recuperación de contraseña
**CWE:** CWE-640 (Weak Password Recovery), CWE-330 (Insufficiently Random Values), CWE-384 (Session/Token reuse)
**Severidad:** Alta (toma de control de cuenta → exposición de PII sensible)

---

## 1. Descripción de la vulnerabilidad

El flujo de "olvidé mi contraseña" emite un token que autoriza el cambio de
contraseña de una cuenta. Si ese token es adivinable, corto, predecible o
reutilizable, un atacante puede tomar el control de cuentas ajenas sin conocer
la contraseña original. En un portal de admisiones esto expone cédulas, fechas
de nacimiento, direcciones y flags de salud.

## 2. Debilidades identificadas

| # | Debilidad | Efecto |
|---|---|---|
| 1 | Token derivado del timestamp | Predecible (se calcula, no se adivina) |
| 2 | Token corto (6 dígitos, ~20 bits) | Vulnerable a fuerza bruta |
| 3 | Sin rate limiting | Se pueden probar millones de valores |
| 4 | Token reutilizable | Un token filtrado da acceso repetido |
| 5 | Sin expiración (TTL) | Un token viejo sigue sirviendo |
| 6 | Respuesta distinta según exista el email | Enumeración de usuarios |

## 3. Explotación (evidencia)

Ataque ejecutado sobre el entorno autorizado. Salida obtenida:

```
[*] Enumeracion (BUG 6):
    email real   -> (200, {'msg': 'token enviado', '_email_simulado': '709323'})
    email falso  -> (404, {'msg': 'ese email no existe'})
    respuestas distintas => confirmamos que la victima existe

[*] Ataque por PREDICCION (BUG 1+2):
    mi token observado: 709324
    ACERTADO con token 709324 (delta=0) -> password de victima@portal.edu cambiada

[*] Reuso del token (BUG 4): 200 => el token NO se quemo, sigue sirviendo

[+] Takeover completo: la password de la victima ahora es "hackeada-por-el-atacante"
```

**Resultado:** se tomó el control de la cuenta objetivo sin conocer su
contraseña. El token de la víctima (`709324`) cayó a un dígito del token propio
(`709323`) porque deriva del reloj, permitiendo acertar al primer intento.

## 4. Modus operandi y anti-forense del atacante

Ver documento adjunto `seccion_modus_operandi.md` para el detalle completo de
fases, técnicas de anonimato y anti-forense.

### 4.1 Justificación del método de anonimato utilizado

Durante la ejecución autorizada se utilizó una **VPN con salida en Hong Kong**
como única capa de ofuscación del origen. Se reconoce explícitamente que esta
medida es **insuficiente para lograr un anonimato real**, por las siguientes
razones:

- **El ISP** registra la conexión al servidor VPN (fecha, hora y volumen de
  datos), aunque no vea el contenido.
- **El propio proveedor de VPN** puede retener logs que, ante una orden judicial,
  vincularían la IP de salida con la IP real del origen.
- **La cuenta atacante** registrada en el sistema es una identidad directa que
  ningún VPN oculta.
- **La correlación temporal** entre las distintas fuentes de registro (ISP +
  servidor) permitiría ubicar al origen aun con la IP enmascarada.

Dado que esta fue una prueba **autorizada con fines educativos**, el objetivo
fue **generar evidencia**, no evadir la atribución; por ello no se aplicaron las
capas adicionales de anonimato (Tor, cadenas de proxy, cuentas desechables,
separación de identidad, ritmo lento). En un escenario real, un atacante
combinaría varias de esas técnicas, y aun así un defensor con logs
centralizados, monitoreo y captura de memoria podría reconstruir el incidente.
El anonimato del atacante es, por lo tanto, **probabilístico y no absoluto**.

## 5. Remediación

Correcciones aplicadas en la versión segura (`app_seguro.py`):

1. **Token CSPRNG de 256 bits** (`secrets.token_urlsafe(32)`) — no predecible ni
   brute-forceable.
2. **Un solo uso** — el token se invalida atómicamente al completarse el reset.
3. **Expiración (TTL)** de 15 minutos.
4. **Comparación en tiempo constante** (`hmac.compare_digest`) y almacenamiento
   del **hash** del token, no el token en claro.
5. **Rate limiting** por IP con respuesta `429`.
6. **Respuesta genérica** idéntica exista o no la cuenta (anti-enumeración).
7. **Invalidación agresiva**: un token nuevo anula los anteriores de la cuenta.

## 6. Verificación / Retest

El hallazgo se considera remediado cuando, contra el sistema corregido: la
predicción falla, la fuerza bruta choca con el rate-limiting (`429`), el reuso
del token es rechazado, los tokens expiran dentro del TTL y el endpoint de
solicitud no permite enumerar usuarios.
