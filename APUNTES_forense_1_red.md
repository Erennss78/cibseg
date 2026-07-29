# Forense 1 — Forense de red

> Reconstruir un ataque a partir del tráfico y los registros de red.
> Conecta directo con el deber: cómo el defensor HABRÍA visto tu ataque de reset.

## 1. Qué es

El forense de red analiza **lo que viajó por la red** para reconstruir qué pasó:
quién habló con quién, cuándo, cuánto y (si no iba cifrado) qué se dijo. Sus dos
fuentes principales son los **logs** y las **capturas de tráfico (PCAP)**.

## 2. Fuentes de evidencia

| Fuente | Qué contiene |
|---|---|
| **Logs del servidor web** | Cada request: IP, hora, método, URL, user-agent, código de respuesta. |
| **Logs de firewall / router** | Conexiones permitidas/bloqueadas, IPs origen-destino, puertos. |
| **PCAP (captura de paquetes)** | El tráfico crudo. Con tcpdump / Wireshark. |
| **Logs de la aplicación** | Eventos de negocio: "se pidió reset", "se cambió password". |
| **NetFlow** | Metadata de flujos (quién-con-quién-cuánto) sin el contenido. |

## 3. Cómo se habría visto TU ataque de reset

Tu exploit generó un patrón muy reconocible. Un defensor mirando los logs vería:

```
15:04:01  IP_atacante  POST /reset/pedir      email=atacante@...   200
15:04:01  IP_atacante  POST /reset/pedir      email=victima@...     200
15:04:02  IP_atacante  POST /reset/confirmar  token=709322          400
15:04:02  IP_atacante  POST /reset/confirmar  token=709323          400
15:04:02  IP_atacante  POST /reset/confirmar  token=709324          200  <-- acertó
...cientos de POST a /reset/confirmar desde la MISMA IP en segundos...
```

**Señales de alarma (IoC — Indicators of Compromise):**
- **Volumen anómalo**: cientos de intentos a `/reset/confirmar` en segundos.
- **Muchos 400 seguidos de un 200**: patrón clásico de fuerza bruta exitosa.
- **Dos resets casi simultáneos** (atacante + víctima): huella del ataque de predicción.
- **Una sola IP** tocando muchas cuentas.

> Moraleja para la defensa: el ataque **grita** en los logs. Lo que faltaba en el
> sistema vulnerable no era ocultarlo, sino **mirarlo** (monitoreo + alertas).

## 4. Herramientas típicas

- **Wireshark** — abrir y analizar PCAP con interfaz gráfica (filtros, follow stream).
- **tcpdump** — capturar tráfico desde la terminal.
- **Zeek (antes Bro)** — convierte tráfico en logs estructurados de alto nivel.
- **grep / awk** sobre logs de texto — el 80% del trabajo real es esto.
- **SIEM** (Splunk, ELK, Wazuh) — centraliza logs de muchas fuentes y alerta.

## 5. Qué revela y qué NO

**Revela:** IPs, horarios, volúmenes, patrones, y contenido **si no iba cifrado**.

**NO revela (limitaciones):**
- **HTTPS cifra el contenido** — el forense ve QUE hablaste con el servidor y
  cuánto, pero no el cuerpo del request. Ve metadata, no el mensaje.
- **VPN/Tor** rompen el "quién" a nivel IP: la IP registrada es la del VPN/nodo
  de salida, no la del atacante.
- Por eso el forense de red **casi nunca cierra el caso solo** — aporta el
  "cuándo y cuánto", y se **cruza** con forense de disco/memoria y atribución.

## 6. El concepto clave: correlación

El poder no está en un log, sino en **cruzar varios**:
`log del servidor (hora del ataque)` + `log del firewall (IP y puerto)` +
`NetFlow (volumen)` → una línea de tiempo coherente. La correlación temporal es
la herramienta más fuerte del forense de red.

## 7. Defensa que habilita el forense

Para que todo esto sea posible, el sistema tiene que estar preparado ANTES:
- **Logs centralizados e inmutables** (que el atacante no pueda borrar).
- **Retención suficiente** (semanas/meses).
- **Sincronización horaria (NTP)** — sin relojes iguales, no hay correlación.
- **Monitoreo con alertas** sobre los IoC del punto 3.
