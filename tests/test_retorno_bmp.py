from datetime import date
from decimal import Decimal
from opencnab.bancos.bmp.cnab_400.retorno import ArquivoRetornoBMP
from opencnab.bancos.bmp.cnab_400.retorno import ler_titulo
from opencnab.bancos.bmp.cnab_400.retorno import ler_arquivo_retorno
from opencnab.bancos.bmp.cnab_400.retorno import descrever_ocorrencia


# monta uma linha de 400 posicoes colocando cada campo na posicao do layout
# recebe uma lista de pares (posicao inicial, conteudo)
def montar_linha(campos):
    linha = []

    for i in range(400):
        linha.append(" ")

    for posicao, conteudo in campos:
        indice = posicao - 1
        for caractere in conteudo:
            linha[indice] = caractere
            indice = indice + 1

    return "".join(linha)


def criar_header():
    campos = []
    campos.append((1, "0"))
    campos.append((2, "2"))
    campos.append((3, "RETORNO"))
    campos.append((27, "00000000000000000123"))
    campos.append((47, "EMPRESA TESTE"))
    campos.append((77, "274"))
    campos.append((95, "050626"))
    campos.append((395, "000001"))
    return montar_linha(campos)


def criar_detalhe(nosso_numero, ocorrencia, valor_titulo, valor_pago, sequencial):
    campos = []
    campos.append((1, "1"))
    campos.append((71, nosso_numero))
    campos.append((109, ocorrencia))
    campos.append((111, "300626"))
    campos.append((117, "NF001"))
    campos.append((147, "300626"))
    campos.append((153, valor_titulo))
    campos.append((175, "0000000000350"))
    campos.append((253, valor_pago))
    campos.append((266, "0000000000120"))
    campos.append((296, "010726"))
    campos.append((395, sequencial))
    return montar_linha(campos)


def criar_trailer():
    campos = []
    campos.append((1, "9"))
    campos.append((395, "000004"))
    return montar_linha(campos)


def criar_arquivo():
    linhas = []
    linhas.append(criar_header())
    linhas.append(criar_detalhe("00000000001", "06", "0000000015070", "0000000015420", "000002"))
    linhas.append(criar_detalhe("00000000002", "02", "0000000009990", "0000000000000", "000003"))
    linhas.append(criar_trailer())
    return "\r\n".join(linhas)


def test_ler_titulo_nosso_numero():
    linha = criar_detalhe("00000000001", "06", "0000000015070", "0000000015420", "000002")
    resultado = ler_titulo(linha)
    assert resultado.nosso_numero == "00000000001"


def test_ler_titulo_numero_documento():
    linha = criar_detalhe("00000000001", "06", "0000000015070", "0000000015420", "000002")
    resultado = ler_titulo(linha)
    assert resultado.numero_documento == "NF001"


def test_ler_titulo_valor_do_titulo():
    linha = criar_detalhe("00000000001", "06", "0000000015070", "0000000015420", "000002")
    resultado = ler_titulo(linha)
    assert resultado.valor_titulo == Decimal("150.70")


def test_ler_titulo_valor_pago():
    linha = criar_detalhe("00000000001", "06", "0000000015070", "0000000015420", "000002")
    resultado = ler_titulo(linha)
    assert resultado.valor_pago == Decimal("154.20")


def test_ler_titulo_juros_e_despesas():
    linha = criar_detalhe("00000000001", "06", "0000000015070", "0000000015420", "000002")
    resultado = ler_titulo(linha)
    assert resultado.juros_mora == Decimal("1.20")
    assert resultado.despesas == Decimal("3.50")


def test_ler_titulo_datas():
    linha = criar_detalhe("00000000001", "06", "0000000015070", "0000000015420", "000002")
    resultado = ler_titulo(linha)
    assert resultado.vencimento == date(2026, 6, 30)
    assert resultado.data_ocorrencia == date(2026, 6, 30)
    assert resultado.data_credito == date(2026, 7, 1)


def test_ler_titulo_liquidado_foi_pago():
    linha = criar_detalhe("00000000001", "06", "0000000015070", "0000000015420", "000002")
    resultado = ler_titulo(linha)
    assert resultado.foi_pago() is True
    assert resultado.descricao() == "Liquidacao normal"


def test_ler_titulo_entrada_confirmada_nao_foi_pago():
    linha = criar_detalhe("00000000002", "02", "0000000009990", "0000000000000", "000003")
    resultado = ler_titulo(linha)
    assert resultado.foi_pago() is False
    assert resultado.descricao() == "Entrada confirmada"


def test_ler_titulo_linha_curta_da_erro():
    mensagem = ""
    try:
        ler_titulo("1234")
    except Exception as erro:
        mensagem = str(erro)

    assert mensagem == "Linha de retorno precisa ter 400 posicoes"


def test_arquivo_retorno_le_header():
    arquivo = ArquivoRetornoBMP(criar_arquivo())
    arquivo.ler()
    assert arquivo.nome_empresa == "EMPRESA TESTE"
    assert arquivo.codigo_banco == "274"
    assert arquivo.data_geracao == date(2026, 6, 5)


def test_arquivo_retorno_ignora_header_e_trailer():
    arquivo = ArquivoRetornoBMP(criar_arquivo())
    resultado = arquivo.ler()
    assert len(resultado) == 2


def test_arquivo_retorno_separa_os_pagos():
    arquivo = ArquivoRetornoBMP(criar_arquivo())
    arquivo.ler()
    resultado = arquivo.pagos()
    assert len(resultado) == 1
    assert resultado[0].nosso_numero == "00000000001"


def test_arquivo_retorno_total_pago():
    arquivo = ArquivoRetornoBMP(criar_arquivo())
    arquivo.ler()
    resultado = arquivo.total_pago()
    assert resultado == Decimal("154.20")


def test_arquivo_retorno_recusa_remessa():
    linha_de_remessa = montar_linha([(1, "0"), (2, "1"), (3, "REMESSA")])

    mensagem = ""
    try:
        arquivo = ArquivoRetornoBMP(linha_de_remessa)
        arquivo.ler()
    except Exception as erro:
        mensagem = str(erro)

    assert mensagem == "Arquivo nao e um retorno"


def test_descrever_ocorrencia_desconhecida():
    resultado = descrever_ocorrencia("99")
    assert resultado == "Ocorrencia desconhecida"


def test_ler_arquivo_retorno_do_disco(tmp_path):
    caminho = tmp_path / "retorno.ret"
    destino = open(caminho, "w", encoding="latin-1", newline="")
    destino.write(criar_arquivo())
    destino.close()

    resultado = ler_arquivo_retorno(caminho)

    assert len(resultado.titulos) == 2
    assert resultado.total_pago() == Decimal("154.20")
