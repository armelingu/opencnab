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


def test_data_de_cnab_ano_bissexto():
    resultado = data_de_cnab("290224")
    assert resultado == date(2024, 2, 29)


def test_data_de_cnab_limites_do_ano_com_dois_digitos():
    assert data_de_cnab("010100") == date(2000, 1, 1)
    assert data_de_cnab("311299") == date(2099, 12, 31)


def test_data_de_cnab_recusa_datas_inexistentes():
    for texto in ["290223", "310426", "000126", "011326"]:
        deu_erro = False

        try:
            data_de_cnab(texto)
        except ValueError:
            deu_erro = True

        assert deu_erro is True


def test_data_de_cnab_recusa_texto_sem_digitos():
    deu_erro = False

    try:
        data_de_cnab("abcdef")
    except ValueError:
        deu_erro = True

    assert deu_erro is True
