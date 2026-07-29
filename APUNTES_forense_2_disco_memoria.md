# Forense 2 — Forense de disco y memoria

> Analizar un equipo secuestrado: qué se recupera del disco y de la RAM.

## 1. La regla de oro: orden de volatilidad

Se captura lo más **frágil primero**, porque desaparece más rápido:

```
RAM y conexiones activas   <- se pierde al apagar (MÁS volátil)
     |
procesos en ejecución
     |
disco / archivos
     |
backups
     |
registros del ISP          <- dura meses (MENOS volátil)
```

Por eso un forense, ante un equipo **encendido**, primero hace un **volcado de
RAM** y recién después lo apaga. Apagar de una destruye evidencia.

## 2. Forense de MEMORIA (RAM)

La RAM contiene lo que el disco no: el estado **vivo** del sistema.

**Qué se recupera de un volcado de RAM:**
- **Contraseñas y tokens en texto plano** — muchas apps los tienen en memoria
  aunque en disco estén cifrados (¡incluido el `TOKENS` de nuestra app!).
- **Procesos en ejecución**, incluso malware "fileless" que nunca tocó el disco.
- **Conexiones de red activas** (a qué IPs estaba conectado).
- **Claves de cifrado** de discos montados → permite abrir el disco cifrado.
- Fragmentos de chats, comandos escritos, portapapeles.

**Herramientas:** Volatility (el estándar), Rekall, para analizar el volcado;
la captura se hace con herramientas que leen `/dev/mem` o equivalentes.

**Por qué importa para el atacante:** la técnica "operar solo en RAM" evita el
disco, pero **un volcado en caliente lo captura igual**. La RAM no es invisible
si el equipo se agarra encendido.

## 3. Forense de DISCO

El disco guarda lo persistente, incluso lo que "borraste".

**Conceptos clave:**
- **Borrar ≠ eliminar.** Al borrar un archivo, el sistema solo marca el espacio
  como "libre"; los datos siguen ahí hasta que se sobrescriben. Se **recuperan**
  con herramientas de *file carving*.
- **Espacio no asignado (unallocated space)** — donde viven los archivos borrados.
- **Slack space** — restos de archivos viejos en bloques parcialmente usados.
- **Metadata del sistema de archivos** — fechas de creación/acceso/modificación
  (MAC times), que arman la **línea de tiempo**.
- **Artefactos del SO:** historial del navegador, caché, registro de Windows,
  logs, papelera, archivos recientes, prefetch (qué programas se ejecutaron).

**Herramientas:** Autopsy / The Sleuth Kit (gratis), FTK, EnCase (comerciales),
`dd` para clonar el disco bit a bit.

## 4. Integridad: la cadena de custodia

La evidencia solo sirve si se puede probar que **no fue alterada**:
- Se trabaja sobre una **copia bit a bit** (imagen forense), nunca el original.
- Se calcula un **hash (SHA-256)** de la imagen al copiarla; si el hash coincide
  después, se prueba que no cambió nada.
- Se documenta **quién** tuvo la evidencia, **cuándo** y **por qué** (cadena de
  custodia). Sin esto, no sirve en un juicio.

## 5. Timestomping y sus límites

El atacante puede falsear las fechas de un archivo (**timestomping**), pero:
- El sistema de archivos guarda fechas en **dos lugares** (ej. NTFS: `$STANDARD_INFO`
  y `$FILE_NAME`); alterar uno y no el otro **delata** la manipulación.
- Los logs y la metadata de otros artefactos suelen **contradecir** la fecha
  falseada. La inconsistencia misma es una pista.

## 6. Idea de fondo

El disco y la RAM son **confesiones**: guardan mucho más de lo que el usuario
cree, y "borrar" rara vez borra de verdad. El atacante que asume "lo borré, no
existe" subestima cuánto persiste — igual que subestima cuánto grita en los logs.
