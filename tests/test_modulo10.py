from app.nucleo.modulo10 import calcular_digito_verificador

def test_modulo10_12345():
    resultado = calcular_digito_verificador("12345")
    assert resultado == 5

def test_modulo10_123456():
    resultado = calcular_digito_verificador("123456")
    assert resultado == 6