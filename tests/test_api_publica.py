from datetime import date
import opencnab


# quem usa a biblioteca deve conseguir importar o essencial direto de opencnab,
# sem precisar saber em que modulo cada classe mora
def test_importa_o_essencial_do_pacote():
    resultado = []

    for nome in opencnab.__all__:
        resultado.append(hasattr(opencnab, nome))

    assert all(resultado) is True


def test_gera_remessa_itau_so_com_o_import_curto():
    remessa = opencnab.ArquivoRemessaItau(
        agencia="1234",
        conta="56789",
        carteira="109",
        documento_empresa="12.345.678/0001-95",
        nome_empresa="MINHA EMPRESA LTDA",
        data_geracao=date(2026, 8, 10),
        sequencial_remessa=1
    )

    remessa.adicionar_boleto(opencnab.BoletoItauCobranca(
        numero_documento="NF001",
        nosso_numero="12345678",
        valor=1250.55,
        vencimento=date(2026, 9, 15),
        data_emissao=date(2026, 8, 10),
        nome_pagador="Jose Antonio",
        documento_pagador="123.456.789-01"
    ))

    resultado = remessa.gerar().split("\r\n")

    assert len(resultado) == 3


def test_gera_remessa_bmp_so_com_o_import_curto():
    remessa = opencnab.ArquivoRemessaBMP(
        codigo_empresa="123",
        nome_empresa="MINHA EMPRESA LTDA",
        data_geracao=date(2026, 6, 5),
        sequencial_remessa=1
    )

    remessa.adicionar_boleto(opencnab.BoletoBMP(
        numero_documento="NF001",
        nosso_numero="1",
        valor=150.70,
        vencimento=date(2026, 6, 30),
        nome_pagador="Jose Antonio",
        documento_pagador="123.456.789-01"
    ))

    resultado = remessa.gerar().split("\r\n")

    assert len(resultado) == 3


def test_gera_boleto_so_com_o_import_curto():
    codigo = opencnab.gerar_codigo_barras("274", 150.70, date(2026, 6, 30), "1234567890123456789012345")

    resultado = opencnab.gerar_linha_digitavel(codigo)

    assert len(resultado) == 47
