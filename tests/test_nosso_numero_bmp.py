from app.bancos.bmp.cnab_400.nosso_numero import gerar_nosso_numero


def test_nosso_numero_completo():

    resultado = gerar_nosso_numero(
        "00000000001"
    )

    assert resultado == "00000000001"


def test_nosso_numero_menor():

    resultado = gerar_nosso_numero(
        "1"
    )

    assert resultado == "00000000001"


def test_nosso_numero_remove_caracteres():

    resultado = gerar_nosso_numero(
        "1-2.3/4"
    )

    assert resultado == "00000001234"