"""EnvíaYa · cálculo del costo de un envío (v2.0.0).

Refactorización de la v1.0.x: funciones pequeñas, constantes con nombre y
patrón Estrategia para las zonas y los descuentos. La aritmética es exacta
(Fraction) para que el redondeo a la centena no dependa del punto flotante.
"""
import math
from abc import ABC, abstractmethod
from fractions import Fraction

# --- Parámetros del negocio (derivados del código estudiantil) ---------------
PESO_MAXIMO_KG = 50
LIMITE_TRAMO_1_KG = 3
LIMITE_TRAMO_2_KG = 10

TARIFA_TRAMO_1 = 6000
TARIFA_TRAMO_2 = 9000
TARIFA_POR_KG_EXTRA = 800

RECARGO_RURAL = Fraction(20, 100)
RECARGO_NACIONAL = Fraction(40, 100)
RECARGO_FIN_DE_SEMANA = 2000

DESCUENTO_FRECUENTE = Fraction(5, 100)
DESCUENTO_VIP = Fraction(15, 100)
DESCUENTO_CUPON_ENVIO10 = Fraction(10, 100)

# --- Constantes generales ----------------------------------------------------
DIA_MINIMO = 1
DIA_SABADO = 6
DIA_MAXIMO = 7
COSTO_MINIMO = 5000
MULTIPLO_REDONDEO = 100
CUPON_ENVIO10 = "ENVIO10"


# --- Estrategias de zona -----------------------------------------------------
class EstrategiaZona(ABC):
    @abstractmethod
    def aplicar(self, tarifa):
        """Devuelve la tarifa con el recargo de la zona."""


class ZonaUrbana(EstrategiaZona):
    def aplicar(self, tarifa):
        return tarifa


class ZonaRural(EstrategiaZona):
    def aplicar(self, tarifa):
        return tarifa * (1 + RECARGO_RURAL)


class ZonaNacional(EstrategiaZona):
    def aplicar(self, tarifa):
        return tarifa * (1 + RECARGO_NACIONAL)


ZONAS = {
    "urbana": ZonaUrbana(),
    "rural": ZonaRural(),
    "nacional": ZonaNacional(),
}


# --- Estrategias de descuento ------------------------------------------------
class EstrategiaDescuento(ABC):
    @abstractmethod
    def aplicar(self, valor):
        """Devuelve el valor con el descuento aplicado."""


class SinDescuento(EstrategiaDescuento):
    def aplicar(self, valor):
        return valor


class DescuentoPorcentual(EstrategiaDescuento):
    def __init__(self, porcentaje):
        self.porcentaje = porcentaje

    def aplicar(self, valor):
        return valor * (1 - self.porcentaje)


DESCUENTOS_CLIENTE = {
    "frecuente": DescuentoPorcentual(DESCUENTO_FRECUENTE),
    "vip": DescuentoPorcentual(DESCUENTO_VIP),
}
DESCUENTOS_CUPON = {
    CUPON_ENVIO10: DescuentoPorcentual(DESCUENTO_CUPON_ENVIO10),
}
SIN_DESCUENTO = SinDescuento()


# --- Pasos del cálculo -------------------------------------------------------
def validar_entradas(peso, zona, dia):
    if peso <= 0 or peso > PESO_MAXIMO_KG:
        raise ValueError("peso inválido")
    if dia < DIA_MINIMO or dia > DIA_MAXIMO:
        raise ValueError("día inválido")
    if zona not in ZONAS:
        raise ValueError("zona inválida")


def tarifa_base(peso):
    if peso <= LIMITE_TRAMO_1_KG:
        return Fraction(TARIFA_TRAMO_1)
    if peso <= LIMITE_TRAMO_2_KG:
        return Fraction(TARIFA_TRAMO_2)
    kg_extra = Fraction(str(peso)) - LIMITE_TRAMO_2_KG
    return TARIFA_TRAMO_2 + kg_extra * TARIFA_POR_KG_EXTRA


def recargo_fin_de_semana(dia):
    return RECARGO_FIN_DE_SEMANA if dia >= DIA_SABADO else 0


def aplicar_descuentos(valor, cliente, cupon):
    """Primero el descuento del cliente y luego el del cupón; un cupón que
    no existe se ignora."""
    valor = DESCUENTOS_CLIENTE.get(cliente, SIN_DESCUENTO).aplicar(valor)
    return DESCUENTOS_CUPON.get(cupon, SIN_DESCUENTO).aplicar(valor)


def aplicar_costo_minimo(valor):
    return max(valor, COSTO_MINIMO)


def redondear_a_centena(valor):
    """Al múltiplo de 100 más cercano; los 50 redondean hacia arriba."""
    return math.floor(valor / MULTIPLO_REDONDEO + Fraction(1, 2)) * MULTIPLO_REDONDEO


# --- Función pública ---------------------------------------------------------
def calc(peso, zona, cliente, dia, cupon=None):
    validar_entradas(peso, zona, dia)
    valor = tarifa_base(peso)
    valor = ZONAS[zona].aplicar(valor)
    valor += recargo_fin_de_semana(dia)
    valor = aplicar_descuentos(valor, cliente, cupon)
    valor = aplicar_costo_minimo(valor)
    return redondear_a_centena(valor)
