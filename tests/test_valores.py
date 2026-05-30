from app.nucleo.valores import valor_cnab

def test_valor_cnab_centavos():
    resultado = valor_cnab(150.75)
    assert resultado == "0000000015075"

def test_valor_cnab_inteiro():
    resultado = valor_cnab(10)
    assert resultado == "0000000001000"

def test_valor_cnab_zero():
    resultado = valor_cnab(0)
    assert resultado == "0000000000000"

