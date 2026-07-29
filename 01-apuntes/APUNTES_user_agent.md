# El User-Agent: cómo lo abusa un atacante y cómo lo caza un forense

> El User-Agent (UA) es un texto que el cliente manda en cada peticion HTTP,
> declarando "quien soy" (navegador, version, sistema). Es texto **controlado
> por el cliente** -> se puede falsear -> y ahi esta todo el juego.

## 1. Qué es y por qué importa

Ejemplo:
```
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64) Chrome/120.0 Safari/537.36
```
El servidor lo usa para: servir contenido segun el dispositivo, estadisticas, y
**detectar bots**. Como lo pone el cliente, no es confiable: es una declaracion,
no una prueba.

## 2. Cómo lo USA/ABUSA un atacante

### a) Mimetizarse (blending)
Poner un UA de navegador normal para parecer trafico legitimo y **no disparar
alertas**. Un scanner con UA vacio o `python-requests/2.31` grita "herramienta";
con UA de Chrome pasa mas desapercibido. (Es lo que le agregamos a nuestro scanner.)

### b) Rotar UAs
Cambiar el UA en cada peticion para **evadir defensas que cuentan por UA** o para
dificultar la correlacion. Un mismo ataque parece venir de muchos clientes.

### c) Suplantar clientes especificos
- Fingir ser **Googlebot** (`Googlebot/2.1`) para saltar paywalls o controles que
  dan acceso libre a buscadores.
- Fingir ser una **app movil** oficial para acceder a APIs internas.

### d) El UA como VECTOR DE ATAQUE (lo mas interesante)
El UA es **input del usuario**. Si el servidor lo guarda/muestra sin sanitizar:
- **Stored XSS**: un UA con `<script>...</script>` que se ejecuta cuando un admin
  abre el panel de logs en el navegador.
- **SQL injection**: si el UA se concatena en una query al guardarlo en la BD.
- **Log poisoning -> RCE**: en apps PHP mal hechas, un UA con codigo PHP se
  escribe en un log que luego se incluye (`include`) y se ejecuta.
> Leccion: cualquier campo que el cliente controla (UA, Referer, headers) es
> input no confiable y hay que validarlo igual que un formulario.

### e) Explotar logica basada en UA
Si la app cambia comportamiento segun UA (ej. menos seguridad para "app movil"),
el atacante elige el UA que le da la version mas debil.

## 3. Cómo lo DETECTA un forense (lado defensivo)

El UA es un rastro que el atacante controla, pero rara vez lo maneja perfecto:

### a) Firmas de herramientas
UAs de herramientas conocidas en los logs: `sqlmap`, `nikto`, `nmap`, `curl`,
`python-requests`, `Nuclei`, o **UA vacio**. Salta al instante.

### b) UA vs comportamiento incoherente
Un UA que dice "Chrome" pero **no pide** CSS, JS ni imagenes como un navegador
real -> es un script disfrazado. El navegador de verdad descarga la pagina entera.

### c) UA vs huella TLS (JA3)
El cliente dice "Chrome" en el UA, pero el **handshake TLS** (huella JA3) es el de
`python`/`curl`. La mentira del UA no cambia como negocia el cifrado -> se delata.
Esta es de las tecnicas mas potentes: el UA se falsea facil, la huella TLS no.

### d) Rotacion sospechosa
Una **misma IP** con **muchos UAs distintos** en poco tiempo = automatizacion.
Un humano no cambia de navegador cada 3 segundos.

### e) UA malformado o con payload
UAs con `<script>`, comillas, `UNION SELECT`, o sintaxis rara = intento de
inyeccion via ese campo. El propio intento queda registrado como evidencia.

### f) Rareza contra la poblacion (baseline)
Se compara el UA contra el trafico normal del sitio. Un UA que aparece en el
0.001% de las peticiones destaca. Lo raro es lo que se investiga.

### g) Correlacion / firma de comportamiento
Un mismo UA (sobre todo si es inusual) que aparece en varios ataques los **liga
entre si**. El atacante que reutiliza su UA arma su propia firma.

## 4. La idea de fondo (las dos mentalidades)

- **Atacante:** el UA es una mascara — la usa para mimetizarse, rotar o inyectar.
- **Forense:** el UA es una confesion — lo compara contra el comportamiento real
  (peticiones, TLS, baseline) y la mascara se cae por incoherencia.

El UA se **falsea** en un segundo; lo que **no** se falsea tan facil es la
coherencia entre lo que decis ser y como realmente te comportas. Ahi vive la
deteccion. Regla: **anonimato de un campo != sigilo del comportamiento completo.**
