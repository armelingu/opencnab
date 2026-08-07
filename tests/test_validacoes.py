from app.nucleo.validacoes import somente_numeros
from app.nucleo.validacoes import tipo_inscricao


def test_somente_numeros():
    resultado = somente_numeros("123.456.789-01")
    assert resultado == "12345678901"


def test_tipo_inscricao_cpf():
    resultado = tipo_inscricao("12345678901")
    assert resultado == "01"


def test_tipo_inscricao_cnpj():
    resultado = tipo_inscricao("12345678000199")
    assert resultado == "02"


def test_tipo_inscricao_cnpj_formatado():
    resultado = tipo_inscricao("12.345.678/0001-99")
    assert resultado == "02"


def test_tipo_inscricao_documento_invalido():
    mensagem = ""
    try:
        tipo_inscricao("123")
    except Exception as erro:
        mensagem = str(erro)

    assert mensagem == "Documento precisa ter 11 digitos para CPF ou 14 para CNPJ"
