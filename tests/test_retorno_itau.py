from datetime import date
from decimal import Decimal
from opencnab.bancos.itau.cnab_400.retorno import ler_titulo
from opencnab.bancos.itau.cnab_400.retorno import descrever_ocorrencia
from opencnab.bancos.itau.cnab_400.retorno import ArquivoRetornoItau
from opencnab.bancos.itau.cnab_400.retorno import ler_arquivo_retorno
from apoio_itau import montar_linha
from apoio_itau import montar_header
from apoio_itau import montar_detalhe
from apoio_itau import montar_trailer
from apoio_itau import montar_arquivo


def test_descrever_ocorrencia_conhecida():
    resultado = descrever_ocorrencia("06")
    assert resultado == "Liquidacao normal"


def test_descrever_ocorrencia_desconhecida():
    resultado = descrever_ocorrencia("99")
    assert resultado == "Ocorrencia desconhecida"


def test_linha_curta_da_erro():
    resultado = ""

    try:
        ler_titulo("1234")
    except Exception as erro:
        resultado = str(erro)

    assert resultado == "Linha de retorno precisa ter 400 posicoes"


def test_titulo_traz_nosso_numero_e_digito():
    resultado = ler_titulo(montar_detalhe())
    assert resultado.nosso_numero == "12345678"
    assert resultado.digito_nosso_numero == "0"


def test_titulo_traz_a_carteira():
    resultado = ler_titulo(montar_detalhe())
    assert resultado.carteira == "109"


def test_titulo_traz_o_numero_do_documento():
    resultado = ler_titulo(montar_detalhe())
    assert resultado.numero_documento == "NF001"


def test_titulo_traz_a_ocorrencia():
    resultado = ler_titulo(montar_detalhe())
    assert resultado.ocorrencia == "06"
    assert resultado.descricao() == "Liquidacao normal"


def test_titulo_traz_as_datas():
    resultado = ler_titulo(montar_detalhe())
    assert resultado.data_ocorrencia == date(2026, 8, 11)
    assert resultado.vencimento == date(2026, 9, 15)
    assert resultado.data_credito == date(2026, 8, 11)


def test_titulo_traz_os_valores():
    resultado = ler_titulo(montar_detalhe())
    assert resultado.valor_titulo == Decimal("1250.55")
    assert resultado.valor_pago == Decimal("1250.55")
    assert resultado.juros_mora == Decimal("5.00")
    assert resultado.tarifa == Decimal("3.50")


def test_titulo_traz_o_nome_do_pagador():
    resultado = ler_titulo(montar_detalhe())
    assert resultado.nome_pagador == "JOSE ANTONIO DA SILVA"


def test_titulo_traz_o_codigo_de_liquidacao():
    resultado = ler_titulo(montar_detalhe())
    assert resultado.codigo_liquidacao == "01"


def test_liquidacao_normal_conta_como_pago():
    resultado = ler_titulo(montar_detalhe(ocorrencia="06"))
    assert resultado.foi_pago() is True


def test_baixa_por_liquidacao_conta_como_pago():
    resultado = ler_titulo(montar_detalhe(ocorrencia="10"))
    assert resultado.foi_pago() is True


def test_entrada_confirmada_nao_conta_como_pago():
    resultado = ler_titulo(montar_detalhe(ocorrencia="02"))
    assert resultado.foi_pago() is False


def test_tarifa_nao_conta_como_pago():
    resultado = ler_titulo(montar_detalhe(ocorrencia="28"))
    assert resultado.foi_pago() is False


def test_arquivo_le_o_header():
    arquivo = ArquivoRetornoItau(montar_arquivo())
    arquivo.ler()

    assert arquivo.agencia == "1234"
    assert arquivo.conta == "56789"
    assert arquivo.nome_empresa == "MINHA EMPRESA LTDA"
    assert arquivo.codigo_banco == "341"
    assert arquivo.data_geracao == date(2026, 8, 10)
    assert arquivo.data_credito == date(2026, 8, 11)


def test_arquivo_le_os_titulos():
    arquivo = ArquivoRetornoItau(montar_arquivo())
    resultado = arquivo.ler()

    assert len(resultado) == 1
    assert resultado[0].nosso_numero == "12345678"


def test_arquivo_de_remessa_da_erro_na_leitura():
    linha = montar_linha([(1, "0"), (2, "1"), (3, "REMESSA")])

    resultado = ""

    try:
        ArquivoRetornoItau(linha).ler()
    except Exception as erro:
        resultado = str(erro)

    assert resultado == "Arquivo nao e um retorno"


def test_total_pago_soma_so_os_liquidados():
    linhas = []
    linhas.append(montar_header())
    linhas.append(montar_detalhe(ocorrencia="06", valor_pago="0000000125055", sequencial="000002"))
    linhas.append(montar_detalhe(ocorrencia="02", valor_pago="0000000089000", sequencial="000003"))
    linhas.append(montar_detalhe(ocorrencia="06", valor_pago="0000000089000", sequencial="000004"))
    linhas.append(montar_trailer())

    arquivo = ArquivoRetornoItau("\r\n".join(linhas))
    arquivo.ler()

    assert arquivo.total_pago() == Decimal("2140.55")
    assert len(arquivo.pagos()) == 2


def test_ler_arquivo_do_disco(tmp_path):
    caminho = tmp_path / "retorno.ret"
    caminho.write_text(montar_arquivo(), encoding="latin-1", newline="")

    resultado = ler_arquivo_retorno(str(caminho))

    assert len(resultado.titulos) == 1
    assert resultado.total_pago() == Decimal("1250.55")
