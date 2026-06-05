from app.bancos.bmp.cnab_400.nosso_numero import gerar_nosso_numero
from app.bancos.bmp.cnab_400.nosso_numero import gerar_nosso_numero


def test_nosso_numero_completo():
    resultado = gerar_nosso_numero("00000000001")

    assert resultado.startswith("00000000001")
    assert "-" in resultado


def test_nosso_numero_menor():
    resultado = gerar_nosso_numero("1")

    assert resultado.startswith("00000000001")
    assert "-" in resultado


def test_nosso_numero_remove_caracteres():
    resultado = gerar_nosso_numero("1-2.3/4")

    assert resultado.startswith("00000001234")
    assert "-" in resultado


def test_nosso_numero_com_tamanho_total():
    resultado = gerar_nosso_numero("1")

    assert len(resultado) == 13