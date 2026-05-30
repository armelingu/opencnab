from app.nucleo.campos import numerico
from app.nucleo.campos import alfa
from app.nucleo.campos import branco
from app.nucleo.campos import zeros


def test_numerico():
    resultado = numerico("123", 5)
    assert resultado == "00123"


def test_alfa():
    resultado = alfa("BMP", 10)
    assert resultado == "BMP       "


def test_branco():
    resultado = branco(3)
    assert resultado == "   "


def test_zeros():
    resultado = zeros(4)
    assert resultado == "0000"