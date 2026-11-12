# Parte 7 · Notas de versión y versionado semántico

## v2.1.0 · 2026-11-11 · MINOR
**Qué hay de nuevo:** cliente empresarial con 12 % de descuento. Si el peso es mayor que 10 kg, el empresarial no paga recargo de zona.
**Compatibilidad:** total. Las llamadas anteriores dan los mismos resultados.
**Por qué MINOR:** agrega funcionalidad sin romper la interfaz.

## v2.0.0 · 2026-11-11 · MAJOR
**Qué cambia:** refactorización con funciones pequeñas, constantes con nombre y patrón Estrategia para zonas y descuentos. Aritmética exacta con `Fraction`.
**Cambios que rompen la compatibilidad:**
- Se eliminó el argumento `flag` de `calc`, y llamar `calc(..., flag=True)` ahora lanza `TypeError`.
- Los parámetros se renombraron a `peso`, `zona`, `cliente`, `dia` y `cupon`, y las llamadas con argumentos con nombre (`p=`, `z=`) dejan de funcionar.

**Por qué MAJOR:** quitar `flag` cambia la interfaz pública de `calc`. En versionado semántico, cualquier cambio incompatible hacia atrás obliga a subir la versión mayor, aunque el cálculo del costo sea el mismo. La prueba P15 documenta ese cambio.

## v1.0.1 · 2026-11-11 · PATCH
**Qué se corrigió:** DEF-01 a DEF-05 (sábado sin recargo, redondeo, zona inválida, día inválido y mensaje de peso).
**Por qué PATCH:** solo corrige defectos, y la interfaz de `calc` no cambia.

## v1.0.0 · 2026-11-11
Código heredado, solo con el `CONFIG` llenado con los parámetros del estudiante.
