from datetime import date
from opencnab.bancos.itau.cnab_400 import instrucoes
from opencnab.bancos.itau.cnab_400.modelos import BoletoItauCobranca
from opencnab.bancos.itau.cnab_400.modelos import EnderecoPagador
from opencnab.bancos.itau.cnab_400.registros import RegistroTipo1Itau
from apoio_itau import AGENCIA
from apoio_itau import CONTA
from apoio_itau import CARTEIRA
from apoio_itau import CNPJ_EMPRESA


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


def criar_endereco():
    endereco = EnderecoPagador(
        logradouro="Rua das Flores, 123 apto 45",
        bairro="Centro",
        cep="01310-100",
        cidade="Sao Paulo",
        uf="SP"
    )
    return endereco


def gerar(boleto):
    registro = RegistroTipo1Itau(AGENCIA, CONTA, CARTEIRA, CNPJ_EMPRESA, boleto, 2)
    return registro.gerar()


def gerar_esperando_erro(boleto):
    mensagem = ""

    try:
        gerar(boleto)
    except Exception as erro:
        mensagem = str(erro)

    return mensagem


def test_descrever_instrucao_conhecida():
    resultado = instrucoes.descrever_instrucao("34")
    assert resultado == "Protestar apos xx dias corridos do vencimento"


def test_descrever_instrucao_desconhecida():
    resultado = instrucoes.descrever_instrucao("77")
    assert resultado == "Instrucao desconhecida"


def test_instrucao_de_protesto_com_prazo_pede_dias():
    resultado = instrucoes.pede_quantidade_de_dias(instrucoes.PROTESTAR_DIAS_CORRIDOS)
    assert resultado is True


def test_protestar_simples_nao_pede_dias():
    resultado = instrucoes.pede_quantidade_de_dias(instrucoes.PROTESTAR)
    assert resultado is False


def test_reconhece_instrucao_de_protesto():
    resultado = instrucoes.e_instrucao_de_protesto(instrucoes.PROTESTAR)
    assert resultado is True


def test_nao_protestar_nao_e_instrucao_de_protesto():
    resultado = instrucoes.e_instrucao_de_protesto(instrucoes.NAO_PROTESTAR)
    assert resultado is False


def test_boleto_simples_vai_sem_instrucao():
    resultado = gerar(criar_boleto())

    assert resultado[156:158] == "00"
    assert resultado[158:160] == "00"


def test_instrucoes_entram_nas_posicoes_certas():
    boleto = criar_boleto()
    boleto.instrucao_1 = instrucoes.PROTESTAR
    boleto.instrucao_2 = instrucoes.DISPENSAR_JUROS

    resultado = gerar(boleto)

    assert resultado[156:158] == "09"
    assert resultado[158:160] == "47"


def test_protesto_com_prazo_grava_os_dias():
    boleto = criar_boleto()
    boleto.instrucao_1 = instrucoes.PROTESTAR_DIAS_CORRIDOS
    boleto.dias_da_instrucao = 15

    resultado = gerar(boleto)

    assert resultado[156:158] == "34"
    assert resultado[391:393] == "15"


def test_protesto_com_prazo_sem_dias_da_erro():
    boleto = criar_boleto()
    boleto.instrucao_1 = instrucoes.PROTESTAR_DIAS_CORRIDOS

    resultado = gerar_esperando_erro(boleto)

    assert resultado == "A instrucao 34 precisa da quantidade de dias"


def test_prazo_na_segunda_instrucao_tambem_e_cobrado():
    boleto = criar_boleto()
    boleto.instrucao_2 = instrucoes.NAO_RECEBER_APOS_XX_DIAS

    resultado = gerar_esperando_erro(boleto)

    assert resultado == "A instrucao 91 precisa da quantidade de dias"


def test_protestar_e_nao_protestar_juntos_da_erro():
    boleto = criar_boleto()
    boleto.instrucao_1 = instrucoes.PROTESTAR
    boleto.instrucao_2 = instrucoes.NAO_PROTESTAR

    resultado = gerar_esperando_erro(boleto)

    assert resultado == "Nao da para mandar protestar e nao protestar no mesmo titulo"


def test_nao_protestar_e_protestar_na_ordem_inversa_tambem_da_erro():
    boleto = criar_boleto()
    boleto.instrucao_1 = instrucoes.NAO_PROTESTAR
    boleto.instrucao_2 = instrucoes.PROTESTAR

    resultado = gerar_esperando_erro(boleto)

    assert resultado == "Nao da para mandar protestar e nao protestar no mesmo titulo"


def test_juros_por_dia_entra_em_centavos():
    boleto = criar_boleto()
    boleto.juros_por_dia = 0.42

    resultado = gerar(boleto)

    assert resultado[160:173] == "0000000000042"


def test_boleto_sem_juros_vai_zerado():
    resultado = gerar(criar_boleto())

    assert resultado[160:173] == "0000000000000"


def test_data_de_mora_entra_quando_informada():
    boleto = criar_boleto()
    boleto.data_mora = date(2026, 9, 16)

    resultado = gerar(boleto)

    assert resultado[385:391] == "160926"


def test_data_de_mora_vai_zerada_quando_nao_informada():
    resultado = gerar(criar_boleto())

    assert resultado[385:391] == "000000"


def test_desconto_com_data_limite():
    boleto = criar_boleto()
    boleto.valor_desconto = 50.00
    boleto.desconto_ate = date(2026, 9, 10)

    resultado = gerar(boleto)

    assert resultado[173:179] == "100926"
    assert resultado[179:192] == "0000000005000"


def test_desconto_sem_data_limite_da_erro():
    boleto = criar_boleto()
    boleto.valor_desconto = 50.00

    resultado = gerar_esperando_erro(boleto)

    assert resultado == "Desconto informado sem a data limite para conceder"


def test_abatimento_e_iof():
    boleto = criar_boleto()
    boleto.valor_abatimento = 10.00
    boleto.valor_iof = 2.50

    resultado = gerar(boleto)

    assert resultado[192:205] == "0000000000250"
    assert resultado[205:218] == "0000000001000"


def test_endereco_do_pagador_entra_nas_posicoes_certas():
    boleto = criar_boleto()
    boleto.endereco_pagador = criar_endereco()

    resultado = gerar(boleto)

    assert resultado[274:314] == "RUA DAS FLORES, 123 APTO 45             "
    assert resultado[314:326] == "CENTRO      "
    assert resultado[326:334] == "01310100"
    assert resultado[334:349] == "SAO PAULO      "
    assert resultado[349:351] == "SP"


def test_boleto_sem_endereco_vai_em_branco():
    resultado = gerar(criar_boleto())

    assert resultado[274:314] == "                                        "
    assert resultado[326:334] == "00000000"
    assert resultado[349:351] == "  "


def test_endereco_com_acento_vira_ascii():
    endereco = criar_endereco()
    endereco.cidade = "São Paulo"

    boleto = criar_boleto()
    boleto.endereco_pagador = endereco

    resultado = gerar(boleto)

    assert resultado[334:349] == "SAO PAULO      "


def test_sacador_avalista():
    boleto = criar_boleto()
    boleto.sacador_avalista = "Empresa Avalista Ltda"

    resultado = gerar(boleto)

    assert resultado[351:381] == "EMPRESA AVALISTA LTDA         "


def test_registro_completo_continua_com_400_posicoes():
    boleto = criar_boleto()
    boleto.endereco_pagador = criar_endereco()
    boleto.juros_por_dia = 0.42
    boleto.data_mora = date(2026, 9, 16)
    boleto.valor_desconto = 50.00
    boleto.desconto_ate = date(2026, 9, 10)
    boleto.valor_abatimento = 10.00
    boleto.valor_iof = 2.50
    boleto.instrucao_1 = instrucoes.PROTESTAR_DIAS_CORRIDOS
    boleto.dias_da_instrucao = 15
    boleto.sacador_avalista = "Empresa Avalista Ltda"

    resultado = gerar(boleto)

    assert len(resultado) == 400
