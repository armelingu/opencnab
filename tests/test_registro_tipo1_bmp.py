from datetime import date
from app.bancos.bmp.cnab_400.registros import RegistroTipo1BMP


def criar_registro():
    registro = RegistroTipo1BMP(numero_documento="NF001", nosso_numero="1", valor=150.70, vencimento=date(2026, 6, 30), nome_pagador="CLIENTE TESTE", documento_pagador="12345678901", sequencial_registro=2)
    return registro


def test_registro_tipo1_tem_400_posicoes():
    registro = criar_registro()
    linha = registro.gerar()
    assert len(linha) == 400


def test_registro_tipo1_comeca_com_1():
    registro = criar_registro()
    linha = registro.gerar()
    assert linha[0:1] == "1"


def test_registro_tipo1_nosso_numero():
    registro = criar_registro()
    linha = registro.gerar()
    assert linha[70:81] == "00000000001"


def test_registro_tipo1_ocorrencia():
    registro = criar_registro()
    linha = registro.gerar()
    assert linha[109:111] == "01"


def test_registro_tipo1_numero_documento():
    registro = criar_registro()
    linha = registro.gerar()
    assert linha[111:121] == "NF001     "


def test_registro_tipo1_vencimento():
    registro = criar_registro()
    linha = registro.gerar()
    assert linha[121:127] == "300626"


def test_registro_tipo1_valor_sem_perder_centavos():
    registro = criar_registro()
    linha = registro.gerar()
    assert linha[127:140] == "0000000015070"


def test_registro_tipo1_documento_pagador():
    registro = criar_registro()
    linha = registro.gerar()
    assert linha[221:235] == "00012345678901"


def test_registro_tipo1_pagador_cpf():
    registro = criar_registro()
    linha = registro.gerar()
    assert linha[219:221] == "01"


def test_registro_tipo1_pagador_cnpj():
    registro = RegistroTipo1BMP(numero_documento="NF001", nosso_numero="1", valor=150.70, vencimento=date(2026, 6, 30), nome_pagador="EMPRESA TESTE", documento_pagador="12345678000199", sequencial_registro=2)
    linha = registro.gerar()
    assert linha[219:221] == "02"
    assert linha[221:235] == "12345678000199"


def test_registro_tipo1_nome_pagador():
    registro = criar_registro()
    linha = registro.gerar()
    assert linha[235:275] == "CLIENTE TESTE                           "


def test_registro_tipo1_sequencial():
    registro = criar_registro()
    linha = registro.gerar()
    assert linha[394:400] == "000002"
