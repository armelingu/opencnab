from datetime import date
from opencnab.bancos.itau.cnab_400.modelos import BoletoItauCobranca
from opencnab.bancos.itau.cnab_400.registros import RegistroTipo1Itau
from opencnab.bancos.itau.cnab_400.remessa import HeaderRemessaItau
from opencnab.bancos.itau.cnab_400.remessa import TrailerRemessaItau
from opencnab.bancos.itau.cnab_400.remessa import ArquivoRemessaItau

AGENCIA = "1234"
CONTA = "56789"
CARTEIRA = "109"
CNPJ_EMPRESA = "12.345.678/0001-95"


def criar_boleto():
    boleto = BoletoItauCobranca(
        numero_documento="NF001",
        nosso_numero="12345678",
        valor=1250.55,
        vencimento=date(2026, 9, 15),
        data_emissao=date(2026, 8, 10),
        nome_pagador="Jose Antonio da Silva",
        documento_pagador="123.456.789-01"
    )
    return boleto


def criar_registro():
    registro = RegistroTipo1Itau(AGENCIA, CONTA, CARTEIRA, CNPJ_EMPRESA, criar_boleto(), 2)
    return registro


def criar_arquivo():
    arquivo = ArquivoRemessaItau(
        agencia=AGENCIA,
        conta=CONTA,
        carteira=CARTEIRA,
        documento_empresa=CNPJ_EMPRESA,
        nome_empresa="MINHA EMPRESA LTDA",
        data_geracao=date(2026, 8, 10),
        sequencial_remessa=1
    )
    arquivo.adicionar_boleto(criar_boleto())
    return arquivo


def test_header_tem_400_posicoes():
    resultado = HeaderRemessaItau(AGENCIA, CONTA, "MINHA EMPRESA LTDA", date(2026, 8, 10), 1).gerar()
    assert len(resultado) == 400


def test_header_identifica_remessa():
    resultado = HeaderRemessaItau(AGENCIA, CONTA, "MINHA EMPRESA LTDA", date(2026, 8, 10), 1).gerar()
    assert resultado[0:2] == "01"
    assert resultado[2:9] == "REMESSA"


def test_header_traz_agencia_e_conta():
    resultado = HeaderRemessaItau(AGENCIA, CONTA, "MINHA EMPRESA LTDA", date(2026, 8, 10), 1).gerar()
    assert resultado[26:30] == AGENCIA
    assert resultado[30:32] == "00"
    assert resultado[32:37] == CONTA


def test_header_traz_o_banco_itau():
    resultado = HeaderRemessaItau(AGENCIA, CONTA, "MINHA EMPRESA LTDA", date(2026, 8, 10), 1).gerar()
    assert resultado[76:79] == "341"
    assert resultado[79:94] == "BANCO ITAU SA  "


def test_header_traz_a_data_de_geracao():
    resultado = HeaderRemessaItau(AGENCIA, CONTA, "MINHA EMPRESA LTDA", date(2026, 8, 10), 1).gerar()
    assert resultado[94:100] == "100826"


def test_trailer_tem_400_posicoes():
    resultado = TrailerRemessaItau(3).gerar()
    assert len(resultado) == 400


def test_trailer_e_do_tipo_9():
    resultado = TrailerRemessaItau(3).gerar()
    assert resultado[0:1] == "9"
    assert resultado[394:400] == "000003"


def test_registro_tem_400_posicoes():
    resultado = criar_registro().gerar()
    assert len(resultado) == 400


def test_registro_traz_os_dados_da_empresa():
    resultado = criar_registro().gerar()
    assert resultado[0:1] == "1"
    assert resultado[1:3] == "02"
    assert resultado[3:17] == "12345678000195"
    assert resultado[17:21] == AGENCIA
    assert resultado[21:23] == "00"
    assert resultado[23:28] == CONTA


def test_registro_traz_nosso_numero_e_carteira():
    resultado = criar_registro().gerar()
    assert resultado[62:70] == "12345678"
    assert resultado[83:86] == CARTEIRA
    assert resultado[107:108] == "I"


def test_registro_traz_a_ocorrencia_de_entrada():
    resultado = criar_registro().gerar()
    assert resultado[108:110] == "01"


def test_registro_traz_documento_vencimento_e_valor():
    resultado = criar_registro().gerar()
    assert resultado[110:120] == "NF001     "
    assert resultado[120:126] == "150926"
    assert resultado[126:139] == "0000000125055"


def test_registro_traz_o_codigo_do_banco():
    resultado = criar_registro().gerar()
    assert resultado[139:142] == "341"


def test_registro_traz_a_data_de_emissao():
    resultado = criar_registro().gerar()
    assert resultado[150:156] == "100826"


def test_registro_identifica_cpf_do_pagador():
    resultado = criar_registro().gerar()
    assert resultado[218:220] == "01"
    assert resultado[220:234] == "00012345678901"


def test_registro_identifica_cnpj_do_pagador():
    boleto = criar_boleto()
    boleto.documento_pagador = "98.765.432/0001-10"

    resultado = RegistroTipo1Itau(AGENCIA, CONTA, CARTEIRA, CNPJ_EMPRESA, boleto, 2).gerar()

    assert resultado[218:220] == "02"
    assert resultado[220:234] == "98765432000110"


def test_registro_traz_o_nome_do_pagador_sem_acento():
    boleto = criar_boleto()
    boleto.nome_pagador = "João Conceição"

    resultado = RegistroTipo1Itau(AGENCIA, CONTA, CARTEIRA, CNPJ_EMPRESA, boleto, 2).gerar()

    assert resultado[234:264] == "JOAO CONCEICAO                "


def test_registro_traz_o_sequencial():
    resultado = criar_registro().gerar()
    assert resultado[394:400] == "000002"


def test_arquivo_tem_header_detalhe_e_trailer():
    resultado = criar_arquivo().gerar().split("\r\n")

    assert len(resultado) == 3
    assert resultado[0][0:1] == "0"
    assert resultado[1][0:1] == "1"
    assert resultado[2][0:1] == "9"


def test_arquivo_numera_os_registros_em_sequencia():
    resultado = criar_arquivo().gerar().split("\r\n")

    assert resultado[0][394:400] == "000001"
    assert resultado[1][394:400] == "000002"
    assert resultado[2][394:400] == "000003"


def test_arquivo_com_dois_boletos_numera_certo():
    arquivo = criar_arquivo()
    arquivo.adicionar_boleto(criar_boleto())

    resultado = arquivo.gerar().split("\r\n")

    assert len(resultado) == 4
    assert resultado[3][394:400] == "000004"


def test_todas_as_linhas_tem_400_posicoes():
    resultado = criar_arquivo().gerar().split("\r\n")

    for linha in resultado:
        assert len(linha) == 400


def test_arquivo_sem_boleto_da_erro():
    arquivo = ArquivoRemessaItau(AGENCIA, CONTA, CARTEIRA, CNPJ_EMPRESA, "MINHA EMPRESA LTDA", date(2026, 8, 10), 1)

    resultado = ""

    try:
        arquivo.gerar()
    except Exception as erro:
        resultado = str(erro)

    assert resultado == "Remessa sem boletos"


# lemos em bytes porque o modo texto do Python troca o CRLF por LF na leitura
# e o banco exige o CRLF exatamente como foi gravado
def test_arquivo_salva_com_crlf(tmp_path):
    arquivo = criar_arquivo()
    caminho = tmp_path / "remessa.rem"

    arquivo.salvar(str(caminho))

    resultado = caminho.read_bytes()

    assert len(resultado) == 3 * 400 + 2 * 2
    assert resultado.count(b"\r\n") == 2


def test_arquivo_salvo_e_ascii_puro(tmp_path):
    arquivo = criar_arquivo()
    arquivo.boletos[0].nome_pagador = "João Conceição"
    caminho = tmp_path / "remessa.rem"

    arquivo.salvar(str(caminho))

    resultado = caminho.read_bytes()

    for byte in resultado:
        assert byte < 128
