from datetime import date
from opencnab import MultaItau
from opencnab.bancos.itau.cnab_400.modelos import BoletoItauCobranca


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
