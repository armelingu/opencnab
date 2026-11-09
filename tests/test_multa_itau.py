from datetime import date
from opencnab import MultaItau
from opencnab.bancos.itau.cnab_400.modelos import BoletoItauCobranca
from opencnab.bancos.itau.cnab_400.remessa import ArquivoRemessaItau


def criar_boleto(multa=None):
    boleto = BoletoItauCobranca(
        numero_documento="NF001",
        nosso_numero="12345678",
        valor="1250.55",
        vencimento=date(2026, 9, 15),
        data_emissao=date(2026, 8, 10),
        nome_pagador="CLIENTE TESTE",
        documento_pagador="123.456.789-01",
        multa=multa
    )
    return boleto


def test_multa_guarda_codigo_data_e_valor():
    multa = MultaItau(codigo="2", data=date(2026, 9, 15), valor="2.00")
    boleto = criar_boleto(multa)

    assert boleto.multa.codigo == "2"
    assert boleto.multa.data == date(2026, 9, 15)
    assert boleto.multa.valor == "2.00"


def test_boleto_sem_multa_mantem_o_padrao():
    boleto = criar_boleto()

    assert boleto.multa is None


def criar_remessa():
    return ArquivoRemessaItau("1234", "56789", "109", "12.345.678/0001-95", "EMPRESA TESTE", date(2026, 8, 10), 1)


def gerar_linhas(multa):
    remessa = criar_remessa()
    remessa.adicionar_boleto(criar_boleto(multa))
    return remessa.gerar().split("\r\n")


def mensagem_de_erro(multa):
    mensagem = ""

    try:
        gerar_linhas(multa)
    except Exception as erro:
        mensagem = str(erro)

    return mensagem


def test_multa_percentual_nas_posicoes_do_manual():
    linhas = gerar_linhas(MultaItau("2", date(2026, 9, 15), "2.00"))
    resultado = linhas[2]

    assert [linha[0:1] for linha in linhas] == ["0", "1", "2", "9"]
    assert len(resultado) == 400
    assert resultado[0:1] == "2"
    assert resultado[1:2] == "2"
    assert resultado[2:10] == "15092026"
    assert resultado[10:23] == "0000000000200"
    assert resultado[23:394] == " " * 371
    assert resultado[394:400] == "000003"
    assert linhas[3][394:400] == "000004"


def test_multa_em_reais():
    resultado = gerar_linhas(MultaItau("1", date(2026, 9, 16), "25.01"))[2]

    assert resultado[1:2] == "1"
    assert resultado[2:10] == "16092026"
    assert resultado[10:23] == "0000000002501"


def test_codigo_zero_nao_registra_multa():
    resultado = gerar_linhas(MultaItau("0", date(2026, 9, 15), 0))[2]

    assert resultado[1:2] == "0"
    assert resultado[10:23] == "0000000000000"


def test_sem_multa_mantem_tres_registros():
    linhas = gerar_linhas(None)

    assert [linha[0:1] for linha in linhas] == ["0", "1", "9"]
    assert linhas[2][394:400] == "000003"


def test_multa_fica_junto_do_seu_titulo_e_sequencia_continua():
    remessa = criar_remessa()
    remessa.adicionar_boleto(criar_boleto(MultaItau("2", date(2026, 9, 15), 2)))
    remessa.adicionar_boleto(criar_boleto())
    remessa.adicionar_boleto(criar_boleto(MultaItau("1", date(2026, 9, 16), 25)))
    remessa.pedir_baixa("87654321", 100)

    linhas = remessa.gerar().split("\r\n")

    assert [linha[0:1] for linha in linhas] == ["0", "1", "2", "1", "1", "2", "1", "9"]
    assert [linha[394:400] for linha in linhas] == ["000001", "000002", "000003", "000004", "000005", "000006", "000007", "000008"]
    assert all(len(linha) == 400 for linha in linhas)


def test_multa_codigo_invalido():
    for codigo in ["3", "", "12", "01"]:
        resultado = mensagem_de_erro(MultaItau(codigo, date(2026, 9, 15), 2))
        assert resultado == "Codigo da multa precisa ser 0, 1 ou 2"


def test_multa_sem_data():
    resultado = mensagem_de_erro(MultaItau("2", None, 2))
    assert resultado == "Multa precisa de data"


def test_multa_antes_do_vencimento():
    resultado = mensagem_de_erro(MultaItau("2", date(2026, 9, 14), 2))
    assert resultado == "Data da multa nao pode ser anterior ao vencimento"


def test_multa_em_reais_precisa_ser_menor_que_o_titulo():
    for valor in ["1250.55", "1250.56", "1250.549"]:
        resultado = mensagem_de_erro(MultaItau("1", date(2026, 9, 15), valor))
        assert resultado == "Multa em reais precisa ser menor que o valor do titulo"


def test_multa_percentual_precisa_ser_menor_que_cem():
    for valor in ["100", "100.01", "99.995"]:
        resultado = mensagem_de_erro(MultaItau("2", date(2026, 9, 15), valor))
        assert resultado == "Percentual da multa precisa ser menor que 100"


def test_multa_percentual_no_limite():
    resultado = gerar_linhas(MultaItau("2", date(2026, 9, 15), "99.99"))[2]
    assert resultado[10:23] == "0000000009999"


def test_multa_negativa_ou_nao_finita():
    assert mensagem_de_erro(MultaItau("2", date(2026, 9, 15), -1)) == "Valor nao pode ser negativo"
    assert mensagem_de_erro(MultaItau("2", date(2026, 9, 15), "NaN")) == "Valor precisa ser finito"


def test_multa_em_comando_nao_e_enviada_silenciosamente():
    remessa = criar_remessa()
    comando = remessa.pedir_baixa("12345678", 100)
    comando.multa = MultaItau("2", date(2026, 9, 15), 2)
    mensagem = ""

    try:
        remessa.gerar()
    except Exception as erro:
        mensagem = str(erro)

    assert mensagem == "Multa disponivel somente na entrada de titulo novo"


def test_multa_gravada_em_ascii_com_crlf(tmp_path):
    remessa = criar_remessa()
    remessa.adicionar_boleto(criar_boleto(MultaItau("2", date(2026, 9, 15), 2)))
    caminho = tmp_path / "multa.rem"

    remessa.salvar(caminho)
    resultado = caminho.read_bytes()

    assert len(resultado) == 4 * 400 + 3 * 2
    assert resultado.count(b"\r\n") == 3
    assert all(byte < 128 for byte in resultado)
