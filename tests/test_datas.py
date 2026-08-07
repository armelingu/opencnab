from datetime import date
from opencnab.nucleo.datas import data_cnab
from opencnab.nucleo.datas import data_de_cnab

def test_data_cnab():
    resultado = data_cnab(date(2026, 5, 30))
    assert resultado == "300526"

def test_data_de_cnab():
    resultado = data_de_cnab("300526")
    assert resultado == date(2026, 5, 30)

def test_data_de_cnab_zerada():
    resultado = data_de_cnab("000000")
    assert resultado is None

def test_data_de_cnab_ida_e_volta():
    resultado = data_de_cnab(data_cnab(date(2026, 6, 30)))
    assert resultado == date(2026, 6, 30)

def test_data_de_cnab_tamanho_errado():
    mensagem = ""
    try:
        data_de_cnab("3005")
    except Exception as erro:
        mensagem = str(erro)

    assert mensagem == "Data CNAB precisa ter 6 posicoes"