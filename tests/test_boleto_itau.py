from datetime import date
from opencnab.bancos.itau.boleto import BoletoItau
from opencnab.bancos.itau.boleto import calcular_dac_nosso_numero
from opencnab.bancos.itau.boleto import calcular_dac_conta
from opencnab.nucleo.modulo10 import calcular_digito_verificador


def criar_boleto():
    boleto = BoletoItau(agencia="1234", conta="56789", carteira="109", nosso_numero="12345678", valor=1250.55, vencimento=date(2026, 9, 15))
    return boleto


def test_campo_livre_tem_25_posicoes():
    resultado = criar_boleto().gerar_campo_livre()
    assert len(resultado) == 25


def test_campo_livre_comeca_com_a_carteira():
    resultado = criar_boleto().gerar_campo_livre()
    assert resultado[0:3] == "109"


def test_campo_livre_traz_o_nosso_numero():
    resultado = criar_boleto().gerar_campo_livre()
    assert resultado[3:11] == "12345678"


def test_campo_livre_traz_agencia_e_conta():
    resultado = criar_boleto().gerar_campo_livre()
    assert resultado[12:16] == "1234"
    assert resultado[16:21] == "56789"


def test_campo_livre_termina_com_zeros():
    resultado = criar_boleto().gerar_campo_livre()
    assert resultado[22:25] == "000"


def test_dac_do_nosso_numero_confere():
    resultado = calcular_dac_nosso_numero("1234", "56789", "109", "12345678")
    esperado = calcular_digito_verificador("1234" + "56789" + "109" + "12345678")
    assert resultado == str(esperado)


def test_dac_da_conta_confere():
    resultado = calcular_dac_conta("1234", "56789")
    esperado = calcular_digito_verificador("1234" + "56789")
    assert resultado == str(esperado)


def test_dac_entra_no_campo_livre():
    boleto = criar_boleto()
    resultado = boleto.gerar_campo_livre()

    assert resultado[11:12] == calcular_dac_nosso_numero("1234", "56789", "109", "12345678")
    assert resultado[21:22] == calcular_dac_conta("1234", "56789")


def test_codigo_barras_tem_44_posicoes():
    resultado = criar_boleto().gerar_codigo_barras()
    assert len(resultado) == 44


def test_codigo_barras_e_do_itau():
    resultado = criar_boleto().gerar_codigo_barras()
    assert resultado[0:3] == "341"


def test_linha_digitavel_tem_47_posicoes():
    resultado = criar_boleto().gerar_linha_digitavel()
    assert len(resultado) == 47


# valores congelados de um boleto ficticio do Itau
# a estrutura do campo livre e o calculo dos dois digitos foram conferidos
# contra um boleto de verdade na epoca em que este codigo foi escrito
def test_boleto_itau_conhecido_campo_livre():
    resultado = criar_boleto().gerar_campo_livre()
    assert resultado == "1091234567841234567897000"


def test_boleto_itau_conhecido_codigo_barras():
    resultado = criar_boleto().gerar_codigo_barras()
    assert resultado == "34191157000001250551091234567841234567897000"


def test_boleto_itau_conhecido_linha_formatada():
    resultado = criar_boleto().gerar_linha_digitavel_formatada()
    assert resultado == "34191.09123 34567.841233 45678.970000 1 15700000125055"
