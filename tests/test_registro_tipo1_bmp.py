from datetime import date
from app.bancos.bmp.cnab_400.registros import RegistroTipo1BMP

def test_registro_tipo1_tem_400_posicoes():
    registro = RegistroTipo1BMP(numero_documento="NF001", valor=150.70, vencimento=date(2026, 6, 30), nome_pagador="CLIENTE TESTE", documento_pagador="12345678901", sequencial_registro=2)
    linha = registro.gerar()
    assert len(linha) == 400