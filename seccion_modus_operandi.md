# Modus operandi y anti-forense del atacante

> Sección de investigación: cómo actuaría un atacante real para comprometer el
> flujo de reset de contraseña y qué técnicas usaría para dificultar su rastreo.

## 1. Fases del ataque

Un atacante real seguiría un ciclo similar al ejecutado en esta prueba:

1. **Reconocimiento** — identificar el endpoint de recuperación de contraseña,
   los nombres de campos y el formato del token (observando el tráfico del
   navegador o probando rutas comunes).
2. **Análisis del token** — pedir varios tokens de una cuenta propia para
   caracterizar su debilidad (longitud, entropía, si deriva del tiempo o de un
   identificador).
3. **Explotación** — según la debilidad: predicción (token derivado del reloj),
   fuerza bruta (token corto sin límite de intentos) o reutilización.
4. **Toma de control** — cambiar la contraseña de la cuenta objetivo sin conocer
   la original, obteniendo acceso completo a los datos sensibles.

## 2. Técnicas de anonimato (ocultar el origen)

Un atacante intentaría no revelar desde dónde opera, apilando capas:

| Técnica | Qué hace | Límite |
|---|---|---|
| **VPN** | Cambia la IP visible para el sitio destino. Elegir un país no cooperativo dificulta órdenes judiciales. | El ISP ve la conexión al VPN; el VPN puede loguear. |
| **Tor** | Encadena 3 nodos; ninguno ve origen y destino a la vez. | Análisis de tráfico, nodos de salida vigilados. |
| **Cadenas de proxy** (VPN→Tor→VPN) | Varias capas para que ningún eslabón tenga la foto completa. | Errores de configuración u OPSEC. |
| **Redes ajenas** | El tráfico sale de una IP que no es la del atacante. | Cámaras, MAC, correlación física. |

## 3. Técnicas anti-forense (no dejar huella en el objetivo)

- **Borrado o alteración de logs** de acceso del servidor tras el ataque.
- **Timestomping**: falsear fechas de archivos para confundir el análisis.
- **Operación en memoria (fileless)**: no escribir en disco; todo vive en RAM y
  se pierde al apagar el equipo.
- **Ritmo lento**: espaciar los intentos para no disparar rate-limiting ni
  alertas de volumen anómalo.
- **Identidad separada**: cuentas y correos desechables, sin reutilizar
  credenciales ni mezclar con la identidad real.

### 3.1 Ofuscar vs. borrar: dos cosas distintas

Es un error frecuente pensar que un mismo script "borra todo el rastro". Hay que
distinguir dos niveles:

- **Ofuscar (posible desde afuera):** lo que hace un exploit que actúa como
  cliente HTTP (como el de esta prueba). Puede enmascarar el origen (VPN/Tor),
  ir lento para no generar picos y mimetizar el tráfico (user-agents y horarios
  normales). **No borra nada**, solo dificulta la atribución y la detección.

- **Borrar logs (fase post-explotación):** eliminar los registros del servidor
  requiere **haber comprometido el servidor** primero (acceso shell/root a la
  máquina). Es un ataque **distinto y mucho más profundo** que el de reset de
  contraseña: este último solo otorga acceso a **una cuenta de la aplicación**,
  no al sistema operativo del servidor. Por eso el borrado de logs **no forma
  parte** de este exploit ni de su script.

- **Logs del ISP: no se pueden borrar.** Están en la infraestructura de la
  compañía de internet, fuera del alcance del atacante. La única defensa contra
  ellos es la **ofuscación** (que registren "conexión a un VPN" en vez del
  ataque), nunca la eliminación.

| Nivel | ¿Qué acceso requiere? | ¿El exploit de reset lo permite? |
|---|---|---|
| Ofuscar origen (VPN/Tor/ritmo) | Ninguno, se hace desde afuera | Sí |
| Borrar logs del servidor | Acceso root/shell al servidor | No (otro ataque aparte) |
| Borrar logs del ISP | Imposible para el atacante | No |

## 4. Por qué el rastro nunca desaparece del todo

El anonimato del atacante es **probabilístico, no absoluto**. Cada capa sube el
costo de rastrearlo, pero el rastro se reparte en lugares que el atacante no
controla:

| Capa usada | Qué la delata igual |
|---|---|
| VPN | El **ISP** registra la conexión al VPN; el proveedor de VPN puede guardar logs. |
| Tor | Correlación de tráfico entrada/salida; nodos de salida monitoreados. |
| Borrado de logs | Copias en un **syslog central**, backups, o la propia RAM. |
| Operación fileless | Un **volcado de RAM** en caliente captura la actividad. |
| Cualquiera | **Correlación temporal**: cruzar horarios de distintas fuentes ubica al atacante. |

## 5. Nota sobre esta prueba

Durante la ejecución autorizada se utilizó una **VPN (salida en Hong Kong)** como
única capa de ofuscación de origen. Se reconoce que es **insuficiente para un
anonimato real**: no cubre los registros del ISP, la posible retención de logs
del propio VPN, ni la cuenta atacante registrada en el sistema (identidad
directa que ningún VPN oculta).

Dado que se trató de una prueba **autorizada con fines educativos**, el objetivo
fue **generar evidencia**, no evadir la atribución; por eso no se aplicaron el
resto de capas de anonimato. En un escenario real, el atacante combinaría varias
de las técnicas anteriores, y aun así un defensor con **logs centralizados,
monitoreo y captura de memoria** podría reconstruir el incidente.

## 6. Implicancia para la defensa

Esto justifica que la remediación no se limite a bloquear, sino a **detectar y
registrar**: rate-limiting con alertas, logs centralizados e inmutables y
monitoreo de volúmenes anómalos. Si el atacante deja rastro, el defensor debe
poder verlo — la ausencia de esa capacidad es parte de la vulnerabilidad.
