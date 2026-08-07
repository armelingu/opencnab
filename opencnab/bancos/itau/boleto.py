from opencnab.nucleo.campos import numerico
from opencnab.nucleo.modulo10 import calcular_digito_verificador
from opencnab.boletos.codigo_barras import gerar_codigo_barras
from opencnab.boletos.linha_digitavel import gerar_linha_digitavel
from opencnab.boletos.linha_digitavel import formatar_linha_digitavel

CODIGO_BANCO = "341"


# o digito do nosso numero no Itau sai do modulo 10 sobre a juncao de
# agencia, conta, carteira e nosso numero, nessa ordem
def calcular_dac_nosso_numero(agencia, conta, carteira, nosso_numero):
    base = numerico(agencia, 4) + numerico(conta, 5) + numerico(carteira, 3) + numerico(nosso_numero, 8)

    digito = calcular_digito_verificador(base)

    return str(digito)


# o digito da conta sai do modulo 10 sobre agencia e conta
def calcular_dac_conta(agencia, conta):
    base = numerico(agencia, 4) + numerico(conta, 5)

    digito = calcular_digito_verificador(base)

    return str(digito)


# boleto do Itau, usado para montar o codigo de barras e a linha digitavel
# as 25 posicoes do campo livre do Itau sao:
# 001-003 carteira, 004-011 nosso numero, 012-012 digito do nosso numero,
# 013-016 agencia, 017-021 conta, 022-022 digito da conta e 023-025 zeros
class BoletoItau:

    def __init__(self, agencia, conta, carteira, nosso_numero, valor, vencimento):
        self.agencia = agencia
        self.conta = conta
        self.carteira = carteira
        self.nosso_numero = nosso_numero
        self.valor = valor
        self.vencimento = vencimento

    def gerar_campo_livre(self):
        dac_nosso_numero = calcular_dac_nosso_numero(self.agencia, self.conta, self.carteira, self.nosso_numero)
        dac_conta = calcular_dac_conta(self.agencia, self.conta)

        campos = []

        campos.append(numerico(self.carteira, 3))       #001-003 carteira
        campos.append(numerico(self.nosso_numero, 8))   #004-011 nosso numero
        campos.append(dac_nosso_numero)                 #012-012 digito do nosso numero
        campos.append(numerico(self.agencia, 4))        #013-016 agencia
        campos.append(numerico(self.conta, 5))          #017-021 conta
        campos.append(dac_conta)                        #022-022 digito da conta
        campos.append(numerico("0", 3))                 #023-025 zeros fixos do layout

        campo_livre = "".join(campos)

        return campo_livre

    def gerar_codigo_barras(self):
        campo_livre = self.gerar_campo_livre()

        codigo = gerar_codigo_barras(CODIGO_BANCO, self.valor, self.vencimento, campo_livre)

        return codigo

    def gerar_linha_digitavel(self):
        linha = gerar_linha_digitavel(self.gerar_codigo_barras())

        return linha

    def gerar_linha_digitavel_formatada(self):
        linha = formatar_linha_digitavel(self.gerar_linha_digitavel())

        return linha
