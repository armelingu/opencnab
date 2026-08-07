from opencnab.nucleo.campos import numerico
from opencnab.nucleo.campos import alfa
from opencnab.nucleo.campos import branco
from opencnab.nucleo.campos import zeros
from opencnab.nucleo.campos import remover_acentos


def test_remover_acentos():
    resultado = remover_acentos("JOSÉ ANTÔNIO DA CONCEIÇÃO")
    assert resultado == "JOSE ANTONIO DA CONCEICAO"


def test_remover_acentos_minusculas():
    resultado = remover_acentos("ácido úmido")
    assert resultado == "acido umido"


def test_remover_acentos_sem_acento():
    resultado = remover_acentos("MERCADO CENTRAL")
    assert resultado == "MERCADO CENTRAL"


def test_remover_acentos_simbolo_vira_espaco():
    resultado = remover_acentos("CAFE º")
    assert resultado == "CAFE  "


def test_alfa_remove_acentos():
    resultado = alfa("José", 10)
    assert resultado == "JOSE      "


def test_alfa_resultado_e_ascii():
    resultado = alfa("AÇÚCAR UNIÃO", 20)
    resultado.encode("ascii")
    assert resultado == "ACUCAR UNIAO        "


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