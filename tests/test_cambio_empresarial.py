"""Parte 8 · Solicitud de cambio 1 (A + F) mod 3 = 1.

Cliente empresarial: 12 % de descuento. Si el peso es mayor que L2 (10 kg),
el recargo de zona no se cobra. Resultados esperados calculados a mano con
los parámetros de Elkin Aguas (L1 3, L2 10, RR 20 %, RN 40 %, S $2.000).
Se escriben ANTES de implementar el cambio.
"""
import pytest
from envios import calc

CASOS = [
    # id, entradas (peso, zona, cliente, dia, cupon), esperado, cálculo
    ("CE-01", (5, "urbana", "empresarial", 1, None), 7900),        # 9.000 × 0,88 = 7.920
    ("CE-02", (5, "rural", "empresarial", 1, None), 9500),         # 9.000 × 1,2 = 10.800 × 0,88 = 9.504
    ("CE-03", (12, "rural", "empresarial", 1, None), 9300),        # base 10.600, sin recargo × 0,88 = 9.328
    ("CE-04", (12, "rural", "normal", 1, None), 12700),            # control: 10.600 × 1,2 = 12.720
    ("CE-05", (10, "nacional", "empresarial", 1, None), 11100),    # límite: 10 no es > 10; 9.000 × 1,4 = 12.600 × 0,88 = 11.088
    ("CE-06", (10.5, "nacional", "empresarial", 1, None), 8300),   # 9.400 sin recargo × 0,88 = 8.272
    ("CE-07", (12, "nacional", "empresarial", 6, "ENVIO10"), 10000),  # 10.600 + 2.000 = 12.600 × 0,88 = 11.088 × 0,90 = 9.979,2
    ("CE-08", (4, "rural", "empresarial", 6, "ENVIO10"), 10100),   # 10.800 + 2.000 = 12.800 × 0,88 = 11.264 × 0,90 = 10.137,6
    ("CE-09", (2, "urbana", "empresarial", 1, None), 5300),        # 6.000 × 0,88 = 5.280
    ("CE-10", (3, "urbana", "empresarial", 1, "ENVIO10"), 5000),   # 6.000 × 0,88 × 0,90 = 4.752 → mínimo 5.000
    ("CE-11", (50, "nacional", "empresarial", 1, None), 36100),    # 41.000 sin recargo × 0,88 = 36.080
    ("CE-12", (12, "urbana", "empresarial", 1, None), 9300),       # 10.600 × 0,88 = 9.328
]


@pytest.mark.parametrize("ce, entradas, esperado", CASOS, ids=[c[0] for c in CASOS])
def test_cliente_empresarial(ce, entradas, esperado):
    assert calc(*entradas) == esperado


def test_ce13_zona_invalida_sigue_siendo_error_con_empresarial():
    """La validación de zona (R2) se mantiene aunque el cliente sea empresarial."""
    with pytest.raises(ValueError):
        calc(12, "insular", "empresarial", 1, None)
