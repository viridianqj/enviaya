# Parte 1 · Requisitos y criterios de aceptación

**Estudiante:** Elkin Eliecer Aguas Giraldo · **Código:** 0182410020

## 1.1 ¿Qué hace la función `calc`?

`calc` calcula **cuánto cuesta enviar un paquete**. Para eso recibe cinco datos: el peso, a qué zona
va, qué tipo de cliente lo envía, qué día de la semana se entrega y, si lo hay, un cupón de descuento.

### Mis números en una mirada

| Qué es | Mi valor |
|--------|----------|
| Peso máximo permitido (PMAX) | 50 kg |
| El tramo 1 llega hasta (L1) | 3 kg |
| El tramo 2 llega hasta (L2) | 10 kg |
| Recargo de zona rural (RR) | 20 % |
| Recargo de zona nacional (RN) | 40 % |
| Descuento del cliente VIP (V) | 15 % |
| Recargo de fin de semana (S) | $2.000 |

### Mis cuatro reglas de paridad, en palabras

Mi código estudiantil hace que cuatro reglas del negocio sean distintas a las de otros compañeros:

- **D = 0 (par).** Un paquete de **exactamente 3 kg** paga la tarifa del tramo 1. El límite cuenta como parte del tramo.
- **E = 2 (par).** El recargo de fin de semana se suma **antes** de los descuentos. Por eso los descuentos también rebajan ese recargo.
- **B = 1 (impar).** Si un cliente tiene descuento y además usa un cupón, se aplican **los dos**, uno después del otro: primero el del cliente y luego el del cupón.
- **F = 0 (par).** Si el cupón **no existe**, simplemente se ignora. No se da ningún error.

## 1.2 Cómo se calcula el costo, paso a paso

1. **Validar** los datos (peso, zona y día).
2. **Tarifa base** según el peso.
3. **Recargo de zona** si el envío es rural o nacional.
4. **Recargo de fin de semana** si es sábado o domingo.
5. **Descuento del cliente** si es frecuente o VIP.
6. **Descuento del cupón** si trae el cupón ENVIO10.
7. **Mínimo y redondeo:** nunca menos de $5.000, y al final se redondea a la centena más cercana.

### Un ejemplo completo

Un paquete de **4 kg** va a una zona **rural**, lo envía un cliente **VIP** un **sábado** con el cupón **ENVIO10**.

1. Pasa de 3 kg y no pasa de 10 kg, así que paga la tarifa del tramo 2: **$9.000**.
2. Zona rural: sube 20 % → 9.000 × 1,20 = **$10.800**.
3. Es sábado: se suman $2.000 → **$12.800**.
4. El cliente VIP descuenta 15 % → 12.800 × 0,85 = **$10.880**. Luego el cupón descuenta 10 % → 10.880 × 0,90 = **$9.792**.
5. Se redondea a la centena más cercana: **$9.800**.

## 1.3 Especificación completa (R1 a R8)

| ID | Qué dice la regla | Con mis números |
|----|-------------------|-----------------|
| R1 | El peso debe ser mayor que cero y no pasar del máximo. Si no, error "peso inválido". | 0 < peso ≤ 50 kg |
| R2 | La zona debe ser una de las tres válidas y el día debe ir de 1 a 7. Si no, error. | Zonas: urbana, rural, nacional. Días: 1 a 7 (6 = sábado, 7 = domingo) |
| R3 | La tarifa base depende del peso. Hay dos tramos de precio fijo. Pasado el tramo 2, se cobra un valor extra por cada kilo de más, también por fracciones de kilo. | Tramo 1 (hasta 3 kg, el 3 incluido): $6.000. Tramo 2 (hasta 10 kg, el 10 incluido): $9.000. Más de 10 kg: $9.000 + $800 por cada kg sobre 10 |
| R4 | Las zonas lejanas cuestan más. | Rural +20 %. Nacional +40 %. Urbana sin recargo |
| R5 | Los sábados y domingos se suma un valor fijo, **antes** de los descuentos. | +$2.000 los días 6 y 7 |
| R6 | Hay descuentos por tipo de cliente y por cupón. Si se tienen ambos, se aplican los dos, primero el del cliente. | Frecuente 5 %. VIP 15 %. Cupón ENVIO10 10 % |
| R7 | Un cupón que no existe se ignora, sin error. | Cualquier cupón distinto de ENVIO10 |
| R8 | El costo nunca baja de un mínimo. El resultado se redondea a la centena más cercana, y cuando queda justo en 50 sube. | Mínimo $5.000. Se redondea a múltiplos de $100. Ejemplo: 8.550 → 8.600 |

### Cosas que la especificación no dice (mis supuestos)

| ID | Supuesto |
|----|----------|
| S-1 | Si el tipo de cliente no es normal, frecuente ni VIP, la especificación no dice qué hacer. No lo pruebo como requisito. |
| S-2 | El cupón se escribe tal cual: `ENVIO10`. Cualquier otro texto cuenta como un cupón que no existe. |
| S-3 | El peso es un número y el día es un número entero. No pruebo otros tipos de dato. |

## 1.4 Historias de usuario con criterios de aceptación

Cada historia dice **quién** quiere **qué** y **para qué**. Los criterios usan el formato
**Dado** (la situación) · **Cuando** (lo que se hace) · **Entonces** (lo que debe pasar).

### HU-01 · Rechazar los envíos con datos inválidos (R1, R2)

> Como operador de EnvíaYa quiero que el sistema rechace los envíos con datos inválidos, para no
> cotizar envíos que no se pueden hacer.

- **CASO-1.1** · **Dado** un paquete de 0 kg, **cuando** se calcula el costo, **entonces** sale el error "peso inválido".
- **CASO-1.2** · **Dado** un paquete de 50,1 kg (apenas pasa el máximo), **cuando** se calcula el costo, **entonces** sale el error "peso inválido".
- **CASO-1.3** · **Dado** un paquete urbano de exactamente 50 kg, **cuando** se calcula el costo, **entonces** se acepta y cuesta $41.000.
- **CASO-1.4** · **Dado** una zona que no existe, como "internacional", **cuando** se calcula el costo, **entonces** sale un error.
- **CASO-1.5** · **Dado** un día 0 o un día 8, **cuando** se calcula el costo, **entonces** sale un error.

### HU-02 · Conocer el costo base y los recargos (R3, R4, R5)

> Como cliente quiero que el costo dependa de mi peso, de la zona y del día de entrega, para saber
> cuánto voy a pagar.

- **CASO-2.1** · **Dado** un paquete urbano de exactamente 3 kg de un cliente normal entre semana, **cuando** se calcula el costo, **entonces** cuesta $6.000 (el 3 cuenta como tramo 1).
- **CASO-2.2** · **Dado** un paquete urbano de 3,1 kg o de 10 kg, **cuando** se calcula el costo, **entonces** cuesta $9.000 (tramo 2).
- **CASO-2.3** · **Dado** un paquete urbano de 10,5 kg, **cuando** se calcula el costo, **entonces** cuesta $9.400: los $9.000 del tramo 2 más $400 por el medio kilo extra.
- **CASO-2.4** · **Dado** un paquete de 5 kg de un cliente normal entre semana, **cuando** la zona es rural, **entonces** cuesta $10.800. Si es nacional, $12.600. Si es urbana, $9.000.
- **CASO-2.5** · **Dado** un paquete urbano de 5 kg de un cliente normal, **cuando** el día es sábado o domingo, **entonces** cuesta $11.000. Si el día es viernes, cuesta $9.000.
- **CASO-2.6** · **Dado** un paquete rural de 12 kg de un cliente empresarial entre semana y sin cupón, **cuando** se calcula el costo, **entonces** no se cobra el recargo de zona y cuesta $9.300 (10.600 × 0,88 = 9.328). Si el paquete pesa exactamente 10 kg y va a zona nacional, el recargo sí se cobra y cuesta $11.100 (9.000 × 1,40 × 0,88 = 11.088).

### HU-03 · Descuentos, cupón, mínimo y redondeo (R6, R7, R8)

> Como cliente frecuente o VIP quiero que mis descuentos y mi cupón se apliquen bien, y que el
> costo final sea un valor redondeado que nunca baje del mínimo.

- **CASO-3.1** · **Dado** un paquete urbano de 5 kg de un cliente frecuente entre semana, sin cupón, **cuando** se calcula el costo, **entonces** cuesta $8.600. Con el 5 % de descuento da $8.550, que queda justo en 50 y sube.
- **CASO-3.2** · **Dado** un paquete urbano de 5 kg de un cliente VIP entre semana con el cupón ENVIO10, **cuando** se calcula el costo, **entonces** se aplican los dos descuentos, primero el VIP y luego el cupón, y cuesta $6.900 (da $6.885 y se redondea).
- **CASO-3.3** · **Dado** un cupón "PROMO50" que no existe, **cuando** se calcula el costo de un paquete urbano de 5 kg de un cliente normal entre semana, **entonces** el cupón se ignora, no hay error y cuesta $9.000.
- **CASO-3.4** · **Dado** un paquete urbano de 3 kg de un cliente VIP con ENVIO10 entre semana, **cuando** los descuentos dejarían el costo en $4.590, **entonces** el costo final es $5.000 (el mínimo).
- **CASO-3.5** · **Dado** un paquete urbano de 5 kg de un cliente VIP con ENVIO10 un domingo, **cuando** se calcula el costo, **entonces** primero se suma el recargo de $2.000 y después se aplican los descuentos, y cuesta $8.400 (da $8.415 y se redondea).
- **CASO-3.6** · **Dado** un paquete rural de 4 kg de un cliente empresarial un sábado con el cupón ENVIO10, **cuando** se calcula el costo, **entonces** primero se suma el recargo de zona y el de fin de semana, y después se aplican los dos descuentos, el empresarial y luego el cupón: 12.800 × 0,88 × 0,90 = 10.137,60, que se redondea a $10.100. 

## 1.5 Matriz de trazabilidad

**Qué pruebas protegen cada requisito**. Dice, para cada regla, en qué historia aparece y
qué casos de prueba la verifican. Los casos `TC-xx` están en `docs/03-caja-negra.md`. Esta matriz se
irá completando en las partes siguientes con las pruebas automatizadas, los defectos y el cambio de la Parte 8.

| Requisito | Historia | Casos de prueba |
|-----------|----------|-----------------|
| R1 · peso válido | HU-01 | TC-01, TC-02, TC-03, TC-10, TC-11, TC-39, TC-40 |
| R2 · zona y día válidos | HU-01 | TC-14, TC-18, TC-19 |
| R3 · tarifa base por tramos | HU-02 | TC-03 a TC-10, TC-35 a TC-39 |
| R4 · recargo por zona | HU-02 | TC-12, TC-13, TC-34 a TC-37 |
| R5 · fin de semana, antes de descuentos | HU-02 | TC-15 a TC-17, TC-26 a TC-31, TC-34 a TC-37 |
| R6 · descuento de cliente y de cupón | HU-03 | TC-21 a TC-25, TC-27, TC-29, TC-31, TC-33 a TC-37 |
| R7 · cupón inexistente se ignora | HU-03 | TC-32 |
| R8 · mínimo y redondeo | HU-03 | TC-08, TC-22 a TC-25, TC-28 a TC-31, TC-33 |
