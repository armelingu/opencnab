from decimal import Decimal
from app.nucleo.valores import valor_cnab
from app.nucleo.valores import valor_de_cnab

def test_valor_cnab_centavos():
    resultado = valor_cnab(150.75)
    assert resultado == "0000000015075"

def test_valor_cnab_inteiro():
    resultado = valor_cnab(10)
    assert resultado == "0000000001000"

def test_valor_cnab_zero():
    resultado = valor_cnab(0)
    assert resultado == "0000000000000"

def test_valor_cnab_centavos_quebrados():
    resultado = valor_cnab(150.70)
    assert resultado == "0000000015070"

def test_valor_cnab_dizima():
    resultado = valor_cnab(0.07)
    assert resultado == "0000000000007"

def test_valor_cnab_texto():
    resultado = valor_cnab("1234.56")
    assert resultado == "0000000123456"

def test_valor_cnab_tamanho_personalizado():
    resultado = valor_cnab(150.70, 10)
    assert resultado == "0000015070"

def test_valor_de_cnab():
    resultado = valor_de_cnab("0000000015070")
    assert resultado == Decimal("150.70")

def test_valor_de_cnab_zero():
    resultado = valor_de_cnab("0000000000000")
    assert resultado == Decimal("0.00")

def test_valor_de_cnab_ida_e_volta():
    resultado = valor_de_cnab(valor_cnab("2500.99"))
    assert resultado == Decimal("2500.99")

def test_valor_de_cnab_sem_digitos():
    mensagem = ""
    try:
        valor_de_cnab("             ")
    except Exception as erro:
        mensagem = str(erro)

    assert mensagem == "Valor CNAB sem digitos"

