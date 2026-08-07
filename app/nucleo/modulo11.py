# pegue o numero 123456
# leia da direita para a esquerda
# multiplique a posicao do digito do numero na lista de arrays
# ex.: 123 -> 1 * 3 ; 2 * 2 e 3 * 1


def calcular_digito_verificador(numero):
    multiplicador = 2
    soma_total = 0

    for digito_texto in numero[::-1]:
        digito_numero = int(digito_texto)

        resultado_multiplicacao = digito_numero * multiplicador

        soma_total = soma_total + resultado_multiplicacao

        multiplicador = multiplicador + 1

        if multiplicador > 7:
            multiplicador = 2

    resto_divisao = soma_total % 11

    digito_verificador = 11 - resto_divisao

    if digito_verificador == 10:
        digito_verificador = 0
    if digito_verificador == 11:
        digito_verificador = 0
    return digito_verificador


# o digito geral do codigo de barras tambem usa modulo 11
# mas com pesos de 2 a 9 e uma regra de resto diferente:
# quando o resultado da 0, 10 ou 11 o digito e sempre 1
def calcular_digito_codigo_barras(numero):
    multiplicador = 2
    soma_total = 0

    for digito_texto in numero[::-1]:
        digito_numero = int(digito_texto)

        soma_total = soma_total + digito_numero * multiplicador

        multiplicador = multiplicador + 1

        if multiplicador > 9:
            multiplicador = 2

    resto_divisao = soma_total % 11

    digito_verificador = 11 - resto_divisao

    if digito_verificador == 0:
        digito_verificador = 1
    if digito_verificador > 9:
        digito_verificador = 1

    return digito_verificador