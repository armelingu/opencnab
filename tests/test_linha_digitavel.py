from datetime import date
from opencnab.boletos.codigo_barras import gerar_codigo_barras
from opencnab.boletos.linha_digitavel import gerar_linha_digitavel
from opencnab.boletos.linha_digitavel import formatar_linha_digitavel
from opencnab.nucleo.modulo10 import calcular_digito_verificador


def criar_codigo_barras():
    return gerar_codigo_barras("274", 150.70, date(2026, 6, 30), "1234567890123456789012345")


def test_linha_digitavel_tem_47_posicoes():
    resultado = gerar_linha_digitavel(criar_codigo_barras())
    assert len(resultado) == 47


def test_linha_digitavel_comeca_com_banco_e_moeda():
    resultado = gerar_linha_digitavel(criar_codigo_barras())
    assert resultado[0:4] == "2749"


def test_linha_digitavel_leva_o_digito_geral():
    codigo = criar_codigo_barras()
    resultado = gerar_linha_digitavel(codigo)
    assert resultado[32:33] == codigo[4:5]


def test_linha_digitavel_termina_com_fator_e_valor():
    codigo = criar_codigo_barras()
    resultado = gerar_linha_digitavel(codigo)
    assert resultado[33:47] == codigo[5:19]


def test_linha_digitavel_digitos_dos_campos_conferem():
    resultado = gerar_linha_digitavel(criar_codigo_barras())

    primeiro = resultado[0:9]
    segundo = resultado[10:20]
    terceiro = resultado[21:31]

    assert int(resultado[9:10]) == calcular_digito_verificador(primeiro)
    assert int(resultado[20:21]) == calcular_digito_verificador(segundo)
    assert int(resultado[31:32]) == calcular_digito_verificador(terceiro)


def test_linha_digitavel_guarda_todo_o_campo_livre():
    codigo = criar_codigo_barras()
    resultado = gerar_linha_digitavel(codigo)

    campo_livre = resultado[4:9] + resultado[10:20] + resultado[21:31]

    assert campo_livre == codigo[19:44]


def test_linha_digitavel_codigo_invalido():
    mensagem = ""
    try:
        gerar_linha_digitavel("123")
    except Exception as erro:
        mensagem = str(erro)

    assert mensagem == "Codigo de barras precisa ter 44 posicoes"


def test_formatar_linha_digitavel():
    linha = gerar_linha_digitavel(criar_codigo_barras())
    resultado = formatar_linha_digitavel(linha)

    assert len(resultado) == 54
    assert resultado.count(" ") == 4
    assert resultado.count(".") == 3


def test_formatar_linha_digitavel_mantem_os_digitos():
    linha = gerar_linha_digitavel(criar_codigo_barras())
    formatada = formatar_linha_digitavel(linha)

    resultado = ""
    for caractere in formatada:
        if caractere.isdigit():
            resultado += caractere

    assert resultado == linha


def test_formatar_linha_digitavel_tamanho_errado():
    mensagem = ""
    try:
        formatar_linha_digitavel("123")
    except Exception as erro:
        mensagem = str(erro)

    assert mensagem == "Linha digitavel precisa ter 47 posicoes"


# valores congelados de um boleto ficticio, conferidos contra um boleto
# de verdade na epoca em que o calculo foi escrito
# se algum destes tres assert quebrar, o boleto gerado deixou de ser valido
def test_boleto_conhecido_codigo_de_barras():
    resultado = criar_codigo_barras()
    assert resultado == "27497149300000150701234567890123456789012345"


def test_boleto_conhecido_linha_digitavel():
    resultado = gerar_linha_digitavel(criar_codigo_barras())
    assert resultado == "27491234576789012345767890123457714930000015070"


def test_boleto_conhecido_linha_formatada():
    linha = gerar_linha_digitavel(criar_codigo_barras())
    resultado = formatar_linha_digitavel(linha)
    assert resultado == "27491.23457 67890.123457 67890.123457 7 14930000015070"
