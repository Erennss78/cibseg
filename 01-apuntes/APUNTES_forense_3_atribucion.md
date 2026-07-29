# Forense 3 — Atribución (el trabajo detectivesco)

> Cómo se identifica al atacante cruzando fragmentos cuando ninguna pista sola
> alcanza. Es la parte "de película" — pero real.

## 1. El problema de la atribución

Una IP no es una persona. Un VPN/Tor rompe el rastro de red. Entonces, ¿cómo se
llega al humano? **No con una prueba única, sino cruzando muchos fragmentos
débiles** hasta que solo una persona encaja en todos.

Principio: cada fragmento por separado no prueba nada; **la intersección sí**.

## 2. OSINT — inteligencia de fuentes abiertas

Investigar con información **pública**, sin hackear nada:
- Apodos, correos y su reutilización en foros, redes, GitHub, filtraciones viejas.
- Metadata de archivos publicados (autor, GPS en fotos, software usado).
- Huella de comportamiento pública: horarios de actividad, forma de escribir,
  temas recurrentes, zona horaria implícita.

**Así cayó Ross Ulbricht:** un apodo reutilizado ligado a su Gmail real,
encontrado con pura búsqueda pública. OSINT, no un exploit.

## 3. Las capas de atribución

```
Red        -> IP, aunque muera en VPN/Tor da hora y patrón
Física     -> CCTV, ubicación, testigos, tu celular en antenas de la zona
Digital    -> metadata, artefactos del equipo (si se incauta), cuentas
Conductual -> horarios, modismos, reutilización, errores de OPSEC
Temporal   -> cruzar TODAS por la hora exacta del evento
```

La **correlación temporal** es el pegamento: "el ataque fue a las 15:04" se cruza
con "cámara X grabó a esta persona a las 15:03", "su celular estuvo en la zona",
"este apodo posteó minutos después". Solo una persona cae en la intersección.

## 4. Firma de comportamiento (behavioral fingerprinting)

Aunque cambies IP y nombre, tu **manera** de hacer las cosas persiste:
- Cómo escribís (modismos, errores típicos, idioma, puntuación).
- Tus horarios (revelan zona horaria y rutina).
- Herramientas y técnicas favoritas (un atacante repite su "estilo").
- Reutilización inconsciente de nombres, contraseñas, avatares.

Esto es lo más difícil de ocultar porque es **inconsciente y sostenido**.

## 5. Por qué el defensor tiene ventaja (asimetría)

- El atacante debe ser perfecto **siempre y para siempre**.
- El forense necesita **un solo fragmento** que cruce con otro.
- El tiempo juega para el forense: cuanto más opera el atacante, más rastro deja.

Por eso casi nadie cae por "criptografía rota" — cae por **acumulación de
pequeños fragmentos** y un error humano que los conecta.

## 6. Los límites del forense (para ser justos)

La atribución **no es infalible**:
- Un atacante con OPSEC impecable (hardware ajeno, identidad totalmente separada,
  cero reutilización, cero error) puede quedar sin atribuir.
- La correlación puede **acusar a un inocente** (IP compartida, equipo usado por
  varios). Por eso una IP **no basta** para condenar — se exige convergencia de
  evidencia y cadena de custodia.
- La evidencia mal recolectada (sin cadena de custodia) **no vale** en juicio.

## 7. Síntesis del capítulo de forense

| Rama | Aporta | Límite |
|---|---|---|
| Red | cuándo, cuánto, patrón | no ve contenido cifrado ni IP real tras VPN/Tor |
| Disco/Memoria | qué hizo el equipo, archivos "borrados", tokens en RAM | requiere incautar el equipo |
| Atribución | quién, cruzando fragmentos | falla ante OPSEC perfecto; riesgo de falso positivo |

Ninguna rama gana sola. El caso se cierra **combinándolas**: la red da el cuándo,
el disco/RAM da el qué, la atribución da el quién. El arte forense es **tejer los
tres en una sola historia coherente** que resista en un tribunal.
