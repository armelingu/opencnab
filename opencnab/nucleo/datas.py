from datetime import date

# transforam o formato de data 00/00/0000
# no padrao cnab 000000
def data_cnab(data):
    data_texto = data.strftime("%d%m%y")
    return data_texto


# varios campos de data sao opcionais e o layout manda zerar quando nao se
# aplicam, como a data de desconto de um titulo que nao tem desconto
def data_ou_zeros(data, tamanho=6):
    if data is None:
        zerado = ""

        for _ in range(tamanho):
            zerado += "0"

        return zerado

    return data_cnab(data)


# caminho contrario do data_cnab, usado na leitura do retorno
# 1. o banco manda a data como 000000 quando o campo nao se aplica
# 2. o ano vem com dois digitos e o CNAB trata todos como 20xx
def data_de_cnab(texto):
    texto = str(texto)

    if len(texto) != 6:
        raise Exception("Data CNAB precisa ter 6 posicoes")

    if texto == "000000":
        return None

    dia = int(texto[0:2])
    mes = int(texto[2:4])
    ano = 2000 + int(texto[4:6])

    return date(ano, mes, dia)