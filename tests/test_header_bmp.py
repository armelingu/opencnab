from datetime import date
from opencnab.bancos.bmp.cnab_400.remessa import HeaderRemessaBMP

def test_header_400_posicoes():
    header = HeaderRemessaBMP(codigo_empresa="123", nome_empresa="EMPRESA TESTE", data_geracao=date(2026, 6, 5), sequencial_remessa=1)
    linha = header.gerar()
    assert len(linha) == 400