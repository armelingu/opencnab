from opencnab.nucleo.modulo10 import calcular_digito_verificador

'''
a linha digitavel e o proprio codigo de barras embaralhado em 5 campos,
para a pessoa conseguir digitar quando o leitor nao le o codigo:

1. campo 1: banco + moeda + as 5 primeiras posicoes do campo livre + digito
2. campo 2: as 10 posicoes seguintes do campo livre + digito
3. campo 3: as 10 ultimas posicoes do campo livre + digito
4. campo 4: o digito geral do codigo de barras
5. campo 5: fator de vencimento + valor

os digitos dos campos 1, 2 e 3 sao calculados em modulo 10
'''


def gerar_linha_digitavel(codigo_barras):
    if len(codigo_barras) != 44:
        raise Exception("Codigo de barras precisa ter 44 posicoes")

    banco = codigo_barras[0:3]
    moeda = codigo_barras[3:4]
    digito_geral = codigo_barras[4:5]
    fator_e_valor = codigo_barras[5:19]
    campo_livre = codigo_barras[19:44]

    primeiro = banco + moeda + campo_livre[0:5]
    segundo = campo_livre[5:15]
    terceiro = campo_livre[15:25]

    primeiro = primeiro + str(calcular_digito_verificador(primeiro))
    segundo = segundo + str(calcular_digito_verificador(segundo))
    terceiro = terceiro + str(calcular_digito_verificador(terceiro))

    linha = primeiro + segundo + terceiro + digito_geral + fator_e_valor

    return linha


# deixa a linha no formato que aparece impresso no boleto
# ex.: 27490.12345 67890.123456 78901.234567 8 12340000015070
def formatar_linha_digitavel(linha):
    if len(linha) != 47:
        raise Exception("Linha digitavel precisa ter 47 posicoes")

    campos = []

    campos.append(linha[0:5] + "." + linha[5:10])
    campos.append(linha[10:15] + "." + linha[15:21])
    campos.append(linha[21:26] + "." + linha[26:32])
    campos.append(linha[32:33])
    campos.append(linha[33:47])

    return " ".join(campos)
