# Changelog

Todos los cambios notables de EnvíaYa se documentan en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el proyecto usa [Versionado Semántico](https://semver.org/lang/es/).

## [Unreleased]

## [2.1.0] - 2026-11-11

### Added
- Nuevo tipo de cliente `empresarial` con 12 % de descuento (solicitud de cambio 1).
- El cliente empresarial no paga recargo de zona cuando el peso es mayor que L2 (10 kg).
- 13 pruebas nuevas (CE-01 a CE-13) en `tests/test_cambio_empresarial.py`.
- Documento de análisis de impacto `docs/08-solicitud-cambio.md`.

## [2.0.0] - 2026-11-11

### Changed
- **BREAKING:** los parámetros de `calc` se renombraron a `peso`, `zona`, `cliente`, `dia` y `cupon`.
- Refactorización: `calc` se dividió en funciones pequeñas (`validar_entradas`, `tarifa_base`, `recargo_fin_de_semana`, `aplicar_descuentos`, `aplicar_costo_minimo`, `redondear_a_centena`).
- Patrón Estrategia para el recargo de zona y para los descuentos.
- Los números mágicos se reemplazaron por constantes con nombre.
- La aritmética usa `Fraction`, así el redondeo no depende del punto flotante.
- La prueba P15 ahora verifica que `flag` ya no existe.

### Removed
- **BREAKING:** el argumento `flag` de `calc` y el `print` asociado.

## [1.0.1] - 2026-11-11

### Fixed
- DEF-01: el sábado recibe el recargo de fin de semana (R5).
- DEF-02: el costo se redondea a la centena más cercana y los $50 suben (R8).
- DEF-03: una zona inválida lanza error (R2).
- DEF-04: un día fuera de 1 a 7 lanza error (R2).
- DEF-05: el mensaje de error dice "peso inválido" con tilde (R1).

## [1.0.0] - 2026-11-11

### Added
- Código heredado de `calc` con el `CONFIG` personalizado del estudiante, sin cambios de lógica.

[Unreleased]: https://github.com/viridianqj/enviaya/compare/v2.1.0...HEAD
[2.1.0]: https://github.com/viridianqj/enviaya/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/viridianqj/enviaya/compare/v1.0.1...v2.0.0
[1.0.1]: https://github.com/viridianqj/enviaya/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/viridianqj/enviaya/releases/tag/v1.0.0
