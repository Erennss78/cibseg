# cibseg — Cuaderno de ciberseguridad

Espacio de aprendizaje: deber de reset de contraseña + apuntes de estudio +
referencia de herramientas + material de carrera.

> ⚠️ Todo el material es para uso educativo contra sistemas **autorizados**:
> tu lab local, sitios de práctica (ver `05-carrera/PRACTICA.md`), o sistemas
> con permiso escrito. Ver `CLAUDE.md` para el contexto y los límites.

## Estructura

| Carpeta | Contenido |
|---|---|
| **01-apuntes/** | Cuaderno de estudio: conceptos, cómo cae un atacante (OPSEC/Tor), forense (red, disco/memoria, atribución), User-Agent, modus operandi. |
| **02-comandos/** | `CHEATSHEET_pentest.md` (comandos por fase), `HERRAMIENTAS_ESTANDAR.md` (mapa de herramientas), `checklist_network.md`. |
| **03-exploits/** | Lab (`app_vulnerable.py`/`app_seguro.py`), exploits (`atacante.py`, `exploit_generico.py`, `exploit_4campos.py`), scanner (`recon_endpoints.py`), analizador (`analizar_token.py`). |
| **04-deber/** | `INFORME.md` — el entregable del deber. |
| **05-carrera/** | `CEDIA_aplicar.md`, `PRACTICA.md` (sitios legales), `GUIA_presentar_tor_al_profe.md`. |

## Práctica rápida del deber (lab local)

Dos terminales en `03-exploits/`:
```bash
python3 app_vulnerable.py     # terminal 1 — levanta el sistema vulnerable
python3 atacante.py           # terminal 2 — lanza el ataque (takeover)
```

## Herramientas profesionales (instaladas en el sistema)

nmap · ffuf · gobuster · nuclei · nikto · sqlmap · hydra · john · hashcat ·
amass · Burp · ZAP. Wordlists: **SecLists** en `~/tools/SecLists`. Anonimato:
**Tor + proxychains** configurados. Ver `02-comandos/CHEATSHEET_pentest.md`.

## Por dónde seguir

- **Practicar:** labs de `05-carrera/PRACTICA.md` (empezar por PortSwigger Auth).
- **Carrera:** `05-carrera/CEDIA_aplicar.md`.
- **Referencia de trabajo:** `02-comandos/CHEATSHEET_pentest.md`.
