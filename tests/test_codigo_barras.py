from datetime import date
from app.boletos.codigo_barras import calcular_fator_vencimento
from app.boletos.codigo_barras import gerar_codigo_barras
from app.nucleo.modulo11 import calcular_digito_codigo_barras


def test_fator_vencimento_antes_do_reinicio():
    resultado = calcular_fator_vencimento(date(2024, 10, 7))
    assert resultado == "9862"


def test_fator_vencimento_no_limite():
    resultado = calcular_fator_vencimento(date(2025, 2, 21))
    assert resultado == "9999"


def test_fator_vencimento_no_dia_do_reinicio():
    resultado = calcular_fator_vencimento(date(2025, 2, 22))
    assert resultado == "1000"


def test_fator_vencimento_depois_do_reinicio():
    resultado = calcular_fator_vencimento(date(2025, 2, 24))
    assert resultado == "1002"


def test_fator_vencimento_antes_da_data_base():
    mensagem = ""
    try:
        calcular_fator_vencimento(date(1990, 1, 1))
    except Exception as erro:
        mensagem = str(erro)

    assert mensagem == "Vencimento anterior a data base do fator de vencimento"


def test_fator_vencimento_estoura_o_limite():
    mensagem = ""
    try:
        calcular_fator_vencimento(date(2049, 10, 14))
    except Exception as erro:
        mensagem = str(erro)

    assert mensagem == "Fator de vencimento passou de 9999 e precisa de nova data base"


def test_codigo_barras_tem_44_posicoes():
    resultado = gerar_codigo_barras("274", 150.70, date(2026, 6, 30), "1234567890123456789012345")
    assert len(resultado) == 44


def test_codigo_barras_partes_fixas():
    resultado = gerar_codigo_barras("274", 150.70, date(2026, 6, 30), "1234567890123456789012345")
    assert resultado[0:3] == "274"
    assert resultado[3:4] == "9"


def test_codigo_barras_valor_em_centavos():
    resultado = gerar_codigo_barras("274", 150.70, date(2026, 6, 30), "1234567890123456789012345")
    assert resultado[9:19] == "0000015070"


def test_codigo_barras_campo_livre():
    resultado = gerar_codigo_barras("274", 150.70, date(2026, 6, 30), "1234567890123456789012345")
    assert resultado[19:44] == "1234567890123456789012345"


def test_codigo_barras_digito_geral_confere():
    resultado = gerar_codigo_barras("274", 150.70, date(2026, 6, 30), "1234567890123456789012345")

    sem_digito = resultado[0:4] + resultado[5:44]
    digito_recalculado = calcular_digito_codigo_barras(sem_digito)

    assert int(resultado[4:5]) == digito_recalculado


def test_codigo_barras_digito_geral_nunca_e_zero():
    resultado = calcular_digito_codigo_barras("2749000000000000000000000000000000000000000")
    assert resultado >= 1
    assert resultado <= 9
