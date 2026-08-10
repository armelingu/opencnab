from opencnab.nucleo.campos import alfa
from opencnab.nucleo.campos import branco
from opencnab.nucleo.campos import numerico
from opencnab.nucleo.campos import zeros
from opencnab.nucleo.datas import data_cnab
from opencnab.nucleo.valores import valor_cnab
from opencnab.nucleo.validacoes import tipo_inscricao
from opencnab.bancos.itau.boleto import calcular_dac_conta

CODIGO_BANCO = "341"

OCORRENCIA_ENTRADA = "01"


# registro tipo 1 (detalhe) da remessa do Itau
# diferente do layout derivado do Bradesco, o Itau repete agencia, conta e
# carteira dentro de cada titulo, entao o registro nao depende so do header
# o mapa de posicoes esta comentado campo a campo no metodo gerar
class RegistroTipo1Itau:

    def __init__(self, agencia, conta, carteira, documento_empresa, boleto, sequencial_registro, ocorrencia=OCORRENCIA_ENTRADA):
        self.agencia = agencia
        self.conta = conta
        self.carteira = carteira
        self.documento_empresa = documento_empresa
        self.boleto = boleto
        self.sequencial_registro = sequencial_registro
        self.ocorrencia = ocorrencia

    def gerar(self):
        dac_conta = calcular_dac_conta(self.agencia, self.conta)

        campos = []

        campos.append(numerico("1", 1))                                          #001-001 identificacao do registro
        campos.append(numerico(tipo_inscricao(self.documento_empresa), 2))       #002-003 01 = CPF e 02 = CNPJ da empresa
        campos.append(numerico(self.documento_empresa, 14))                      #004-017 cpf ou cnpj da empresa
        campos.append(numerico(self.agencia, 4))                                 #018-021 agencia da empresa
        campos.append(zeros(2))                                                  #022-023 complemento de registro
        campos.append(numerico(self.conta, 5))                                   #024-028 conta da empresa
        campos.append(dac_conta)                                                 #029-029 digito da agencia com a conta
        campos.append(branco(4))                                                 #030-033 complemento de registro
        campos.append(zeros(4))                                                  #034-037 instrucao a ser cancelada
        campos.append(alfa(self.boleto.uso_da_empresa, 25))                      #038-062 identificacao do titulo na empresa
        campos.append(numerico(self.boleto.nosso_numero, 8))                     #063-070 nosso numero
        campos.append(zeros(13))                                                 #071-083 quantidade de moeda variavel
        campos.append(numerico(self.carteira, 3))                                #084-086 numero da carteira
        campos.append(branco(21))                                                #087-107 uso do banco
        campos.append(alfa("I", 1))                                              #108-108 codigo da carteira
        campos.append(numerico(self.ocorrencia, 2))                              #109-110 ocorrencia 01 = entrada de titulo
        campos.append(alfa(self.boleto.numero_documento, 10))                    #111-120 numero do documento
        campos.append(data_cnab(self.boleto.vencimento))                         #121-126 data de vencimento
        campos.append(valor_cnab(self.boleto.valor))                             #127-139 valor do titulo
        campos.append(numerico(CODIGO_BANCO, 3))                                 #140-142 codigo do banco
        campos.append(zeros(5))                                                  #143-147 agencia cobradora, o banco define
        campos.append(alfa(self.boleto.especie, 2))                              #148-149 especie do titulo
        campos.append(alfa(self.boleto.aceite, 1))                               #150-150 A = aceite e N = sem aceite
        campos.append(data_cnab(self.boleto.data_emissao))                       #151-156 data de emissao do titulo
        campos.append(zeros(2))                                                  #157-158 primeira instrucao de cobranca
        campos.append(zeros(2))                                                  #159-160 segunda instrucao de cobranca
        campos.append(zeros(13))                                                 #161-173 juros por dia de atraso
        campos.append(zeros(6))                                                  #174-179 data limite do desconto
        campos.append(zeros(13))                                                 #180-192 valor do desconto
        campos.append(zeros(13))                                                 #193-205 valor do iof
        campos.append(zeros(13))                                                 #206-218 valor do abatimento
        campos.append(numerico(tipo_inscricao(self.boleto.documento_pagador), 2)) #219-220 01 = CPF e 02 = CNPJ do pagador
        campos.append(numerico(self.boleto.documento_pagador, 14))               #221-234 cpf ou cnpj do pagador
        campos.append(alfa(self.boleto.nome_pagador, 30))                        #235-264 nome do pagador
        campos.append(branco(10))                                                #265-274 complemento de registro
        campos.append(branco(40))                                                #275-314 logradouro do pagador
        campos.append(branco(12))                                                #315-326 bairro do pagador
        campos.append(zeros(8))                                                  #327-334 cep do pagador
        campos.append(branco(15))                                                #335-349 cidade do pagador
        campos.append(branco(2))                                                 #350-351 uf do pagador
        campos.append(branco(30))                                                #352-381 nome do sacador ou avalista
        campos.append(branco(4))                                                 #382-385 complemento de registro
        campos.append(zeros(6))                                                  #386-391 data de mora
        campos.append(zeros(2))                                                  #392-393 quantidade de dias
        campos.append(branco(1))                                                 #394-394 complemento de registro
        campos.append(numerico(self.sequencial_registro, 6))                     #395-400 sequencial do registro

        linha = "".join(campos)

        if len(linha) != 400:
            raise Exception("Registro de detalhe do Itau saiu com " + str(len(linha)) + " posicoes em vez de 400")

        return linha
