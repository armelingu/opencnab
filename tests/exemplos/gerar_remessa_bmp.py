from argparse import ArgumentParser
from datetime import date
from opencnab import ArquivoRemessaBMP
from opencnab import BoletoBMP


def main():
    argumentos = ArgumentParser(description="Gera uma remessa BMP CNAB 400 com dados ficticios")
    argumentos.add_argument("caminho", help="Caminho do arquivo de remessa que sera gravado")
    opcoes = argumentos.parse_args()

    remessa = ArquivoRemessaBMP(
        codigo_empresa="123",
        nome_empresa="EMPRESA DE EXEMPLO",
        data_geracao=date(2026, 6, 5),
        sequencial_remessa=1
    )

    remessa.adicionar_boleto(BoletoBMP(
        numero_documento="NF001",
        nosso_numero="1",
        valor="150.70",
        vencimento=date(2026, 6, 30),
        nome_pagador="José de Exemplo",
        documento_pagador="123.456.789-01"
    ))

    remessa.adicionar_boleto(BoletoBMP(
        numero_documento="NF002",
        nosso_numero="2",
        valor="99.90",
        vencimento=date(2026, 7, 15),
        nome_pagador="EMPRESA FICTICIA",
        documento_pagador="12.345.678/0001-99"
    ))

    remessa.salvar(opcoes.caminho)
    print("Remessa gravada em:", opcoes.caminho)
    print("Quantidade de titulos:", len(remessa.boletos))


if __name__ == "__main__":
    main()
