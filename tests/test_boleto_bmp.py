from datetime import date
from opencnab.bancos.bmp.cnab_400.modelos import BoletoBMP

def test_criar_boleto():
    boleto = BoletoBMP(
        numero_documento="NF001",
        nosso_numero="0000000001",
        valor=150.75,
        vencimento=date(2026, 6, 30),
        nome_pagador="CLIENTE TESTE",
        documento_pagador="12345678901"
    )

    assert boleto.numero_documento == "NF001"
    assert boleto.nosso_numero == "0000000001"
    assert boleto.valor == 150.75