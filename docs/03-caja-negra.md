# Parte 3 · Diseño de casos de caja negra

**Estudiante:** Elkin Eliecer Aguas Giraldo · **Código:** 0182410020

## Qué es la caja negra y cómo la voy a usar

Probar por **caja negra** es probar la función **sin mirar su código**. Solo uso lo que dice la
especificación: le entrego unos datos, miro qué devuelve y lo comparo con lo que *debería* devolver
según las reglas.

El problema es que hay infinitos datos posibles. Para escoger bien cuáles probar uso tres técnicas:

1. **Particiones de equivalencia:** agrupar los datos en familias que la función trata igual y probar una de cada familia.
2. **Valores límite:** probar justo en los bordes, donde las reglas cambian, porque ahí se esconden los errores.
3. **Tabla de decisión:** probar todas las combinaciones de varias condiciones que se juntan.

Los resultados esperados los calculé a mano con la especificación y los verifiqué con un segundo
cálculo exacto. Ninguno salió de la función `calc`.

**Mis reglas, para tenerlas a la vista:** el 3 kg cuenta como tramo 1 (D par) · el recargo de fin de
semana va antes de los descuentos (E par) · el cliente y el cupón se aplican los dos, el del cliente
primero (B impar) · un cupón que no existe se ignora (F par).

## 3.1 Particiones de equivalencia: agrupar para no probar todo

No puedo probar todos los pesos del mundo. Pero un peso de 4 kg y uno de 7 kg deberían tratarse
igual, porque los dos caen en el tramo 2. Entonces separo cada dato en **familias** y pruebo al menos
un ejemplo de cada una, tanto de las válidas como de las inválidas.

**Peso**

| Familia | Qué incluye | ¿Válida? | Ejemplo | Caso |
|---------|-------------|:--------:|---------|------|
| P1 | Cero o negativo | No | 0 y −5 | TC-01, TC-02 |
| P2 | Tramo 1: más de 0 y hasta 3 kg | Sí | 2,9 y 3 | TC-04, TC-05 |
| P3 | Tramo 2: más de 3 y hasta 10 kg | Sí | 5 y 10 | TC-20, TC-07 |
| P4 | Tramo 3: más de 10 y hasta 50 kg | Sí | 10,5 · 12 · 20 | TC-09, TC-35, TC-36 |
| P5 | Más de 50 kg | No | 50,1 | TC-11 |

**Zona**

| Familia | Qué incluye | ¿Válida? | Caso |
|---------|-------------|:--------:|------|
| Z1 | Urbana | Sí | TC-20 |
| Z2 | Rural | Sí  | TC-12 |
| Z3 | Nacional | Sí | TC-13 |
| Z4 | Cualquier otra | No | TC-14 |

**Cliente**

| Familia | Qué incluye | ¿Válida? | Caso |
|---------|-------------|:--------:|------|
| C1 | Normal | Sí  | TC-20 |
| C2 | Frecuente | Sí | TC-22 |
| C3 | VIP | Sí | TC-24 |

Un tipo de cliente que no sea ninguno de estos tres no se prueba (supuesto S-1).

**Día**

| Familia | Qué incluye | ¿Válida? | Ejemplo | Caso |
|---------|-------------|:--------:|---------|------|
| D1 | Lunes a viernes (1 a 5) | Sí | 3 y 5 | TC-20, TC-15 |
| D2 | Sábado y domingo (6 y 7) | Sí | 6 y 7 | TC-16, TC-17 |
| D3 | Menor que 1 | No | 0 | TC-18 |
| D4 | Mayor que 7 | No | 8 | TC-19 |

**Cupón**

| Familia | Qué incluye | ¿Válida? | Ejemplo | Caso |
|---------|-------------|:--------:|---------|------|
| K1 | Sin cupón | Sí | ninguno | TC-20 |
| K2 | El cupón ENVIO10 | Sí | ENVIO10 | TC-21 |
| K3 | Un cupón que no existe | Sí, se ignora | PROMO50 | TC-32 |

**Resultado**

| Familia | Qué incluye | Ejemplo | Caso |
|---------|-------------|---------|------|
| O1 | El cálculo da menos del mínimo | 3 kg, VIP, ENVIO10 (daría $4.590) | TC-33 |
| O2 | El redondeo sube (resto de 50 o más) | 8.550 → 8.600 | TC-22 |
| O3 | El redondeo baja (resto menor de 50) | 9.405 → 9.400 | TC-29 |

## 3.2 Valores límite: los errores se esconden en los bordes

Los programadores se equivocan sobre todo en los bordes: un `<` en vez de un `<=`, y el límite queda
en el tramo equivocado. Por eso pruebo **cada borde con tres valores**: uno justo debajo, uno
exactamente en el borde y uno justo encima.

En el peso hay cuatro bordes: **0, 3, 10 y 50**.

| Borde | Qué cambia ahí | Justo debajo | En el borde | Justo encima |
|-------|----------------|--------------|-------------|--------------|
| **0** | Empiezan los pesos válidos | −0,1 → error (TC-40) | 0 → error (TC-01) | 0,1 → $6.000 (TC-03) |
| **3** | Termina el tramo 1 | 2,9 → $6.000 (TC-04) | 3 → **$6.000** (TC-05) | 3,1 → $9.000 (TC-06) |
| **10** | Termina el tramo 2 | 9,9 → $9.000 (TC-38) | 10 → $9.000 (TC-07) | 10,1 → $9.100 (TC-08) |
| **50** | Termina lo permitido | 49,9 → $40.900 (TC-39) | 50 → $41.000 (TC-10) | 50,1 → error (TC-11) |

**El borde más delicado es el 3.** Como mi D es par, un paquete de exactamente 3 kg paga $6.000 (tramo
1). Si mi D fuera impar, pagaría $9.000. Por eso el caso TC-05 es uno de los más importantes.

**Otros bordes:** el día. El 5 es el último día entre semana (TC-15), el 6 es el primer día con recargo
(TC-16), el 7 es el último día válido (TC-17), el 0 está justo antes del primero (TC-18) y el 8 justo
después del último (TC-19).

## 3.3 Tabla de decisión: cuando se juntan varias condiciones

Tres condiciones afectan el precio al mismo tiempo: el **cliente** (normal, frecuente o VIP), si usa el
**cupón** ENVIO10 y si es **fin de semana**. Eso da 3 × 2 × 2 = **12 combinaciones**, y pruebo todas.

El cálculo siempre sigue este orden (por mi E par y mi B impar):

1. Si es fin de semana, se suman $2.000 **primero**.
2. Se aplica el descuento del cliente (5 % o 15 %), si lo hay.
3. Se aplica el descuento del cupón (10 %), si lo hay.
4. Se redondea a la centena más cercana, y los 50 suben.

Para que las combinaciones se puedan comparar, todas usan el mismo envío: **5 kg, zona urbana**, que
parte de una tarifa base de **$9.000**.

| Regla | Cliente | Cupón | Fin de semana | Qué se aplica, en orden | Cuenta y resultado | Caso |
|:----:|---------|:-----:|:-------------:|-------------------------|--------------------|------|
| 1 | normal | No | No | Nada | 9.000 → **$9.000** | TC-20 |
| 2 | normal | Sí | No | Solo el cupón | 9.000 × 0,90 = 8.100 → **$8.100** | TC-21 |
| 3 | frecuente | No | No | Cliente (5 %) | 9.000 × 0,95 = 8.550 → **$8.600** | TC-22 |
| 4 | frecuente | Sí | No | Cliente y luego cupón | 9.000 × 0,95 × 0,90 = 7.695 → **$7.700** | TC-23 |
| 5 | vip | No | No | Cliente (15 %) | 9.000 × 0,85 = 7.650 → **$7.700** | TC-24 |
| 6 | vip | Sí | No | Cliente y luego cupón | 9.000 × 0,85 × 0,90 = 6.885 → **$6.900** | TC-25 |
| 7 | normal | No | Sí | Solo el recargo | 9.000 + 2.000 = 11.000 → **$11.000** | TC-26 |
| 8 | normal | Sí | Sí | Recargo y luego cupón | 11.000 × 0,90 = 9.900 → **$9.900** | TC-27 |
| 9 | frecuente | No | Sí | Recargo y luego cliente | 11.000 × 0,95 = 10.450 → **$10.500** | TC-28 |
| 10 | frecuente | Sí | Sí | Recargo, cliente y cupón | 11.000 × 0,95 × 0,90 = 9.405 → **$9.400** | TC-29 |
| 11 | vip | No | Sí | Recargo y luego cliente | 11.000 × 0,85 = 9.350 → **$9.400** | TC-30 |
| 12 | vip | Sí | Sí | Recargo, cliente y cupón | 11.000 × 0,85 × 0,90 = 8.415 → **$8.400** | TC-31 |

**Qué mirar en esta tabla:**

- Las reglas 3, 5, 9 y 11 dan un número que termina justo en 50. Son las que comprueban que el redondeo **sube** y no solo corta.
- Un cliente VIP con cupón paga 0,85 × 0,90 = 76,5 % del valor. Como mi B es impar, los dos descuentos se juntan. Si fuera par, solo se aplicaría el mayor.
- Los $2.000 se suman antes de descontar (E par), por eso en las reglas 8 a 12 el descuento se calcula sobre $11.000 y no sobre $9.000.
- Un cupón que no existe es un caso aparte: se ignora y no cambia nada (TC-32).

## 3.4 Matriz de casos de prueba (40 casos)

Cada caso dice qué datos entran, qué debe salir y para qué sirve. Las entradas van en este orden:
`peso · zona · cliente · día · cupón`. La técnica es **EP** (partición de equivalencia), **VL**
(valor límite), **TD** (tabla de decisión) o **CMB** (varias reglas combinadas).

### A. Peso (14 casos)

| ID | Req. | Entradas | Esperado | Qué comprueba | Técnica |
|----|------|----------|----------|---------------|---------|
| TC-01 | R1 | 0 · urbana · normal · 1 · — | Error "peso inválido" | El cero no es un peso válido | VL |
| TC-02 | R1 | −5 · urbana · normal · 1 · — | Error "peso inválido" | Un peso negativo se rechaza | EP |
| TC-03 | R1, R3 | 0,1 · urbana · normal · 1 · — | $6.000 | El peso válido más pequeño | VL |
| TC-04 | R3 | 2,9 · urbana · normal · 1 · — | $6.000 | Justo debajo de 3 kg | VL |
| TC-05 | R3 | 3 · urbana · normal · 1 · — | $6.000 | El 3 cuenta como tramo 1 | VL |
| TC-06 | R3 | 3,1 · urbana · normal · 1 · — | $9.000 | Justo encima de 3 kg pasa al tramo 2 | VL |
| TC-07 | R3 | 10 · urbana · normal · 1 · — | $9.000 | El 10 sigue siendo tramo 2 | VL |
| TC-08 | R3, R8 | 10,1 · urbana · normal · 1 · — | $9.100 | Pasa de 10 kg y se cobra la fracción extra | VL |
| TC-09 | R3 | 10,5 · urbana · normal · 1 · — | $9.400 | Medio kilo extra cuesta $400 | EP |
| TC-10 | R1, R3 | 50 · urbana · normal · 1 · — | $41.000 | El peso máximo permitido se acepta | VL |
| TC-11 | R1 | 50,1 · urbana · normal · 1 · — | Error "peso inválido" | Un peso apenas mayor al máximo se rechaza | VL |
| TC-38 | R3 | 9,9 · urbana · normal · 1 · — | $9.000 | Justo debajo de 10 kg | VL |
| TC-39 | R1, R3 | 49,9 · urbana · normal · 1 · — | $40.900 | Justo debajo del máximo | VL |
| TC-40 | R1 | −0,1 · urbana · normal · 1 · — | Error "peso inválido" | Un negativo muy pequeño se rechaza | VL |

### B. Zona (3 casos)

| ID | Req. | Entradas | Esperado | Qué comprueba | Técnica |
|----|------|----------|----------|---------------|---------|
| TC-12 | R4 | 5 · rural · normal · 1 · — | $10.800 | La zona rural cobra 20 % más | EP |
| TC-13 | R4 | 5 · nacional · normal · 1 · — | $12.600 | La zona nacional cobra 40 % más | EP |
| TC-14 | R2 | 5 · internacional · normal · 1 · — | Error | Una zona que no existe se rechaza | EP |

### C. Día de la semana (5 casos)

| ID | Req. | Entradas | Esperado | Qué comprueba | Técnica |
|----|------|----------|----------|---------------|---------|
| TC-15 | R5 | 5 · urbana · normal · 5 · — | $9.000 | El viernes no tiene recargo | VL |
| TC-16 | R5 | 5 · urbana · normal · 6 · — | $11.000 | El sábado sí tiene recargo | VL |
| TC-17 | R5 | 5 · urbana · normal · 7 · — | $11.000 | El domingo sí tiene recargo | VL |
| TC-18 | R2 | 5 · urbana · normal · 0 · — | Error | El día 0 no existe | VL |
| TC-19 | R2 | 5 · urbana · normal · 8 · — | Error | El día 8 no existe | VL |

### D. Cliente, cupón y fin de semana (12 casos, la tabla de decisión)

| ID | Req. | Entradas | Esperado | Qué comprueba | Técnica |
|----|------|----------|----------|---------------|---------|
| TC-20 | R3, R6 | 5 · urbana · normal · 1 · — | $9.000 | Sin descuentos ni recargos | TD regla 1 |
| TC-21 | R6 | 5 · urbana · normal · 1 · ENVIO10 | $8.100 | Solo el cupón | TD regla 2 |
| TC-22 | R6, R8 | 5 · urbana · frecuente · 1 · — | $8.600 | Descuento frecuente y redondeo en 50 | TD regla 3 |
| TC-23 | R6, R8 | 5 · urbana · frecuente · 1 · ENVIO10 | $7.700 | Frecuente y luego cupón | TD regla 4 |
| TC-24 | R6, R8 | 5 · urbana · vip · 1 · — | $7.700 | Descuento VIP y redondeo en 50 | TD regla 5 |
| TC-25 | R6, R8 | 5 · urbana · vip · 1 · ENVIO10 | $6.900 | VIP y luego cupón | TD regla 6 |
| TC-26 | R5 | 5 · urbana · normal · 6 · — | $11.000 | Solo el recargo de fin de semana | TD regla 7 |
| TC-27 | R5, R6 | 5 · urbana · normal · 7 · ENVIO10 | $9.900 | El cupón rebaja también el recargo | TD regla 8 |
| TC-28 | R5, R6, R8 | 5 · urbana · frecuente · 6 · — | $10.500 | Recargo, descuento frecuente y redondeo en 50 | TD regla 9 |
| TC-29 | R5, R6, R8 | 5 · urbana · frecuente · 7 · ENVIO10 | $9.400 | Los tres a la vez, el redondeo baja | TD regla 10 |
| TC-30 | R5, R6, R8 | 5 · urbana · vip · 6 · — | $9.400 | Recargo, descuento VIP y redondeo en 50 | TD regla 11 |
| TC-31 | R5, R6, R8 | 5 · urbana · vip · 7 · ENVIO10 | $8.400 | Todo junto con el cliente VIP | TD regla 12 |

### E. Cupón inexistente y costo mínimo (2 casos)

| ID | Req. | Entradas | Esperado | Qué comprueba | Técnica |
|----|------|----------|----------|---------------|---------|
| TC-32 | R7 | 5 · urbana · normal · 1 · PROMO50 | $9.000 | Un cupón que no existe se ignora, sin error | EP |
| TC-33 | R8 | 3 · urbana · vip · 1 · ENVIO10 | $5.000 | El costo nunca baja de $5.000 | EP |

### F. Envíos completos (4 casos)

| ID | Req. | Entradas | Esperado | Qué comprueba | Técnica |
|----|------|----------|----------|---------------|---------|
| TC-34 | R3 a R8 | 4 · rural · vip · 6 · ENVIO10 | $9.800 | Un envío con todas las reglas juntas | CMB |
| TC-35 | R3 a R6, R8 | 12 · nacional · frecuente · 7 · — | $16.000 | Tramo 3, zona nacional, domingo y descuento | CMB |
| TC-36 | R3 a R8 | 20 · nacional · vip · 7 · ENVIO10 | $19.700 | Un envío pesado con todo aplicado | CMB |
| TC-37 | R3 a R8 | 50 · nacional · vip · 7 · ENVIO10 | $45.400 | El caso más extremo permitido | CMB |

## 3.5 Cálculo paso a paso de seis casos

Cada cálculo se lee igual: primero digo **en qué tramo cae** el peso, después aplico los recargos y
los descuentos **en el orden de la especificación** y al final redondeo.

### TC-34 · 4 kg · rural · VIP · sábado · ENVIO10

1. **¿En qué tramo cae?** 4 kg pasa de 3 y no pasa de 10, así que paga la tarifa del tramo 2: **$9.000**.
2. **Zona rural:** sube 20 %. 9.000 × 1,20 = **$10.800**.
3. **Sábado:** se suma el recargo antes de descontar. 10.800 + 2.000 = **$12.800**.
4. **Descuentos (se aplican los dos):** primero el VIP, 12.800 × 0,85 = $10.880. Después el cupón, 10.880 × 0,90 = **$9.792**.
5. **Redondeo:** $9.792 está a 8 pesos de $9.800 y el mínimo no aplica. Resultado: **$9.800**.

### TC-31 · 5 kg · urbana · VIP · domingo · ENVIO10

1. **Tramo:** 5 kg va al tramo 2, **$9.000**. La zona urbana no tiene recargo.
2. **Domingo:** se suma el recargo primero. 9.000 + 2.000 = **$11.000**.
3. **Descuentos:** el VIP, 11.000 × 0,85 = $9.350. Luego el cupón, 9.350 × 0,90 = **$8.415**.
4. **Redondeo:** el resto es 15, que es menos de 50, así que baja. Resultado: **$8.400**.

### TC-22 · 5 kg · urbana · frecuente · lunes · sin cupón

1. **Tramo:** 5 kg va al tramo 2, **$9.000**. Zona urbana y día entre semana, sin recargos.
2. **Descuento frecuente (5 %):** 9.000 × 0,95 = **$8.550**.
3. **Redondeo:** $8.550 queda justo en 50. Por la regla R8, los 50 **suben**. Resultado: **$8.600**.

### TC-33 · 3 kg · urbana · VIP · lunes · ENVIO10

1. **Tramo:** como mi D es par, el 3 cuenta como tramo 1. Cuesta **$6.000**.
2. **Descuentos:** el VIP, 6.000 × 0,85 = $5.100. Luego el cupón, 5.100 × 0,90 = **$4.590**.
3. **Mínimo:** $4.590 es menos de $5.000, así que se cobra el mínimo. Resultado: **$5.000**.

### TC-08 · 10,1 kg · urbana · normal · lunes · sin cupón

1. **Tramo:** 10,1 kg ya pasó los 10 kg, así que va al tramo 3. Cuesta los $9.000 del tramo 2 más $800 por cada kilo sobre 10. Se pasa por 0,1 kg: 0,1 × 800 = $80. Total: **$9.080**.
2. **Recargos y descuentos:** ninguno. Es urbana, entre semana, cliente normal y sin cupón.
3. **Redondeo:** el resto es 80, que es 50 o más, así que sube. Resultado: **$9.100**.

### TC-35 · 12 kg · nacional · frecuente · domingo · sin cupón

1. **Tramo:** 12 kg pasa de 10 por 2 kg: 9.000 + 2 × 800 = **$10.600**.
2. **Zona nacional:** sube 40 %. 10.600 × 1,40 = **$14.840**.
3. **Domingo:** se suma el recargo antes de descontar. 14.840 + 2.000 = **$16.840**.
4. **Descuento frecuente (5 %):** 16.840 × 0,95 = **$15.998**.
5. **Redondeo:** $15.998 está a 2 pesos de $16.000. Resultado: **$16.000**.
