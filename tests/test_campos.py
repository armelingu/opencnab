from opencnab.nucleo.campos import numerico
from opencnab.nucleo.campos import alfa
from opencnab.nucleo.campos import branco
from opencnab.nucleo.campos import zeros
from opencnab.nucleo.campos import remover_acentos


def test_remover_acentos():
    resultado = remover_acentos("JOSÉ ANTÔNIO DA CONCEIÇÃO")
    assert resultado == "JOSE ANTONIO DA CONCEICAO"


def test_remover_acentos_minusculas():
    resultado = remover_acentos("ácido úmido")
    assert resultado == "acido umido"


def test_remover_acentos_sem_acento():
    resultado = remover_acentos("MERCADO CENTRAL")
    assert resultado == "MERCADO CENTRAL"


def test_remover_acentos_simbolo_vira_espaco():
    resultado = remover_acentos("CAFE º")
    assert resultado == "CAFE  "


def test_alfa_remove_acentos():
    resultado = alfa("José", 10)
    assert resultado == "JOSE      "


def test_alfa_resultado_e_ascii():
    resultado = alfa("AÇÚCAR UNIÃO", 20)
    resultado.encode("ascii")
    assert resultado == "ACUCAR UNIAO        "


def test_numerico():
    resultado = numerico("123", 5)
    assert resultado == "00123"


def test_alfa():
    resultado = alfa("BMP", 10)
    assert resultado == "BMP       "


def test_branco():
    resultado = branco(3)
    assert resultado == "   "


def test_zeros():
    resultado = zeros(4)
    assert resultado == "0000"


def test_numerico_no_tamanho_maximo():
    resultado = numerico("99999", 5)
    assert resultado == "99999"


def test_numerico_maior_que_o_campo_da_erro():
    mensagem = ""

    try:
        numerico("100000", 5)
    except Exception as erro:
        mensagem = str(erro)

    assert mensagem == "Valor muito grande"


def test_numerico_confere_tamanho_depois_de_tirar_a_pontuacao():
    resultado = numerico("12.345", 5)
    assert resultado == "12345"


def test_numerico_vazio_vai_zerado():
    resultado = numerico("", 5)
    assert resultado == "00000"


def test_alfa_no_tamanho_maximo():
    resultado = alfa("ABCDE", 5)
    assert resultado == "ABCDE"


def test_alfa_corta_o_que_passa_do_campo():
    resultado = alfa("ABCDEF", 5)
    assert resultado == "ABCDE"


def test_alfa_vazio_vai_em_branco():
    resultado = alfa("", 5)
    assert resultado == "     "


def test_alfa_normaliza_antes_de_cortar():
    resultado = alfa("ação extra", 4)
    assert resultado == "ACAO"
