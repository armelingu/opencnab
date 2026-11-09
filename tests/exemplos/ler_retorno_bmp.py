from argparse import ArgumentParser
from opencnab import ler_retorno_bmp


def main():
    argumentos = ArgumentParser(description="Le um arquivo de retorno BMP CNAB 400")
    argumentos.add_argument("caminho", help="Caminho do arquivo de retorno recebido do banco")
    opcoes = argumentos.parse_args()

    retorno = ler_retorno_bmp(opcoes.caminho)

    print("Empresa:", retorno.nome_empresa)
    print("Banco:", retorno.codigo_banco)
    print("Quantidade de titulos:", len(retorno.titulos))

    # entrada confirmada nao e pagamento, entao mostramos a ocorrencia de todos
    for titulo in retorno.titulos:
        print(titulo.nosso_numero, titulo.numero_documento, titulo.ocorrencia, titulo.descricao())

    print("Titulos pagos:")

    for titulo in retorno.pagos():
        print(titulo.nosso_numero, titulo.valor_pago, titulo.data_credito)

    print("Total pago:", retorno.total_pago())


if __name__ == "__main__":
    main()
