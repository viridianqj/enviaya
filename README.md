# EnvíaYa · Parcial 3 · Ingeniería de Software I

**Estudiante:** Elkin Eliecer Aguas Giraldo · **Código:** 0182410020
**Docente:** Ing. Robert Damián Quintero Laverde · Grupo B1 · 2026-2

Repositorio del equipo de calidad y mantenimiento de EnvíaYa: función `calc` de
`envios.py` (cálculo del costo de un envío).

## Mis parámetros
| A | B | C | D | E | F | PMAX | L1 | L2 | RR | RN | V | S | CAMBIO |
|---|---|---|---|---|---|------|----|----|----|----|---|---|--------|
| 4 | 1 | 0 | 0 | 2 | 0 | 50 kg | 3 kg | 10 kg | 20 % | 40 % | 15 % | $2.000 | 1 |

Reglas de paridad:

- **D = 0 (par):** el tramo 1 incluye el límite (`peso <= L1`).
- **E = 2 (par):** el recargo de fin de semana se suma **antes** de los descuentos.
- **B = 1 (impar):** se aplican **ambos** descuentos: primero el del cliente y luego el cupón.
- **F = 0 (par):** un cupón que no existe se **ignora**.

Solicitud de cambio: (A + F) mod 3 = (4 + 0) mod 3 = **1** → cliente empresarial con 12 % de
descuento; si el peso es mayor que L2, no se cobra el recargo de zona.

  ## Estado
   - v1.0.0:código heredado, solo con el CONFIG llenado.
   - v1.0.1:corrige DEF-01 a DEF-05.
   - v2.0.0:refactorización con patrón Estrategia; se elimina `flag`.

   Pruebas:`python -m pytest` · Cobertura: `python -m pytest --cov=envios --cov-branch`
