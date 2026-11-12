"""Parte 5 · Caminos independientes P1 a P15 y casos extra X1, X2
(docs/04-caja-blanca.md)."""
import pytest
from envios import calc

ERROR = "ERROR"

# (id, entradas, esperado)
CAMINOS = [
    ("P01", (0, "urbana", "normal", 3, None), ERROR),
    ("P02", (51, "urbana", "normal", 3, None), ERROR),
    ("P03", (2, "urbana", "normal", 3, None), 6000),
    ("P04", (5, "urbana", "normal", 3, None), 9000),
    ("P05", (12, "urbana", "normal", 3, None), 10600),
    ("P06", (2, "rural", "normal", 3, None), 7200),
    ("P07", (2, "nacional", "normal", 3, None), 8400),
    ("P08", (2, "marciana", "normal", 3, None), ERROR),
    ("P09", (2, "urbana", "normal", 7, None), 8000),
    ("P10", (2, "urbana", "frecuente", 3, None), 5700),
    ("P11", (2, "urbana", "vip", 3, None), 5100),
    ("P12", (2, "urbana", "normal", 3, "XYZ"), 6000),
    ("P13", (2, "urbana", "normal", 3, "ENVIO10"), 5400),
    ("P14", (2, "urbana", "vip", 3, "ENVIO10"), 5000),
    ("X1", (2, "urbana", "normal", 6, None), 8000),
    ("X2", (2, "urbana", "normal", 9, None), ERROR),
]


@pytest.mark.parametrize("pid, entradas, esperado", CAMINOS,
                         ids=[c[0] for c in CAMINOS])
def test_caminos(pid, entradas, esperado):
    if esperado == ERROR:
        with pytest.raises(ValueError):
            calc(*entradas)
    else:
        assert calc(*entradas) == esperado


def test_p15_calc_ya_no_imprime_ni_acepta_flag(capsys):
    """P15 (v2.0.0): flag fue eliminado; calc no imprime y rechaza el argumento."""
    assert calc(2, "urbana", "normal", 3, None) == 6000
    assert capsys.readouterr().out == ""
    with pytest.raises(TypeError):
        calc(2, "urbana", "normal", 3, None, flag=True)