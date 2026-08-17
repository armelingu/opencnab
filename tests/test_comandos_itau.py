from datetime import date
from opencnab.bancos.itau.cnab_400 import ocorrencias
from opencnab.bancos.itau.cnab_400.modelos import BoletoItauCobranca
from opencnab.bancos.itau.cnab_400.remessa import ArquivoRemessaItau
from apoio_itau import AGENCIA
from apoio_itau import CONTA
from apoio_itau import CARTEIRA
from apoio_itau import CNPJ_EMPRESA


def criar_remessa():
    remessa = ArquivoRemessaItau(
        agencia=AGENCIA,
        conta=CONTA,
        carteira=CARTEIRA,
        documento_empresa=CNPJ_EMPRESA,
        nome_empresa="MINHA EMPRESA LTDA",
        data_geracao=date(2026, 8, 17),
        sequencial_remessa=1
    )
    return remessa


def criar_boleto():
    boleto = BoletoItauCobranca(
        numero_documento="NF001",
        nosso_numero="12345678",
        valor=1250.55,
        vencimento=date(2026, 9, 15),
        data_emissao=date(2026, 8, 17),
        nome_pagador="Jose Antonio da Silva",
        documento_pagador="123.456.789-01"
    )
    return boleto


def primeiro_detalhe(remessa):
    linhas = remessa.gerar().split("\r\n")
    return linhas[1]


def test_descrever_ocorrencia_conhecida():
    resultado = ocorrencias.descrever_ocorrencia("02")
    assert resultado == "Pedido de baixa"


def test_descrever_ocorrencia_desconhecida():
    resultado = ocorrencias.descrever_ocorrencia("88")
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
    remessa.pedir_baixa(nosso_numero="11111111", valor=500.00, numero_documento="NF002")

    resultado = primeiro_detalhe(remessa)

    assert resultado[108:110] == "02"
    assert resultado[62:70] == "11111111"
    assert resultado[126:139] == "0000000050000"
    assert resultado[110:120] == "NF002     "


def test_baixa_por_pagamento_direto_gera_ocorrencia_34():
    remessa = criar_remessa()
    remessa.baixar_por_pagamento_direto(nosso_numero="11111111", valor=500.00)

    resultado = primeiro_detalhe(remessa)

    assert resultado[108:110] == "34"


def test_alterar_vencimento_gera_ocorrencia_06_com_a_data_nova():
    remessa = criar_remessa()
    remessa.alterar_vencimento(nosso_numero="22222222", valor=800.00, novo_vencimento=date(2026, 10, 30))

    resultado = primeiro_detalhe(remessa)

    assert resultado[108:110] == "06"
    assert resultado[120:126] == "301026"


def test_mandar_protestar_gera_ocorrencia_09_com_o_prazo():
    remessa = criar_remessa()
    remessa.mandar_protestar(nosso_numero="33333333", valor=990.00, dias=10)

    resultado = primeiro_detalhe(remessa)

    assert resultado[108:110] == "09"
    assert resultado[391:393] == "10"


def test_protesto_sem_prazo_vai_com_zeros():
    remessa = criar_remessa()
    remessa.mandar_protestar(nosso_numero="33333333", valor=990.00)

    resultado = primeiro_detalhe(remessa)

    assert resultado[391:393] == "00"


def test_sustar_protesto_gera_ocorrencia_18():
    remessa = criar_remessa()
    remessa.sustar_protesto(nosso_numero="33333333", valor=990.00)

    resultado = primeiro_detalhe(remessa)

    assert resultado[108:110] == "18"


def test_conceder_abatimento_gera_ocorrencia_04_com_o_valor():
    remessa = criar_remessa()
    remessa.conceder_abatimento(nosso_numero="44444444", valor=700.00, valor_abatimento=70.00)

    resultado = primeiro_detalhe(remessa)

    assert resultado[108:110] == "04"
    assert resultado[205:218] == "0000000007000"


def test_cancelar_abatimento_gera_ocorrencia_05():
    remessa = criar_remessa()
    remessa.cancelar_abatimento(nosso_numero="44444444", valor=700.00, valor_abatimento=70.00)

    resultado = primeiro_detalhe(remessa)

    assert resultado[108:110] == "05"


def test_dispensar_juros_gera_ocorrencia_47():
    remessa = criar_remessa()
    remessa.dispensar_juros(nosso_numero="55555555", valor=300.00)

    resultado = primeiro_detalhe(remessa)

    assert resultado[108:110] == "47"


# no comando o banco encontra o titulo pelo nosso numero, entao o layout manda
# zerar os dados do pagador em vez de repeti-los
def test_comando_vai_sem_os_dados_do_pagador():
    remessa = criar_remessa()
    remessa.pedir_baixa(nosso_numero="11111111", valor=500.00)

    resultado = primeiro_detalhe(remessa)

    assert resultado[218:220] == "00"
    assert resultado[220:234] == "00000000000000"
    assert resultado[234:264] == "                              "


def test_comando_vai_sem_data_de_emissao():
    remessa = criar_remessa()
    remessa.pedir_baixa(nosso_numero="11111111", valor=500.00)

    resultado = primeiro_detalhe(remessa)

    assert resultado[150:156] == "000000"


def test_comando_mantem_agencia_conta_e_carteira():
    remessa = criar_remessa()
    remessa.pedir_baixa(nosso_numero="11111111", valor=500.00)

    resultado = primeiro_detalhe(remessa)

    assert resultado[17:21] == AGENCIA
    assert resultado[23:28] == CONTA
    assert resultado[83:86] == CARTEIRA


def test_comando_tem_400_posicoes():
    remessa = criar_remessa()
    remessa.pedir_baixa(nosso_numero="11111111", valor=500.00)

    resultado = primeiro_detalhe(remessa)

    assert len(resultado) == 400


def test_titulo_novo_e_comando_no_mesmo_arquivo():
    remessa = criar_remessa()
    remessa.adicionar_boleto(criar_boleto())
    remessa.pedir_baixa(nosso_numero="11111111", valor=500.00)
    remessa.alterar_vencimento(nosso_numero="22222222", valor=800.00, novo_vencimento=date(2026, 10, 30))

    resultado = remessa.gerar().split("\r\n")

    assert len(resultado) == 5
    assert resultado[1][108:110] == "01"
    assert resultado[2][108:110] == "02"
    assert resultado[3][108:110] == "06"


def test_sequencial_continua_correto_com_comandos():
    remessa = criar_remessa()
    remessa.adicionar_boleto(criar_boleto())
    remessa.pedir_baixa(nosso_numero="11111111", valor=500.00)

    resultado = remessa.gerar().split("\r\n")

    assert resultado[0][394:400] == "000001"
    assert resultado[1][394:400] == "000002"
    assert resultado[2][394:400] == "000003"
    assert resultado[3][394:400] == "000004"


# o Banco Central nao aceita boleto sem vencimento nem sem valor, mas o
# comando sobre titulo ja registrado pode ir sem vencimento
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


def test_titulo_novo_sem_valor_da_erro():
    boleto = criar_boleto()
    boleto.valor = 0

    remessa = criar_remessa()
    remessa.adicionar_boleto(boleto)

    resultado = ""

    try:
        remessa.gerar()
    except Exception as erro:
        resultado = str(erro)

    assert resultado == "Titulo novo precisa de valor"


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


# especie e aceite so valem no registro que cria o titulo, entao no comando o
# manual manda ir zerado e em branco
def test_comando_vai_sem_especie_e_sem_aceite():
    remessa = criar_remessa()
    remessa.pedir_baixa(nosso_numero="11111111", valor=500.00)

    resultado = primeiro_detalhe(remessa)

    assert resultado[147:149] == "00"
    assert resultado[149:150] == " "


def test_titulo_novo_mantem_especie_e_aceite():
    remessa = criar_remessa()
    remessa.adicionar_boleto(criar_boleto())

    resultado = primeiro_detalhe(remessa)

    assert resultado[147:149] == "01"
    assert resultado[149:150] == "N"


def test_comando_vai_sem_instrucoes():
    remessa = criar_remessa()
    remessa.pedir_baixa(nosso_numero="11111111", valor=500.00)

    resultado = primeiro_detalhe(remessa)

    assert resultado[156:160] == "0000"


def test_comando_vai_sem_juros_desconto_iof_e_abatimento():
    remessa = criar_remessa()
    remessa.pedir_baixa(nosso_numero="11111111", valor=500.00)

    resultado = primeiro_detalhe(remessa)

    assert resultado[160:173] == "0000000000000"
    assert resultado[179:192] == "0000000000000"
    assert resultado[192:205] == "0000000000000"
    assert resultado[205:218] == "0000000000000"


def test_comando_vai_sem_endereco_do_pagador():
    remessa = criar_remessa()
    remessa.pedir_baixa(nosso_numero="11111111", valor=500.00)

    resultado = primeiro_detalhe(remessa)

    assert resultado[274:314] == " " * 40
    assert resultado[326:334] == "00000000"


def test_comando_sem_vencimento_nao_da_erro():
    remessa = criar_remessa()
    remessa.pedir_baixa(nosso_numero="11111111", valor=500.00)

    resultado = primeiro_detalhe(remessa)

    assert resultado[120:126] == "000000"
