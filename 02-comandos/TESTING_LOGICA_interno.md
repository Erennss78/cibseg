# Testing de lógica interna — encontrar los bugs que los scanners NO ven

> Guía para probar la seguridad PROFUNDA de mis apps (avisaras/Eventshow, distries).
> Los scanners (nuclei, nikto, sqlmap, hydra) encuentran la capa fácil
> (vulns conocidas, config). Los bugs REALES de apps modernas son de LÓGICA y
> AUTORIZACIÓN — solo los encuentra un humano logueado probando "¿qué pasa si...?".
>
> Ventaja: son MIS apps, tengo el código → puedo hacer whitebox (leer dónde falta
> el chequeo) además de black-box (probar a mano).

## La mentalidad (esto es todo)

- Un scanner pregunta: "¿tiene esta app una vulnerabilidad conocida?"
- Yo pregunto: "¿confía esta app en algo que el usuario controla, sin verificarlo?"

Cada vez que la app confía en un dato del cliente (un ID, un precio, un rol, un
"ya pagué") SIN validarlo del lado del servidor → ahí hay un bug potencial.

## Las 4 categorías + las preguntas "¿qué pasa si...?"

### 1. IDOR — "¿puedo ver/tocar cosas de OTRO usuario?" (el más común)
Preguntas:
- Logueado como A, ¿puedo acceder a `/api/reservations/6` que es de B, cambiando el ID?
- ¿Puedo editar/borrar un recurso de otro cambiando su ID en la petición?
- ¿Los IDs son secuenciales (1,2,3...) y adivinables?

Cómo probar: crear 2 cuentas (A y B). Desde A, intentar acceder a recursos de B
cambiando el ID en Burp Repeater.

### 2. Autorización / escalada — "¿puedo hacer cosas de admin siendo normal?"
Preguntas:
- Logueado como usuario normal, ¿puedo llamar `/api/admin/...` o rutas de otro rol?
- ¿Puedo cambiar mi propio rol en una petición de "editar perfil"?
- ¿Un endpoint sensible chequea el ROL, o solo que esté logueado?

### 3. Lógica de negocio — "¿puedo romper las reglas?"
Preguntas:
- ¿Puedo poner cantidad/precio NEGATIVO y que me acredite plata?
- ¿Puedo saltar el paso de pago yendo directo a la URL de "confirmado"?
- ¿Puedo usar un cupón/beneficio dos veces (doble submit, condición de carrera)?
- ¿Puedo reservar algo lleno, con fecha pasada, o fuera de las reglas?

### 4. Manipulación de parámetros — "¿qué pasa si mando algo inesperado?"
Preguntas:
- El campo espera número → mando texto, negativo, o enorme. ¿Rompe o valida?
- El precio/total viene del cliente → lo cambio a 0.01. ¿Lo acepta?
- Mi userId va en la petición → lo cambio por el de otro. ¿Confía en él?

## Método WHITEBOX (más fácil — tengo el código)

Buscar endpoints que usan un ID/input pero quizá NO validan dueño o rol:

```bash
# Eventshow (Next.js):
grep -rn "params.id\|params\.\|searchParams\|req.body" ~/Documents/Eventshow/web/src/app/api/

# distries (Express/Prisma):
grep -rn "req.params\|req.query\|req.body" ~/Documents/distries/backend/src/controllers/

# buscar queries que NO incluyen el user.id (candidatas a IDOR):
grep -rn "findUnique\|findFirst\|delete\|update" ~/Documents/distries/backend/src/ | grep -v "user"
```

Por cada resultado, preguntarse: **"¿este endpoint verifica que el recurso sea
del usuario logueado (pasa user.id al where), o solo lo busca por ID?"**
- Pasa user.id / chequea rol → seguro (ej: `cancelar(id, user.id)` ✓)
- Solo busca por ID sin dueño → IDOR potencial → validar a mano

## Método BLACK-BOX (más realista — con Burp)

1. Levantar la app en LOCAL (nunca fuerza bruta/manipulación en producción).
2. Crear 2 cuentas de prueba (A y B) + una admin si hay roles.
3. Abrir Burp → Proxy → Open Browser. Navegar logueado como A.
4. Por cada acción (ver reserva, editar perfil, pagar), capturar la petición.
5. En Repeater: modificar (cambiar ID a uno de B, cambiar precio, cambiar rol) y
   reenviar. Ver la respuesta.
6. Si accedo a algo que no debería → BUG. Documentar con PoC (Fase 3.5).

## Regla de oro (igual que siempre)

- Solo en MIS apps o autorizado. Lo destructivo (fuerza bruta, manipulación) → LOCAL.
- Nada es "bug" hasta reproducirlo yo con una PoC.
- Validar el mínimo para probar impacto, sin dañar datos.

## Checklist rápido para una sesión de testing

- [ ] ¿IDs adivinables? ¿puedo cambiarlos y acceder a datos ajenos? (IDOR)
- [ ] ¿Endpoints sensibles chequean ROL, no solo login? (AuthZ)
- [ ] ¿El servidor confía en precios/totales/roles que manda el cliente?
- [ ] ¿Puedo saltar pasos de un flujo (pago, verificación)?
- [ ] ¿Valores negativos/enormes/tipos raros rompen la lógica?
- [ ] ¿Puedo repetir acciones que deberían ser únicas? (cupones, votos)
- [ ] Whitebox: ¿hay queries por ID sin user.id en el where?
