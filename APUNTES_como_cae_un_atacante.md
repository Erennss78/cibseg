# Cómo cae un atacante — errores de OPSEC y reconstrucción forense

> Apunte de estudio. La mayoría de los grandes hackers NO cayeron porque les
> rompieran la tecnología (VPN/Tor/cripto aguantaron), sino por **errores
> humanos de OPSEC**. El forense solo necesita reconstruir UN fragmento.

## 1. Qué es OPSEC

OPSEC = *Operational Security*: la disciplina de no filtrar datos que te
conecten con la operación. No es una herramienta, es un **hábito sostenido**.
El anonimato es 100% o es 0%: un solo descuido lo tira.

## 2. Casos reales (cómo cayeron)

### Ross Ulbricht — "Dread Pirate Roberts" (Silk Road)
- Montó un mercado ilegal enorme sobre Tor, técnicamente sólido.
- **Error:** meses antes promocionó el sitio en un foro con un apodo que también
  había usado ligado a su **Gmail real**. Un investigador cruzó ambos.
- **Lección:** *el pasado te persigue.* Un post viejo de hace años rompe el
  anonimato del presente.

### Héctor Monsegur — "Sabu" (LulzSec)
- Anonimato impecable por Tor... hasta que entró **una sola vez** a un chat IRC
  **sin Tor**. El FBI capturó su IP real en ese instante.
- **Lección:** *basta un descuido de un segundo.* No existe "casi anónimo".

### Jeremy Hammond (Anonymous)
- **Error:** reutilizó una contraseña de su vida real y mencionó detalles
  personales (su arresto previo, su gato) en chats "anónimos".
- **Lección:** *tu comportamiento te delata* — cómo escribís, horarios, lo que
  contás — no solo tus IPs.

**Patrón común de las 3:** reutilización + un descuido + el pasado.
Nunca fue "les descifraron el cifrado".

## 3. Errores de OPSEC más comunes

- **Reutilizar** apodos, correos, contraseñas entre identidad real y anónima.
- **Un solo lapsus de red** (conectarte sin Tor/VPN una vez).
- **Mezclar sesiones**: abrir tu Gmail/redes en la misma máquina o momento.
- **Firma de comportamiento**: horarios, modismos al escribir, temas personales.
- **Confiar en un parche parcial** (ej. modo avión) sobre un equipo que sigue
  siendo tuyo.
- **Metadata olvidada**: fotos con GPS, documentos con autor, telemetría del SO.

## 4. Por qué "modo avión + solo la terminal" no alcanza

| Creencia | Realidad |
|---|---|
| "El teléfono en avión no me ubica" | Tu cuerpo está físicamente ahí: cámaras, testigos. El celular ya registró antenas de la zona antes/después. |
| "Solo abrí el script y la terminal" | El SO habla solo por detrás: telemetría, updates, sincronizaciones, todo con IDs de tu equipo. |
| "No abrí nada personal" | La máquina es **tuya**: disco, MAC, número de serie la conectan con vos si cae en forense. |

El anonimato no se logra *cerrando apps*, sino con **separación total**:
hardware ajeno + red ajena + identidad ajena, sostenido sin un cruce.

## 5. Cómo el forense reconstruye (la asimetría)

El atacante debe hacer **todo** perfecto, siempre. El forense necesita **un**
fragmento. La ventaja es del defensor.

Ejemplo de cadena de reconstrucción cuando la red no ayuda:

```
IP del ataque -> muere en el VPN (callejón sin salida por red)
      |
      +-- cruce por HORARIO con cámaras CCTV del lugar
      +-- metadata del CELULAR en antenas de la zona a esa hora
      +-- apodo/correo REUTILIZADO en algún lado
      +-- patrón de COMPORTAMIENTO (horarios, forma de escribir)
      =
   fragmentos sueltos -> convergen en UNA persona
```

**Orden de volatilidad** (qué capturar primero, de más frágil a más durable):
RAM y conexiones activas → discos → logs del servidor → backups → registros del
ISP. Lo volátil se recoge primero porque desaparece al apagar.

## 6. Las dos mentalidades

- **Atacante:** "¿cómo lo hago perfecto?" — entrena el ojo para ver debilidades.
- **Forense:** "¿qué fragmento dejó?" — usa ese mismo ojo para cazar el error.

Pensar como atacante te hace **mejor** forense: sabés dónde suele estar el fallo.

---

## Anexo: ¿Qué es Tor?

**Tor** (*The Onion Router*, "enrutamiento cebolla") es una red de anonimato.

**Cómo funciona:** tu tráfico no va directo al destino; pasa por **3 nodos**
elegidos al azar y cifrados en capas (como una cebolla):

```
Vos -> [Nodo de entrada] -> [Nodo intermedio] -> [Nodo de salida] -> Destino
        conoce tu IP          no conoce ninguna    conoce el destino
        pero no el destino    de las dos puntas    pero no tu IP
```

- Cada nodo pela **una capa** de cifrado y solo sabe de dónde vino y a dónde
  mandar el siguiente salto. **Ningún nodo ve origen Y destino a la vez.**
- Por eso es más anónimo que un VPN: en un VPN, el proveedor ve las dos puntas
  (tu IP y el destino) y podría loguearlas. En Tor, ningún actor tiene la foto
  completa.

**Diferencia rápida VPN vs Tor:**

| | VPN | Tor |
|---|---|---|
| Saltos | 1 (el servidor VPN) | 3 nodos |
| Quién ve las 2 puntas | El proveedor de VPN | Nadie |
| Confianza | Confiás en el VPN | Distribuida entre nodos |
| Velocidad | Rápido | Más lento (3 saltos) |

**Límites de Tor** (por qué no es magia):
- Los **nodos de salida** están vigilados; ven el tráfico que sale (si no va
  cifrado con HTTPS, lo leen).
- **Análisis de tráfico**: correlacionar el timing/volumen de entrada y salida
  puede desanonimizar con recursos suficientes.
- **No protege del error humano**: si te logueás a tu cuenta real por Tor, Tor
  no te salva (así cayó gente que "usaba Tor").

**Usos legítimos:** periodistas, activistas, gente bajo censura, o simplemente
privacidad. Tor no es ilegal — es una herramienta; el uso define la intención.

### Configuración de Tor: qué sirve y qué te delata

- **Nivel de seguridad del navegador (escudo):** Standard / Safer / Safest.
  Subirlo desactiva JavaScript (vía común de desanonimización). *Sirve* — muchos
  ataques reales a usuarios de Tor fueron por JS, no por romper Tor.
- **Bridges (puentes):** nodos de entrada no listados, para *entrar* a Tor donde
  está bloqueado. No dan más anonimato, solo evitan la censura.
- **Pluggable transports (obfs4, meek, snowflake):** disfrazan el tráfico para
  que **no parezca Tor**. Camuflaje de la conexión, no anonimato extra.
- **torrc (avanzado):** archivo de config; forzar países de salida, puertos, etc.

**Regla clave:** casi ninguna personalización te hace *más* anónimo, y varias te
hacen **menos**. Si agregás extensiones, maximizás la ventana o cambiás fuentes,
te volvés **único** → más rastreable por *fingerprinting*. La gracia de Tor es que
todos los usuarios se vean **iguales**; tunearlo rompe eso. El default es el óptimo.

> Sabu (LulzSec) no cayó por config: su Tor funcionaba. Cayó porque entró **una
> vez sin Tor**. Ninguna configuración salva de un error humano.

### Cómo un atacante *opera* Tor (y sus fugas)

Dos formas de usarlo:
1. **Tor Browser** — protege solo lo que pasa por esa ventana.
2. **Tor como proxy SOCKS** (`127.0.0.1:9050`) — rutea el tráfico de **cualquier**
   programa. Es lo que usa un atacante para que su herramienta salga por Tor.
   Se hace con envoltorios externos: **proxychains** o **torsocks**
   (`proxychains python3 herramienta.py`). A veces encadenan **VPN → Tor**.

**Fugas frecuentes (por qué "usar Tor" mal no alcanza):**
- **DNS leak:** si el programa resuelve el dominio *fuera* de Tor, el ISP ve a
  qué sitio ibas aunque el tráfico vaya por Tor. Por eso se usa torsocks/proxychains
  bien configurado, que fuerza también el DNS por Tor.
- **Contenido sin HTTPS:** el nodo de salida lo lee. Nunca datos sensibles sin HTTPS.
- **Correlación temporal:** un adversario global cruza entrada y salida por el
  timing. Caro (nivel Estado), pero real.
- **Usar Tor deja huella:** los nodos de salida son IPs **públicas y listadas**;
  un defensor detecta "esto viene de Tor" aunque no sepa quién. Anonimato ≠ sigilo.

**Idea de fondo:** Tor es el **sobre**, no el ataque. El exploit es el mismo; Tor
solo cambia el remitente. Por eso el defensor no intenta romper Tor (inútil):
detecta el **patrón del ataque** en los logs y correlaciona con el mundo físico,
que Tor no toca.
