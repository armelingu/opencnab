from datetime import date
from opencnab.bancos.bmp.cnab_400 import ocorrencias
from opencnab.bancos.bmp.cnab_400.modelos import BoletoBMP
from opencnab.bancos.bmp.cnab_400.remessa import ArquivoRemessaBMP


def criar_remessa():
    remessa = ArquivoRemessaBMP(
        codigo_empresa="123",
        nome_empresa="MINHA EMPRESA LTDA",
        data_geracao=date(2026, 8, 17),
        sequencial_remessa=1
    )
    return remessa


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


def primeiro_detalhe(remessa):
    linhas = remessa.gerar().split("\r\n")
    return linhas[1]


def test_descrever_ocorrencia_conhecida():
    resultado = ocorrencias.descrever_ocorrencia("02")
    assert resultado == "Pedido de baixa"


def test_descrever_ocorrencia_desconhecida():
    resultado = ocorrencias.descrever_ocorrencia("77")
    assert resultado == "Ocorrencia desconhecida"


def test_entrada_nao_e_comando():
    resultado = ocorrencias.e_comando(ocorrencias.ENTRADA)
    assert resultado is False


def test_pedido_de_baixa_e_comando():
    resultado = ocorrencias.e_comando(ocorrencias.PEDIDO_DE_BAIXA)
    assert resultado is True


def test_boleto_novo_vai_com_ocorrencia_de_entrada():
    remessa = criar_remessa()
    remessa.adicionar_boleto(criar_boleto())

    resultado = primeiro_detalhe(remessa)

    assert resultado[108:110] == "01"


def test_pedir_baixa_gera_ocorrencia_02():
    remessa = criar_remessa()
    remessa.pedir_baixa(nosso_numero="2", valor=500.00, numero_documento="NF002")

    resultado = primeiro_detalhe(remessa)

    assert resultado[108:110] == "02"
    assert resultado[126:139] == "0000000050000"
    assert resultado[110:120] == "NF002     "


def test_alterar_vencimento_gera_ocorrencia_06_com_a_data_nova():
    remessa = criar_remessa()
    remessa.alterar_vencimento(nosso_numero="3", valor=800.00, novo_vencimento=date(2026, 10, 30))

    resultado = primeiro_detalhe(remessa)

    assert resultado[108:110] == "06"
    assert resultado[120:126] == "301026"


def test_alterar_valor_gera_ocorrencia_20():
    remessa = criar_remessa()
    remessa.alterar_valor(nosso_numero="3", novo_valor=999.99)

    resultado = primeiro_detalhe(remessa)

    assert resultado[108:110] == "20"
    assert resultado[126:139] == "0000000099999"


def test_mandar_protestar_gera_ocorrencia_09():
    remessa = criar_remessa()
    remessa.mandar_protestar(nosso_numero="4", valor=990.00)

    resultado = primeiro_detalhe(remessa)

    assert resultado[108:110] == "09"


# o layout separa sustar e baixar de sustar e continuar cobrando
def test_sustar_protesto_e_baixar_gera_ocorrencia_18():
    remessa = criar_remessa()
    remessa.sustar_protesto_e_baixar(nosso_numero="4", valor=990.00)

    resultado = primeiro_detalhe(remessa)

    assert resultado[108:110] == "18"


def test_sustar_protesto_e_manter_gera_ocorrencia_19():
    remessa = criar_remessa()
    remessa.sustar_protesto_e_manter(nosso_numero="4", valor=990.00)

    resultado = primeiro_detalhe(remessa)

    assert resultado[108:110] == "19"


def test_conceder_abatimento_gera_ocorrencia_04_com_o_valor():
    remessa = criar_remessa()
    remessa.conceder_abatimento(nosso_numero="5", valor=700.00, valor_abatimento=70.00)

    resultado = primeiro_detalhe(remessa)

    assert resultado[108:110] == "04"
    assert resultado[205:218] == "0000000007000"


def test_cancelar_abatimento_gera_ocorrencia_05():
    remessa = criar_remessa()
    remessa.cancelar_abatimento(nosso_numero="5", valor=700.00, valor_abatimento=70.00)

    resultado = primeiro_detalhe(remessa)

    assert resultado[108:110] == "05"


def test_comando_vai_sem_os_dados_do_pagador():
    remessa = criar_remessa()
    remessa.pedir_baixa(nosso_numero="2", valor=500.00)

    resultado = primeiro_detalhe(remessa)

    assert resultado[218:220] == "00"
    assert resultado[220:234] == "00000000000000"
    assert resultado[234:274] == " " * 40


def test_comando_vai_sem_especie_e_sem_aceite():
    remessa = criar_remessa()
    remessa.pedir_baixa(nosso_numero="2", valor=500.00)

    resultado = primeiro_detalhe(remessa)

    assert resultado[147:149] == "00"
    assert resultado[149:150] == " "


def test_comando_tem_400_posicoes():
    remessa = criar_remessa()
    remessa.pedir_baixa(nosso_numero="2", valor=500.00)

    resultado = primeiro_detalhe(remessa)

    assert len(resultado) == 400


def test_titulo_novo_e_comando_no_mesmo_arquivo():
    remessa = criar_remessa()
    remessa.adicionar_boleto(criar_boleto())
    remessa.pedir_baixa(nosso_numero="2", valor=500.00)
    remessa.alterar_vencimento(nosso_numero="3", valor=800.00, novo_vencimento=date(2026, 10, 30))

    resultado = remessa.gerar().split("\r\n")

    assert len(resultado) == 5
    assert resultado[1][108:110] == "01"
    assert resultado[2][108:110] == "02"
    assert resultado[3][108:110] == "06"


def test_sequencial_continua_correto_com_comandos():
    remessa = criar_remessa()
    remessa.adicionar_boleto(criar_boleto())
    remessa.pedir_baixa(nosso_numero="2", valor=500.00)

    resultado = remessa.gerar().split("\r\n")

    assert resultado[1][394:400] == "000002"
    assert resultado[2][394:400] == "000003"
    assert resultado[3][394:400] == "000004"


def test_titulo_novo_sem_vencimento_da_erro():
    boleto = criar_boleto()
    boleto.vencimento = None

    remessa = criar_remessa()
    remessa.adicionar_boleto(boleto)

    resultado = ""

    try:
        remessa.gerar()
    except Exception as erro:
        resultado = str(erro)

    assert resultado == "Titulo novo precisa de data de vencimento"


def test_titulo_novo_sem_documento_do_pagador_da_erro():
    boleto = criar_boleto()
    boleto.documento_pagador = ""

    remessa = criar_remessa()
    remessa.adicionar_boleto(boleto)

    resultado = ""

    try:
        remessa.gerar()
    except Exception as erro:
        resultado = str(erro)

    assert resultado == "Titulo novo precisa do CPF ou CNPJ do pagador"


def test_comando_sem_vencimento_nao_da_erro():
    remessa = criar_remessa()
    remessa.pedir_baixa(nosso_numero="2", valor=500.00)

    resultado = primeiro_detalhe(remessa)

    assert resultado[120:126] == "000000"
