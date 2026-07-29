# Guía — Presentar Tor al profe (en privado)

> Presentación individual, no en clase. La divulgación restringida es una
> decisión deliberada: el material tiene doble uso y compartirlo con quien
> corresponde (el docente) en vez de al aire es **divulgación responsable**.

## 0. Cómo enmarcarlo (lo primero que decís)

> "Quise entender Tor a fondo para el lado defensivo: cómo funciona, por qué es
> más fuerte que un VPN y, sobre todo, dónde falla. Se lo muestro en privado
> porque parte de esto tiene doble uso y no me parece responsable divulgarlo
> abiertamente."

Esa frase sola ya comunica madurez técnica **y** ética. Es la mejor apertura.

## 1. Preparación previa (antes de la reunión)

- [ ] Descargar Tor Browser **solo** de `https://www.torproject.org`
      (dirección escrita a mano, no buscada en Google).
- [ ] Verificar la firma GPG de la descarga (ver Anexo A) y tener el resultado
      listo para mostrar — es tu "cadena de custodia" del software.
- [ ] Tener abiertos: los apuntes del repo y esta guía.
- [ ] Probar la demo una vez vos solo, para que salga fluida.

## 2. Guion de la demo (5–7 minutos)

**Paso 1 — Qué es (30 seg).**
Tor = "enrutamiento cebolla". El tráfico pasa por 3 nodos con cifrado en capas;
ningún nodo ve origen y destino a la vez.

**Paso 2 — Mostrar el circuito en vivo (1 min).**
Abrir Tor Browser, entrar a cualquier sitio, y abrir el panel de conexión que
muestra los **3 relays** con sus países. "Miren: entrada, intermedio, salida —
cada uno solo conoce a su vecino."

**Paso 3 — IP antes y después (1 min).**
Mostrar tu IP real en un "what is my IP" con un navegador normal, y luego la IP
de salida (otro país) desde Tor. Efecto visual claro del anonimato de red.

**Paso 4 — Por qué es más fuerte que un VPN (1 min).**
En un VPN, el proveedor ve las dos puntas (tu IP y el destino) y podría loguear.
En Tor, **nadie** tiene la foto completa. La confianza está distribuida.

**Paso 5 — Dónde FALLA (2 min) — la parte que más suma.**
- Nodos de salida vigilados (contenido sin HTTPS es visible).
- No salva del error humano (loguearte a tu cuenta real por Tor te delata).
- Análisis de tráfico por un adversario global.
- Correlación con el mundo físico (cámaras, celular, comportamiento).
Cerrar con: "Tor protege la identidad de red, no el criterio del usuario."

**Paso 6 — Conexión con el deber (1 min).**
"Esto es el lado que un atacante usaría para ofuscar origen en el ataque de
reset. Del lado defensivo, es lo que explica por qué la remediación no es solo
bloquear, sino **detectar y registrar**: aunque el atacante use Tor, deja
patrón en los logs y rastro físico."

## 3. Preguntas que te puede hacer (y respuestas)

- **"¿Es legal usar Tor?"** → Sí. Lo usan periodistas, activistas y gente bajo
  censura. Es una herramienta neutra; el uso define la intención.
- **"¿Por qué no lo presentaste en clase?"** → Doble uso. Preferí divulgación
  responsable: el concepto defensivo es valioso, pero el detalle operativo no
  me parece prudente al aire.
- **"¿Tor te hace irrastreable?"** → No. Rompe el rastro de IP, pero la
  atribución se logra cruzando fragmentos físicos, conductuales y temporales.
  La irrastreabilidad absoluta no existe; solo la práctica, y es frágil.
- **"¿Cómo lo detecto en mi red?"** → Los nodos de entrada/salida de Tor son
  IPs públicas y listadas; se puede alertar sobre conexiones a ellas.

## 4. Qué llevar (checklist del día)

- [ ] Tor Browser instalado y verificado.
- [ ] El repo abierto (apuntes + toolkit del deber).
- [ ] Esta guía y el guion practicado.
- [ ] Una frase de cierre sobre ética (abajo).

## 5. Cierre (lo último que decís)

> "Me interesa la seguridad de verdad, por eso estudié las dos mentalidades: la
> del que ataca para entender el riesgo, y la del que defiende y hace forense
> para contenerlo. Y por eso elijo compartir esto con criterio, no divulgarlo."

---

## Anexo A — Verificar la firma GPG de Tor (opcional, pero impresiona)

La verificación prueba matemáticamente que el archivo bajado no fue alterado —
mismo principio que el hash y la cadena de custodia del forense.

Pasos generales (el sitio oficial tiene la guía exacta y actualizada en
`support.torproject.org` → "How can I verify Tor Browser's signature?"):

1. Instalar GnuPG (en Mac: `brew install gnupg`).
2. Importar la clave firmante del Tor Browser Developers (el ID está en la web
   oficial).
3. Descargar el archivo `.asc` (la firma) que acompaña al instalador.
4. Correr `gpg --verify <archivo.asc> <instalador>`.
5. Si dice **"Good signature"**, el archivo es auténtico e íntegro.

> Mostrarle al profe el "Good signature" en pantalla es un detalle de nivel:
> demuestra que no solo usás la herramienta, sino que verificás su integridad
> como lo haría un profesional.
