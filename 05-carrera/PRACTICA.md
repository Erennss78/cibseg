# Sitios legales para practicar (hechos para ser atacados)

> Todos estos existen **para** que practiques ataques. El permiso ya está dado
> por diseño. Aun así, leé los términos de cada uno. Nunca apuntes tus scripts
> a nada fuera de esta lista, tu lab local, o un sistema con permiso escrito.

## Para tu tema (reset de contraseña / autenticación) — EMPEZAR AQUÍ

- **PortSwigger Web Security Academy** — https://portswigger.net/web-security
  Gratis. El mejor recurso web. Tiene labs específicos de **Authentication** y
  **password reset**. Es exactamente tu tema. Arrancá por acá.

## Apps web vulnerables a propósito

- **OWASP Juice Shop** — https://owasp.org/www-project-juice-shop/
  App moderna deliberadamente vulnerable. Corre local o online. Todo el OWASP Top 10.
- **DVWA** (Damn Vulnerable Web Application) — https://github.com/digininja/DVWA
- **OWASP WebGoat** — https://owasp.org/www-project-webgoat/
- **bWAPP** — http://www.itsecgames.org/

## ⭐ Lab recomendado: Juice Shop en local (para correr el cheatsheet en orden)

El mejor campo para practicar TODO el CHEATSHEET_pentest.md contra un objetivo
que SÍ tiene bugs. Se levanta en un comando (necesita Docker):

```bash
# 1. Levantar (puerto 3001 para no chocar con otras apps):
docker run -d -p 3001:3000 bkimminich/juice-shop

# 2. Esperar ~30s y verificar:
curl -s -o /dev/null -w "Juice Shop → HTTP:%{http_code}\n" http://localhost:3001
# abrir http://localhost:3001 en el navegador

# 3. Para parar/borrar cuando termines:
docker ps                       # ver el id del contenedor
docker stop <id> && docker rm <id>
```

### Correr el cheatsheet EN ORDEN contra Juice Shop (TARGET = localhost:3001)

```bash
# FASE 1 — Recon
curl -sI http://localhost:3001
whatweb http://localhost:3001                     # http, sin el bug de HTTPS

# FASE 2 — Descubrir rutas (acá SÍ encuentra cosas):
ffuf -u http://localhost:3001/FUZZ -c -mc 200,301,403 \
  -w ~/tools/SecLists/Discovery/Web-Content/common.txt
nuclei -u http://localhost:3001                   # vulns conocidas
nikto -h http://localhost:3001

# FASE 4 — Explotar (ejemplos reales que funcionan en Juice Shop):
# a) SQLi bypass de login → en el form de login probar usuario:  ' OR 1=1--
# b) SQLi automática con sqlmap en la búsqueda de productos:
sqlmap -u "http://localhost:3001/rest/products/search?q=test" --batch --dbs
```

> Contraste clave: los MISMOS comandos que contra tu app (avisaras) no soltaron
> nada, contra Juice Shop revientan todo. La diferencia es que una está bien hecha
> y la otra rota A PROPÓSITO. Así aprendés a reconocer cómo se ve un bug real.

## Sitios de prueba públicos (para escáneres/exploits)

- **testphp.vulnweb.com** — http://testphp.vulnweb.com  (Acunetix, PHP)
- **testasp.vulnweb.com** / **testaspnet.vulnweb.com**  (ASP)
- **scanme.nmap.org** — http://scanme.nmap.org
  El propio Nmap lo hostea para practicar escaneo legalmente.

## Máquinas completas (sistemas enteros para vulnerar)

- **TryHackMe** — https://tryhackme.com  (el más amigable para empezar, guiado)
- **Hack The Box** — https://www.hackthebox.com  (más difícil, tipo CTF)
- **VulnHub** — https://www.vulnhub.com
  Descargás VMs vulnerables y las atacás en tu red local. 100% offline.

## CTFs (competencias)

- **picoCTF** — https://picoctf.org  (hecho para estudiantes, gratis)
- **CTFtime** — https://ctftime.org  (calendario de competencias abiertas)

---

## Cómo probar TUS herramientas acá

**Scanner (`recon_endpoints.py`):**
```python
BASE = "http://testphp.vulnweb.com"   # o scanme.nmap.org
```
Corré `python3 recon_endpoints.py`. Ves fingerprint + rutas encontradas.

**Exploits (`exploit_generico.py`, `exploit_4campos.py`):**
Los labs de **PortSwigger Authentication** te dan un objetivo con URL propia y
credenciales de práctica. Ahí ajustás `BASE` y los campos, y probás el ataque
en un entorno donde está permitido.

**Analizador de tokens (`analizar_token.py`):**
No manda tráfico — funciona con cualquier token que capturés legítimamente de
tus cuentas de práctica.

> Recordá: cambiar `BASE` es lo único que decide el objetivo. Antes de correr
> cualquier script activo, confirmá que apunta a un sitio de esta lista, a tu
> localhost, o a un sistema autorizado.
