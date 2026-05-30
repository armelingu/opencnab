from app.nucleo.valores import valor_cnab

def test_valor_cnab():
    resultado = valor_cnab(150.75)
    assert resultado == "0000000015075"

def test_valor_cnab():
    resultado = valor_cnab(10)
    assert resultado == "0000000015075"