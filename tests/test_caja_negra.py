"""Parte 5 · Casos de caja negra TC-01 a TC-40 (docs/03-caja-negra.md).

Entradas: (peso, zona, cliente, dia, cupon). Los resultados esperados se
calcularon a mano con la especificacion, NO con la funcion calc.
"""
import pytest
from envios import calc

ERROR = "ERROR"

# (id, entradas, esperado)
CASOS = [
    # A. Peso
    ("TC-01", (0, "urbana", "normal", 1, None), ERROR),
    ("TC-02", (-5, "urbana", "normal", 1, None), ERROR),
    ("TC-03", (0.1, "urbana", "normal", 1, None), 6000),
    ("TC-04", (2.9, "urbana", "normal", 1, None), 6000),
    ("TC-05", (3, "urbana", "normal", 1, None), 6000),
    ("TC-06", (3.1, "urbana", "normal", 1, None), 9000),
    ("TC-07", (10, "urbana", "normal", 1, None), 9000),
    ("TC-08", (10.1, "urbana", "normal", 1, None), 9100),
    ("TC-09", (10.5, "urbana", "normal", 1, None), 9400),
    ("TC-10", (50, "urbana", "normal", 1, None), 41000),
    ("TC-11", (50.1, "urbana", "normal", 1, None), ERROR),
    ("TC-38", (9.9, "urbana", "normal", 1, None), 9000),
    ("TC-39", (49.9, "urbana", "normal", 1, None), 40900),
    ("TC-40", (-0.1, "urbana", "normal", 1, None), ERROR),
    # B. Zona
    ("TC-12", (5, "rural", "normal", 1, None), 10800),
    ("TC-13", (5, "nacional", "normal", 1, None), 12600),
    ("TC-14", (5, "internacional", "normal", 1, None), ERROR),
    # C. Dia
    ("TC-15", (5, "urbana", "normal", 5, None), 9000),
    ("TC-16", (5, "urbana", "normal", 6, None), 11000),
    ("TC-17", (5, "urbana", "normal", 7, None), 11000),
    ("TC-18", (5, "urbana", "normal", 0, None), ERROR),
    ("TC-19", (5, "urbana", "normal", 8, None), ERROR),
    # D. Tabla de decision cliente x cupon x fin de semana
    ("TC-20", (5, "urbana", "normal", 1, None), 9000),
    ("TC-21", (5, "urbana", "normal", 1, "ENVIO10"), 8100),
    ("TC-22", (5, "urbana", "frecuente", 1, None), 8600),
    ("TC-23", (5, "urbana", "frecuente", 1, "ENVIO10"), 7700),
    ("TC-24", (5, "urbana", "vip", 1, None), 7700),
    ("TC-25", (5, "urbana", "vip", 1, "ENVIO10"), 6900),
    ("TC-26", (5, "urbana", "normal", 6, None), 11000),
    ("TC-27", (5, "urbana", "normal", 7, "ENVIO10"), 9900),
    ("TC-28", (5, "urbana", "frecuente", 6, None), 10500),
    ("TC-29", (5, "urbana", "frecuente", 7, "ENVIO10"), 9400),
    ("TC-30", (5, "urbana", "vip", 6, None), 9400),
    ("TC-31", (5, "urbana", "vip", 7, "ENVIO10"), 8400),
    # E. Cupon inexistente y minimo
    ("TC-32", (5, "urbana", "normal", 1, "PROMO50"), 9000),
    ("TC-33", (3, "urbana", "vip", 1, "ENVIO10"), 5000),
    # F. Envios completos
    ("TC-34", (4, "rural", "vip", 6, "ENVIO10"), 9800),
    ("TC-35", (12, "nacional", "frecuente", 7, None), 16000),
    ("TC-36", (20, "nacional", "vip", 7, "ENVIO10"), 19700),
    ("TC-37", (50, "nacional", "vip", 7, "ENVIO10"), 45400),
]


@pytest.mark.parametrize("tc, entradas, esperado", CASOS,
                         ids=[c[0] for c in CASOS])
def test_caja_negra(tc, entradas, esperado):
    if esperado == ERROR:
        with pytest.raises(ValueError):
            calc(*entradas)
    else:
        assert calc(*entradas) == esperado


def test_mensaje_de_error_de_peso():
    """R1: el mensaje debe decir exactamente "peso inválido" (con tilde)."""
    with pytest.raises(ValueError, match="peso inválido"):
        calc(0, "urbana", "normal", 1, None)
