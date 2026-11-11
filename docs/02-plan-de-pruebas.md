# Parte 2 · Plan de pruebas

**Estudiante:** Elkin Eliecer Aguas Giraldo · **Código:** 0182410020
**Qué se prueba:** la función `calc` de `envios.py` (EnvíaYa), en su versión heredada v1.0.0 y en las siguientes.

**¿Cómo voy a comprobar que este software hace lo que
debe?** Aquí explico qué voy a probar, de qué formas, con qué herramientas, qué puede salir mal y
cuándo doy por terminado el trabajo.

## 2.1 Alcance

**Qué sí se prueba**

- Que los datos inválidos se rechacen: peso (R1), zona y día (R2).
- Que el costo se calcule bien: tarifa base (R3), recargos de zona y de fin de semana (R4, R5), descuentos y cupón (R6, R7), mínimo y redondeo (R8).
- Que después de corregir y de reorganizar el código **nada se dañe** (pruebas de regresión).
- El cambio de la Parte 8 (cliente empresarial), con las pruebas escritas antes que el código.

**Qué no se prueba**

- Pantallas, base de datos, velocidad o seguridad. El sistema es una sola función.
- Datos de tipo equivocado, como un peso escrito con letras (supuesto S-3).
- Tipos de cliente que la especificación no define (supuesto S-1).

**Objetivo:** encontrar los defectos del código heredado según mi especificación, demostrarlos con
pruebas que se puedan repetir, corregirlos sin romper nada y dejar una suite de pruebas que proteja
los cambios futuros.

## 2.2 Los cuatro niveles de prueba

Las pruebas se hacen en niveles, de lo más pequeño a lo más grande. Como aquí todo es una sola
función, los cuatro niveles usan la misma entrada pública, pero cada uno responde una pregunta distinta.

| Nivel | La pregunta que responde | Cómo se aplica a este caso |
|-------|--------------------------|----------------------------|
| **Unidad** | ¿Cada pieza funciona sola? | Pruebo `calc` regla por regla: un caso para el peso, otro para la zona, otro para el día. Después del refactor probaré también cada función pequeña que extraiga. Casos TC-01 a TC-19, TC-32, TC-33 y TC-38 a TC-40. |
| **Integración** | ¿Las piezas funcionan bien juntas? | Pruebo que las reglas se apliquen **en el orden correcto** cuando se juntan: zona, fin de semana, descuento de cliente, cupón, mínimo y redondeo. Un error de orden solo aparece aquí. Casos TC-20 a TC-31 y TC-34 a TC-37. |
| **Sistema** | ¿El envío completo se cotiza bien, de principio a fin? | Pruebo cotizaciones reales, con todos los datos a la vez y también con errores, usando solo la interfaz pública, sin mirar el código. Casos TC-34 a TC-37 y los escenarios de la Parte 5. |
| **Aceptación** | ¿Esto es lo que el cliente pidió? | Cada criterio Dado/Cuando/Entonces de las historias de usuario se convierte en una prueba. La aceptación final la da el docente, que hace de representante de EnvíaYa, en la sustentación. |

**¿Qué casos prueban cada criterio de aceptación?**

| Criterio | Casos | Criterio | Casos |
|----------|-------|----------|-------|
| CASO-1.1 | TC-01 | CASO-2.4 | TC-12, TC-13, TC-20 |
| CASO-1.2 | TC-11 | CASO-2.5 | TC-15, TC-16, TC-17 |
| CASO-1.3 | TC-10 | CASO-3.1 | TC-22 |
| CASO-1.4 | TC-14 | CASO-3.2 | TC-25 |
| CASO-1.5 | TC-18, TC-19 | CASO-3.3 | TC-32 |
| CASO-2.1 | TC-05 | CASO-3.4 | TC-33 |
| CASO-2.2 | TC-06, TC-07 | CASO-3.5 | TC-31 |
| CASO-2.3 | TC-09 | | |

## 2.3 Estrategia: cómo voy a trabajar

1. **Diseñar casos sin mirar el código** (caja negra, Parte 3): agrupo los datos en familias, pruebo los bordes y cruzo las condiciones.
2. **Diseñar casos mirando el código** (caja blanca, Parte 4): dibujo los caminos que puede seguir `calc` y me aseguro de recorrerlos todos.
3. **Calcular cada resultado esperado a mano** a partir de la especificación y verificarlo con un segundo cálculo independiente. Nunca copio el resultado del código, porque si el código está mal, mi esperado quedaría mal.
4. **Automatizar** todo con pytest y medir la cobertura con pytest-cov.
5. **Ejecutar las pruebas contra el código heredado.** Las que fallen señalan defectos. Cada defecto se registra con su gravedad y su prioridad.
6. **Corregir y reorganizar** en ramas separadas, con la suite completa como red de seguridad, y volver a ejecutar todo (regresión).
7. **Hacer el cambio de la Parte 8 con las pruebas primero:** las escribo, las veo fallar, implemento el cambio y las veo pasar.
8. **Empezar por lo que más duele.** Lo más grave es cobrar mal, así que primero van los errores de cálculo, descuentos y redondeo.

## 2.4 Ambiente

| Elemento | Detalle |
|----------|---------|
| Computador | Windows, con PowerShell |
| Herramientas | Python, pytest, pytest-cov y Git |
| Repositorio | Carpeta `enviaya`, con una rama por cada defecto, una para el refactor y una para las pruebas |
| Datos de prueba | Los 40 casos de `docs/03-caja-negra.md`, todos inventados, sin datos reales |
| Evidencia | Capturas de pytest y de cobertura, y la salida de `git log --oneline --graph --all` |

## 2.5 Roles

El equipo es de una sola persona que usa varios "sombreros".

| Rol | Qué hace |
|-----|----------|
| Analista de requisitos | Escribe las reglas, las historias y la trazabilidad |
| Diseñador de pruebas | Diseña los casos y calcula los resultados esperados |
| Automatizador | Escribe la suite de pytest y mide la cobertura |
| Desarrollador de mantenimiento | Corrige los defectos, reorganiza el código y hace el cambio de la Parte 8 |
| Gestor de configuración | Maneja ramas, etiquetas, versiones y CHANGELOG |
| Aprobador | El docente, como representante de EnvíaYa, que revisa y acepta |

## 2.6 Riesgos y cómo evitarlos

| Riesgo | Qué podría pasar | Qué hago para evitarlo |
|--------|------------------|------------------------|
| Calcular mal un resultado esperado | Una prueba correcta se vería como falla, o una falla pasaría desapercibida | Cada cálculo se hace a mano y se verifica con un segundo cálculo independiente |
| Marcar como defecto algo que está bien con mis dígitos | Reporto un "defecto" que no existe y pierdo puntos | Reviso cada línea del código contra mis cuatro reglas de paridad (D, E, B, F) |
| Errores de decimales en los descuentos y el redondeo | Un valor que debería subir en $50 baja | Incluyo casos que caen justo en $50 y uso aritmética exacta al corregir |
| Romper algo al reorganizar el código | Una regla que funcionaba deja de funcionar | Tengo la suite completa antes de tocar el código, hago commits pequeños y repito la regresión |
| Quitar el argumento `flag` | Quien lo use dejaría de funcionar | Subo la versión mayor y lo explico en el CHANGELOG |
| Reglas que la especificación no define | Pruebo algo que nadie pidió | Dejo escritos los supuestos S-1 a S-3 |
| Cobertura del 100 % que no comprueba valores | Creo que está todo probado y no es así | Combino la cobertura con los casos de bordes y los resultados esperados independientes |
| Quedarme sin tiempo | No entrego a las 11:59 p. m. | Trabajo por etapas, con una hora de colchón, y armo el informe desde el principio |
| No poder explicar mi trabajo | Nota máxima de 2,0 | Entiendo cada etapa antes de seguir y ensayo el ejercicio de la sustentación al final |

## 2.7 Criterios de entrada y de salida

**Para empezar a ejecutar pruebas necesito:**

- La especificación R1 a R8 con mis parámetros revisada.
- El `CONFIG` verificado contra mi código estudiantil.
- El código heredado etiquetado `v1.0.0`.
- Python, pytest, pytest-cov y Git instalados.
- Los casos diseñados, con su resultado esperado calculado y verificado.

**Para dar por terminado el trabajo necesito:**

- Todos los casos ejecutados contra v1.0.0 y cada falla analizada.
- Todos los defectos registrados, con gravedad y prioridad justificadas.
- Después de corregir: todos los casos pasando y ningún defecto grave abierto.
- Cobertura de al menos 95 % de las sentencias y 90 % de las ramas.
- La regresión completa en verde después del refactor y del cambio de la Parte 8.
- Las etiquetas de versión publicadas y el CHANGELOG al día.
