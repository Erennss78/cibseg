# Herramientas estándar de pentesting (para deberes futuros)

> Caja de herramientas profesional, por fase. Para trabajo real e investigación,
> usar estas en vez de programar scripts a mano: más rápido, más completo, más
> creíble. Los scripts caseros (en esta carpeta) quedan como material de
> aprendizaje / portafolio, no para el trabajo real.
>
> RECORDATORIO LEGAL: todas son de doble uso. Solo contra tu lab, sitios de
> práctica autorizados (ver PRACTICA.md), o sistemas con permiso escrito.

## Instalación rápida (macOS con Homebrew)

```bash
brew install nmap ffuf gobuster nuclei nikto sqlmap hydra john hashcat amass
brew install --cask zap        # OWASP ZAP (proxy web gratis)
# Burp Suite Community: descargar de portswigger.net (gratis)

# whatweb NO está en brew — se instala aparte (Ruby):
git clone --depth 1 https://github.com/urbanadventurer/WhatWeb.git ~/tools/WhatWeb
gem install --user-install addressable
ln -sf ~/tools/WhatWeb/whatweb /opt/homebrew/bin/whatweb   # para llamarlo directo
```

> ⚠️ BUG conocido: whatweb 0.6.4 falla en **HTTPS** con Ruby 4.x
> ("can't modify frozen Hash"). Es incompatibilidad tool-viejo/Ruby-nuevo, no
> un problema del sitio. Alternativas para fingerprint HTTPS (ya instaladas):
>   curl -sI https://TARGET                 # headers rápido
>   nuclei -tags tech -u https://TARGET     # detección de stack (mejor reemplazo)
>   whatweb http://TARGET                   # funciona en HTTP (puede redirigir a HTTPS)

> Estado: las 11 herramientas instaladas y verificadas. SecLists en
> `~/tools/SecLists` (rockyou descomprimido). Tor + proxychains configurados.

## Fase 1 — Reconocimiento / Escaneo

| Herramienta | Para qué | Uso básico |
|---|---|---|
| **nmap** | Puertos y servicios de un host | `nmap -sV objetivo` |
| **masscan** | Escaneo masivo ultrarrápido | `masscan -p1-65535 rango` |
| **ffuf** | Fuerza bruta de rutas/parámetros | `ffuf -u https://sitio/FUZZ -w wordlist.txt` |
| **gobuster** | Descubrir directorios/archivos | `gobuster dir -u https://sitio -w wordlist.txt` |
| **nuclei** | Plantillas de vulns conocidas | `nuclei -u https://sitio` |
| **nikto** | Config insegura de webs | `nikto -h https://sitio` |
| **amass / subfinder** | Descubrir subdominios | `amass enum -d dominio.com` |
| **whatweb** | Fingerprint de tecnología | `whatweb https://sitio` |

> Reemplaza a: `recon_endpoints.py` (ffuf/gobuster hacen lo mismo, más rápido).

## Fase 2 — Análisis / Proxy web

| Herramienta | Para qué |
|---|---|
| **Burp Suite** (Community, gratis) | Interceptar y modificar peticiones HTTP. El estándar web. Repeater (editar y reenviar), Intruder (automatizar), Decoder (analizar tokens). |
| **OWASP ZAP** | Alternativa open source a Burp. |

> Reemplaza a: `analizar_token.py` (el Decoder de Burp) y `checklist_network.md`
> (el Proxy de Burp hace el trabajo del Network tab, con superpoderes).

## Fase 3 — Explotación

| Herramienta | Para qué | Uso básico |
|---|---|---|
| **Metasploit** | Framework de exploits (CVEs listos) | `msfconsole` |
| **sqlmap** | Inyección SQL automática | `sqlmap -u "https://sitio?id=1"` |
| **hydra** | Fuerza bruta de logins/servicios | `hydra -l user -P passlist ssh://host` |
| **john / hashcat** | Crackear hashes de contraseñas | `hashcat -m 0 hashes.txt wordlist.txt` |

> Reemplaza a: `exploit_generico.py` / `exploit_4campos.py` (Burp Intruder o
> Metasploit para casos comunes; código propio solo para lógica única de un
> objetivo).

## Todo junto — distribuciones

- **Kali Linux** / **Parrot OS** — Linux con TODAS estas preinstaladas. La "caja
  de herramientas" lista para usar. Se corre en VM o dual-boot.

## IA (la nueva capa)

- **Shannon** — pentester autónomo white-box (necesita código fuente). ~$50/run.
- **PentestGPT** — asistente que orquesta herramientas.

---

## Flujo típico para un deber de web (rápido y limpio)

1. **Recon:** `whatweb` + `ffuf`/`gobuster` para mapear la app.
2. **Análisis:** abrir **Burp**, navegar la app con el proxy, interceptar el flujo
   vulnerable (ej. reset de contraseña).
3. **Explotar:** con **Burp Repeater/Intruder** modificás y automatizás el ataque.
4. **Confirmar y documentar:** captura del exploit exitoso para el informe.
5. **Código propio SOLO** si el bug es único y ninguna herramienta lo cubre.

## Regla de decisión

- **90% de los casos** → herramienta estándar (rápido, creíble, reproducible).
- **10% (pegamento o lógica única de un objetivo)** → script propio a medida.
- **Nunca** reimplementar desde cero lo que una herramienta probada ya hace.

## Nota académica

Si un deber pide explícitamente **demostrar comprensión programando el exploit**,
ahí sí conviene el código propio (los scripts de esta carpeta). Confirmar con el
docente qué evalúa: comprensión (código propio) o hallazgo (herramienta estándar).
