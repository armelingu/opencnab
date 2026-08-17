from datetime import date
from opencnab.bancos.bmp.cnab_400.modelos import BoletoBMP
from opencnab.bancos.bmp.cnab_400.registros import RegistroTipo1BMP


def criar_boleto():
    boleto = BoletoBMP(
        numero_documento="NF001",
        nosso_numero="1",
        valor=150.70,
        vencimento=date(2026, 6, 30),
        nome_pagador="CLIENTE TESTE",
        documento_pagador="12345678901"
    )
    return boleto


def criar_registro():
    registro = RegistroTipo1BMP(criar_boleto(), sequencial_registro=2)
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


# o layout coloca a ocorrencia em 109-110, que e a mesma posicao que o arquivo
# de retorno usa para dizer o que aconteceu com o titulo
def test_registro_tipo1_ocorrencia():
    registro = criar_registro()
    linha = registro.gerar()
    assert linha[108:110] == "01"


def test_registro_tipo1_numero_documento():
    registro = criar_registro()
    linha = registro.gerar()
    assert linha[110:120] == "NF001     "


def test_registro_tipo1_vencimento():
    registro = criar_registro()
    linha = registro.gerar()
    assert linha[120:126] == "300626"


def test_registro_tipo1_valor_sem_perder_centavos():
    registro = criar_registro()
    linha = registro.gerar()
    assert linha[126:139] == "0000000015070"


def test_registro_tipo1_especie_e_aceite():
    registro = criar_registro()
    linha = registro.gerar()
    assert linha[147:149] == "01"
    assert linha[149:150] == "N"


def test_registro_tipo1_documento_pagador():
    registro = criar_registro()
    linha = registro.gerar()
    assert linha[220:234] == "00012345678901"


def test_registro_tipo1_pagador_cpf():
    registro = criar_registro()
    linha = registro.gerar()
    assert linha[218:220] == "01"


def test_registro_tipo1_pagador_cnpj():
    boleto = criar_boleto()
    boleto.nome_pagador = "EMPRESA TESTE"
    boleto.documento_pagador = "12345678000199"

    registro = RegistroTipo1BMP(boleto, sequencial_registro=2)
    linha = registro.gerar()

    assert linha[218:220] == "02"
    assert linha[220:234] == "12345678000199"


def test_registro_tipo1_nome_pagador():
    registro = criar_registro()
    linha = registro.gerar()
    assert linha[234:274] == "CLIENTE TESTE                           "


def test_registro_tipo1_sequencial():
    registro = criar_registro()
    linha = registro.gerar()
    assert linha[394:400] == "000002"


# os campos numericos que o titulo nao usa vao zerados, porque campo numerico
# em branco costuma ser recusado pelo banco
def test_registro_tipo1_campos_de_valor_nao_usados_vao_zerados():
    registro = criar_registro()
    linha = registro.gerar()

    assert linha[160:173] == "0000000000000"
    assert linha[179:192] == "0000000000000"
    assert linha[192:205] == "0000000000000"
    assert linha[205:218] == "0000000000000"


def test_registro_tipo1_endereco_do_pagador():
    boleto = criar_boleto()
    boleto.logradouro_pagador = "RUA DAS FLORES, 123"
    boleto.cep_pagador = "01310-100"

    registro = RegistroTipo1BMP(boleto, sequencial_registro=2)
    linha = registro.gerar()

    assert linha[274:314] == "RUA DAS FLORES, 123                     "
    assert linha[326:334] == "01310100"
