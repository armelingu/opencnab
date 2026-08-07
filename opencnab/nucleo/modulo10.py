'''
1. Ler da direita para esquerda
2. Multiplicar alternando 2 e 1
3. Se resultado > 9
       somar os dígitos
4. Somar tudo
5. Descobrir próximo múltiplo de 10
6. Retornar o dígito
'''


def calcular_digito_verificador(numero):
    multiplicador = 2
    soma = 0

    for digito in numero[::-1]:
        digito = int(digito)
        resultado = digito * multiplicador
        if resultado > 9:
            resultado = int(str(resultado)[0]) + int(str(resultado)[1])
        soma = soma + resultado
        if multiplicador == 2:
            multiplicador = 1
        else:
            multiplicador = 2
    proximo_multiplo = soma
    while proximo_multiplo % 10 != 0:
        proximo_multiplo = proximo_multiplo + 1
    digito_verificador = proximo_multiplo - soma
    return digito_verificador