from datetime import date
from decimal import Decimal
from opencnab.bancos.itau.cnab_400.modelos import BoletoItauCobranca
from opencnab.bancos.itau.cnab_400.remessa import ArquivoRemessaItau
from opencnab.bancos.itau.cnab_400.retorno import ArquivoRetornoItau
from opencnab.bancos.itau.boleto import BoletoItau
from opencnab.bancos.itau.boleto import calcular_dac_nosso_numero
from apoio_itau import montar_linha
from apoio_itau import montar_header
from apoio_itau import montar_trailer
from apoio_itau import AGENCIA
from apoio_itau import CONTA
from apoio_itau import CARTEIRA
from apoio_itau import CNPJ_EMPRESA


# simula o que o banco devolve depois de receber a remessa
# so precisamos das posicoes que a conciliacao le
def montar_retorno_do_banco(nosso_numero, valor_pago, sequencial):
    digito = calcular_dac_nosso_numero(AGENCIA, CONTA, CARTEIRA, nosso_numero)

    linha = montar_linha([
        (1, "1"),
        (83, CARTEIRA),
        (86, nosso_numero),
        (94, digito),
        (109, "06"),
        (111, "200926"),
        (117, "NF001     "),
        (147, "150926"),
        (153, "0000000125055"),
        (254, valor_pago),
        (296, "210926"),
        (395, sequencial),
    ])

    return linha


# o ciclo real de quem usa a biblioteca:
# 1. gera a remessa e manda para o banco
# 2. o banco devolve o retorno com as liquidacoes
# 3. a empresa concilia o que entrou na conta
def test_remessa_e_retorno_fecham_no_mesmo_nosso_numero():
    remessa = ArquivoRemessaItau(AGENCIA, CONTA, CARTEIRA, CNPJ_EMPRESA, "MINHA EMPRESA LTDA", date(2026, 8, 10), 1)
    remessa.adicionar_boleto(BoletoItauCobranca("NF001", "12345678", 1250.55, date(2026, 9, 15), date(2026, 8, 10), "Jose Antonio", "123.456.789-01"))

    linha_remessa = remessa.gerar().split("\r\n")[1]
    nosso_numero_enviado = linha_remessa[62:70]

    retorno = ArquivoRetornoItau("\r\n".join([
        montar_header(),
        montar_retorno_do_banco(nosso_numero_enviado, "0000000125055", "000002"),
        montar_trailer(),
    ]))
    retorno.ler()

    resultado = retorno.pagos()[0]

    assert resultado.nosso_numero == nosso_numero_enviado
    assert resultado.valor_pago == Decimal("1250.55")


def test_valor_da_remessa_bate_com_o_valor_creditado():
    remessa = ArquivoRemessaItau(AGENCIA, CONTA, CARTEIRA, CNPJ_EMPRESA, "MINHA EMPRESA LTDA", date(2026, 8, 10), 1)
    remessa.adicionar_boleto(BoletoItauCobranca("NF001", "12345678", 1250.55, date(2026, 9, 15), date(2026, 8, 10), "Jose Antonio", "123.456.789-01"))

    linha_remessa = remessa.gerar().split("\r\n")[1]
    valor_enviado = linha_remessa[126:139]

    retorno = ArquivoRetornoItau("\r\n".join([
        montar_header(),
        montar_retorno_do_banco("12345678", valor_enviado, "000002"),
        montar_trailer(),
    ]))
    retorno.ler()

    resultado = retorno.total_pago()

    assert resultado == Decimal("1250.55")


# o digito do nosso numero precisa ser o mesmo nas tres pontas:
# no boleto que o pagador recebe, na remessa e no retorno do banco
def test_digito_do_nosso_numero_e_o_mesmo_do_boleto():
    boleto = BoletoItau(AGENCIA, CONTA, CARTEIRA, "12345678", 1250.55, date(2026, 9, 15))
    campo_livre = boleto.gerar_campo_livre()

    digito_no_boleto = campo_livre[11:12]

    linha_retorno = montar_retorno_do_banco("12345678", "0000000125055", "000002")
    digito_no_retorno = linha_retorno[93:94]

    assert digito_no_boleto == digito_no_retorno
