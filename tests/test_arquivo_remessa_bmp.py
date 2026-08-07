from datetime import date
from opencnab.bancos.bmp.cnab_400.remessa import ArquivoRemessaBMP
from opencnab.bancos.bmp.cnab_400.modelos import BoletoBMP


def criar_arquivo():
    arquivo = ArquivoRemessaBMP(codigo_empresa="123", nome_empresa="EMPRESA TESTE", data_geracao=date(2026, 6, 5), sequencial_remessa=1)

    primeiro = BoletoBMP(numero_documento="NF001", nosso_numero="1", valor=150.70, vencimento=date(2026, 6, 30), nome_pagador="CLIENTE UM", documento_pagador="12345678901")
    segundo = BoletoBMP(numero_documento="NF002", nosso_numero="2", valor=99.90, vencimento=date(2026, 7, 15), nome_pagador="CLIENTE DOIS", documento_pagador="98765432100")

    arquivo.adicionar_boleto(primeiro)
    arquivo.adicionar_boleto(segundo)

    return arquivo


def test_arquivo_tem_header_dois_registros_e_trailer():
    arquivo = criar_arquivo()
    texto = arquivo.gerar()
    linhas = texto.split("\r\n")
    assert len(linhas) == 4


def test_arquivo_todas_as_linhas_tem_400_posicoes():
    arquivo = criar_arquivo()
    texto = arquivo.gerar()
    linhas = texto.split("\r\n")
    for linha in linhas:
        assert len(linha) == 400


def test_arquivo_ordem_dos_registros():
    arquivo = criar_arquivo()
    texto = arquivo.gerar()
    linhas = texto.split("\r\n")
    assert linhas[0][0:1] == "0"
    assert linhas[1][0:1] == "1"
    assert linhas[2][0:1] == "1"
    assert linhas[3][0:1] == "9"


def test_arquivo_sequencial_continuo():
    arquivo = criar_arquivo()
    texto = arquivo.gerar()
    linhas = texto.split("\r\n")
    assert linhas[0][394:400] == "000001"
    assert linhas[1][394:400] == "000002"
    assert linhas[2][394:400] == "000003"
    assert linhas[3][394:400] == "000004"


def test_arquivo_sem_boletos_da_erro():
    arquivo = ArquivoRemessaBMP(codigo_empresa="123", nome_empresa="EMPRESA TESTE", data_geracao=date(2026, 6, 5), sequencial_remessa=1)

    mensagem = ""
    try:
        arquivo.gerar()
    except Exception as erro:
        mensagem = str(erro)

    assert mensagem == "Remessa sem boletos"


def test_arquivo_salva_em_disco(tmp_path):
    arquivo = criar_arquivo()
    caminho = tmp_path / "remessa.rem"
    arquivo.salvar(caminho)

    destino = open(caminho, "r", encoding="ascii", newline="")
    texto = destino.read()
    destino.close()

    assert len(texto) == 1606
