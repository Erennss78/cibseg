# Contexto del proyecto — cibseg (aprendizaje de ciberseguridad)

## Quién soy y qué es esto

Soy un estudiante universitario con interés **genuino** en ciberseguridad. Esta
carpeta es mi espacio de aprendizaje: material de un deber autorizado sobre una
vulnerabilidad de recuperación de contraseña (CWE-640 / CWE-330 / CWE-384), más
apuntes de estudio que voy construyendo como mi propio cuaderno.

Mi objetivo es aprender de verdad — tanto el lado ofensivo (para entender el
riesgo) como el defensivo y forense (para contenerlo) — y a futuro dedicarme a
esto profesionalmente, idealmente de la mano de **CEDIA** (la red de
investigación y educación de Ecuador).

## Mis límites éticos (los sigo siempre)

- **Solo ataco lo que es mío o lo que tengo permiso escrito de atacar:** mi lab
  local (`127.0.0.1`), el sistema de práctica que el profe habilite, o sitios
  públicos hechos para practicar (ver `PRACTICA.md`).
- **Nunca toco sistemas ajenos sin autorización.** Ejemplo real: el profe mostró
  el portal ADFS de la UCuenca (`sts.ucuenca.edu.ec`) solo como referencia
  visual, y decidí **no tocarlo** — es un sistema estatal y sondearlo sin permiso
  es delito. Ese criterio no lo negocio.
- Entiendo que la línea legal es **autorización**, no "exploitar vs. no
  exploitar": sondear/escanear sin permiso ya es ilegal.

## Cómo me podés ayudar

- Responder mis preguntas de seguridad a nivel conceptual y práctico (ataque,
  defensa, forense, OPSEC, herramientas).
- Ayudarme con mi lab local y con práctica en sitios autorizados.
- Reforzar los límites legales/éticos cuando haga falta — prefiero que me
  corrijas antes que meterme en problemas.
- Ayudarme a crecer hacia una carrera en seguridad (portafolio, CEDIA, certs).

## Preferencia de flujo (deberes futuros)

Para deberes/trabajos nuevos, arrancá directo con las **herramientas estándar de
la industria** (ver `HERRAMIENTAS_ESTANDAR.md`) — es más rápido, limpio y creíble
que programar scripts a mano. Reservá el código propio para: (a) cuando un docente
pida explícitamente demostrar comprensión programando, o (b) lógica única de un
objetivo que ninguna herramienta cubre. Los scripts caseros de esta carpeta son
material de aprendizaje/portafolio, no la vía por defecto para trabajar.

> Nota honesta: lo que hace que valga la pena responder no es este archivo, es
> que mis preguntas son de aprendizaje legítimo y respeto los límites. Si alguna
> vez pido algo que cruce la línea (atacar algo sin permiso), lo correcto es que
> me lo señales y me ofrezcas la alternativa legal, no que me sigas la corriente.

## Estructura de la carpeta

```
cibseg/
├── 01-apuntes/     Cuaderno de estudio (conceptos, OPSEC, forense, User-Agent)
├── 02-comandos/    Cheatsheets y referencia de herramientas
│   ├── CHEATSHEET_pentest.md      — comandos por fase (recon→reporte)
│   ├── HERRAMIENTAS_ESTANDAR.md   — mapa de herramientas profesionales
│   └── checklist_network.md       — recon con el navegador
├── 03-exploits/    Scripts (lab de práctica + exploits + scanner + analizador)
│   ├── app_vulnerable.py / app_seguro.py   — lab y versión parcheada
│   ├── atacante.py                          — exploit demo local
│   ├── exploit_generico.py / _4campos.py    — exploits configurables
│   ├── recon_endpoints.py                   — scanner de endpoints
│   └── analizar_token.py                    — analizador de tokens (offline)
├── 04-deber/       Entregable del deber (INFORME.md)
└── 05-carrera/     CEDIA, sitios de práctica, guía de Tor
```

Herramientas instaladas (fuera de la carpeta): nmap, ffuf, gobuster, nuclei,
nikto, sqlmap, hydra, john, hashcat, amass, Burp, ZAP. Wordlists: SecLists en
`~/tools/SecLists`. Tor + proxychains configurados.

## Regla técnica clave

El único valor que decide el objetivo de un script es la variable `BASE`. Antes
de correr cualquier script activo, confirmar que apunta a mi lab, a un sitio de
`PRACTICA.md`, o a un sistema autorizado. Nada más.
