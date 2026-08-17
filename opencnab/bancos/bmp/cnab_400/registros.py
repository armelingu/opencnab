from opencnab.nucleo.campos import alfa
from opencnab.nucleo.campos import branco
from opencnab.nucleo.campos import numerico
from opencnab.nucleo.campos import zeros
from opencnab.nucleo.datas import data_ou_zeros
from opencnab.nucleo.valores import valor_cnab
from opencnab.nucleo.validacoes import somente_numeros
from opencnab.nucleo.validacoes import tipo_inscricao_ou_zeros
from opencnab.bancos.bmp.cnab_400.nosso_numero import gerar_nosso_numero
from opencnab.bancos.bmp.cnab_400 import ocorrencias


# so o titulo novo precisa dos dados completos
# o comando vai sobre um titulo que o banco ja tem, entao identifica pelo
# nosso numero e o layout manda zerar o resto
def validar_boleto(boleto):
    if boleto.ocorrencia == ocorrencias.ENTRADA:
        if boleto.vencimento is None:
            raise Exception("Titulo novo precisa de data de vencimento")

        if boleto.valor == 0:
            raise Exception("Titulo novo precisa de valor")

        if somente_numeros(boleto.documento_pagador) == "":
            raise Exception("Titulo novo precisa do CPF ou CNPJ do pagador")


# registro tipo 1 (detalhe) do CNAB 400
# cada registro tipo 1 representa um titulo enviado para o banco
# o mapa de posicoes esta comentado campo a campo no metodo gerar
class RegistroTipo1BMP:
    def __init__(self, boleto, sequencial_registro):
        self.boleto = boleto
        self.sequencial_registro = sequencial_registro

    def gerar(self):
        validar_boleto(self.boleto)

        nosso_numero_completo = gerar_nosso_numero(self.boleto.nosso_numero)
        partes = nosso_numero_completo.split("-")
        nosso_numero_base = partes[0]
        digito_nosso_numero = partes[1]

        campos = []
        campos.append(numerico("1", 1))                                          #001-001 identificacao do registro
        campos.append(branco(69))                                                #002-070 uso do banco
        campos.append(numerico(nosso_numero_base, 11))                           #071-081 nosso numero
        campos.append(numerico(digito_nosso_numero, 1))                          #082-082 digito do nosso numero
        campos.append(zeros(10))                                                 #083-092 desconto bonificacao por dia
        campos.append(alfa(self.boleto.condicao_emissao, 1))                     #093-093 condicao de emissao do boleto
        campos.append(alfa(self.boleto.debito_automatico, 1))                    #094-094 emissao de boleto para debito automatico
        campos.append(branco(10))                                                #095-104 uso do banco
        campos.append(branco(1))                                                 #105-105 indicador de rateio de credito
        campos.append(branco(1))                                                 #106-106 endereco para aviso de debito automatico
        campos.append(branco(2))                                                 #107-108 uso do banco
        campos.append(numerico(self.boleto.ocorrencia, 2))                       #109-110 o que o banco deve fazer com o titulo
        campos.append(alfa(self.boleto.numero_documento, 10))                    #111-120 numero do documento
        campos.append(data_ou_zeros(self.boleto.vencimento))                     #121-126 data de vencimento
        campos.append(valor_cnab(self.boleto.valor))                             #127-139 valor do titulo
        campos.append(zeros(3))                                                  #140-142 banco encarregado da cobranca
        campos.append(zeros(5))                                                  #143-147 agencia depositaria
        campos.append(numerico(self.boleto.especie, 2))                          #148-149 especie do titulo
        campos.append(alfa(self.boleto.aceite, 1))                               #150-150 A = aceite e N = sem aceite
        campos.append(data_ou_zeros(self.boleto.data_emissao))                   #151-156 data de emissao do titulo
        campos.append(numerico(self.boleto.instrucao_1, 2))                      #157-158 primeira instrucao de cobranca
        campos.append(numerico(self.boleto.instrucao_2, 2))                      #159-160 segunda instrucao de cobranca
        campos.append(valor_cnab(self.boleto.juros_por_dia))                     #161-173 juros por dia de atraso
        campos.append(data_ou_zeros(self.boleto.desconto_ate))                   #174-179 data limite do desconto
        campos.append(valor_cnab(self.boleto.valor_desconto))                    #180-192 valor do desconto
        campos.append(valor_cnab(self.boleto.valor_iof))                         #193-205 valor do iof
        campos.append(valor_cnab(self.boleto.valor_abatimento))                  #206-218 valor do abatimento
        campos.append(numerico(tipo_inscricao_ou_zeros(self.boleto.documento_pagador), 2)) #219-220 01 = CPF e 02 = CNPJ do pagador
        campos.append(numerico(self.boleto.documento_pagador, 14))               #221-234 cpf ou cnpj do pagador
        campos.append(alfa(self.boleto.nome_pagador, 40))                        #235-274 nome do pagador
        campos.append(alfa(self.boleto.logradouro_pagador, 40))                  #275-314 logradouro do pagador
        campos.append(alfa(self.boleto.mensagem, 12))                            #315-326 primeira mensagem do boleto
        campos.append(numerico(self.boleto.cep_pagador, 8))                      #327-334 cep do pagador
        campos.append(alfa(self.boleto.sacador_avalista, 60))                    #335-394 sacador avalista ou segunda mensagem
        campos.append(numerico(self.sequencial_registro, 6))                     #395-400 sequencial do registro

        linha = "".join(campos)

        if len(linha) != 400:
            raise Exception("Registro de detalhe do BMP saiu com " + str(len(linha)) + " posicoes em vez de 400")

        return linha
