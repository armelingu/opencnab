from opencnab.nucleo.campos import alfa
from opencnab.nucleo.campos import branco
from opencnab.nucleo.campos import numerico
from opencnab.nucleo.campos import zeros
from opencnab.nucleo.datas import data_ou_zeros
from opencnab.nucleo.valores import valor_cnab
from opencnab.nucleo.valores import valor_de_cnab
from opencnab.nucleo.validacoes import somente_numeros
from opencnab.nucleo.validacoes import tipo_inscricao
from opencnab.nucleo.validacoes import tipo_inscricao_ou_zeros
from opencnab.bancos.itau.boleto import calcular_dac_conta
from opencnab.bancos.itau.cnab_400 import instrucoes
from opencnab.bancos.itau.cnab_400 import ocorrencias

CODIGO_BANCO = "341"


# manual de setembro de 2026, paginas 23 e 24 e notas 35 a 37
# a primeira entrega aceita multa na entrada; alteracao usa a ocorrencia 49
def validar_multa(boleto):
    if boleto.ocorrencia != ocorrencias.ENTRADA:
        raise Exception("Multa disponivel somente na entrada de titulo novo")

    codigo = str(boleto.multa.codigo)

    if codigo not in ["0", "1", "2"]:
        raise Exception("Codigo da multa precisa ser 0, 1 ou 2")

    if boleto.multa.data is None:
        raise Exception("Multa precisa de data")

    if boleto.vencimento is None:
        raise Exception("Multa precisa do vencimento do titulo")

    if boleto.multa.data < boleto.vencimento:
        raise Exception("Data da multa nao pode ser anterior ao vencimento")

    # conferimos o valor que sera gravado, inclusive depois do arredondamento
    valor_multa = valor_de_cnab(valor_cnab(boleto.multa.valor))

    if codigo == "1":
        valor_titulo = valor_de_cnab(valor_cnab(boleto.valor))

        if valor_multa >= valor_titulo:
            raise Exception("Multa em reais precisa ser menor que o valor do titulo")

    if codigo == "2" and valor_multa >= 100:
        raise Exception("Percentual da multa precisa ser menor que 100")


# o registro tipo 2 complementa o tipo 1 e tem seu proprio sequencial
class RegistroMultaItau:

    def __init__(self, boleto, sequencial_registro):
        self.boleto = boleto
        self.sequencial_registro = sequencial_registro

    def gerar(self):
        validar_multa(self.boleto)

        campos = []

        campos.append(numerico("2", 1))                          #001-001 identificacao do registro
        campos.append(numerico(self.boleto.multa.codigo, 1))      #002-002 codigo da multa
        campos.append(self.boleto.multa.data.strftime("%d%m%Y")) #003-010 data da multa em DDMMAAAA
        campos.append(valor_cnab(self.boleto.multa.valor))        #011-023 valor em reais ou percentual
        campos.append(branco(371))                               #024-394 complemento de registro
        campos.append(numerico(self.sequencial_registro, 6))     #395-400 sequencial do registro

        linha = "".join(campos)

        if len(linha) != 400:
            raise Exception("Registro de multa do Itau saiu com " + str(len(linha)) + " posicoes em vez de 400")

        return linha


# confere o que o banco rejeitaria ou entenderia errado
# 1. instrucao que precisa de prazo sem o prazo informado o banco ignora
# 2. protestar e nao protestar no mesmo titulo e uma contradicao
# 3. desconto sem data limite o banco nao sabe ate quando conceder
# 4. o Banco Central nao aceita titulo novo sem vencimento nem sem valor,
#    mas em comando sobre titulo ja registrado esses campos podem faltar
def validar_boleto(boleto):
    if boleto.ocorrencia == ocorrencias.ENTRADA:
        if boleto.vencimento is None:
            raise Exception("Titulo novo precisa de data de vencimento")

        if boleto.valor == 0:
            raise Exception("Titulo novo precisa de valor")

        if somente_numeros(boleto.documento_pagador) == "":
            raise Exception("Titulo novo precisa do CPF ou CNPJ do pagador")

    if instrucoes.pede_quantidade_de_dias(boleto.instrucao_1) and boleto.dias_da_instrucao == 0:
        raise Exception("A instrucao " + boleto.instrucao_1 + " precisa da quantidade de dias")

    if instrucoes.pede_quantidade_de_dias(boleto.instrucao_2) and boleto.dias_da_instrucao == 0:
        raise Exception("A instrucao " + boleto.instrucao_2 + " precisa da quantidade de dias")

    if instrucoes.e_instrucao_de_protesto(boleto.instrucao_1) and boleto.instrucao_2 == instrucoes.NAO_PROTESTAR:
        raise Exception("Nao da para mandar protestar e nao protestar no mesmo titulo")

    if instrucoes.e_instrucao_de_protesto(boleto.instrucao_2) and boleto.instrucao_1 == instrucoes.NAO_PROTESTAR:
        raise Exception("Nao da para mandar protestar e nao protestar no mesmo titulo")

    if boleto.valor_desconto != 0 and boleto.desconto_ate is None:
        raise Exception("Desconto informado sem a data limite para conceder")


# registro tipo 1 (detalhe) da remessa do Itau
# diferente do layout derivado do Bradesco, o Itau repete agencia, conta e
# carteira dentro de cada titulo, entao o registro nao depende so do header
# o mapa de posicoes esta comentado campo a campo no metodo gerar
class RegistroTipo1Itau:

    def __init__(self, agencia, conta, carteira, documento_empresa, boleto, sequencial_registro):
        self.agencia = agencia
        self.conta = conta
        self.carteira = carteira
        self.documento_empresa = documento_empresa
        self.boleto = boleto
        self.sequencial_registro = sequencial_registro

    def gerar(self):
        validar_boleto(self.boleto)

        dac_conta = calcular_dac_conta(self.agencia, self.conta)

        logradouro = ""
        bairro = ""
        cep = "0"
        cidade = ""
        uf = ""

        if self.boleto.endereco_pagador is not None:
            logradouro = self.boleto.endereco_pagador.logradouro
            bairro = self.boleto.endereco_pagador.bairro
            cep = self.boleto.endereco_pagador.cep
            cidade = self.boleto.endereco_pagador.cidade
            uf = self.boleto.endereco_pagador.uf

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
        campos.append(numerico(self.boleto.ocorrencia, 2))                       #109-110 o que o banco deve fazer com o titulo
        campos.append(alfa(self.boleto.numero_documento, 10))                    #111-120 numero do documento
        campos.append(data_ou_zeros(self.boleto.vencimento))                     #121-126 data de vencimento
        campos.append(valor_cnab(self.boleto.valor))                             #127-139 valor do titulo
        campos.append(numerico(CODIGO_BANCO, 3))                                 #140-142 codigo do banco
        campos.append(zeros(5))                                                  #143-147 agencia cobradora, o Itau define pelo cep
        campos.append(alfa(self.boleto.especie, 2))                              #148-149 especie do titulo
        campos.append(alfa(self.boleto.aceite, 1))                               #150-150 A = aceite e N = sem aceite
        campos.append(data_ou_zeros(self.boleto.data_emissao))                   #151-156 data de emissao do titulo
        campos.append(alfa(self.boleto.instrucao_1, 2))                          #157-158 primeira instrucao de cobranca
        campos.append(alfa(self.boleto.instrucao_2, 2))                          #159-160 segunda instrucao de cobranca
        campos.append(valor_cnab(self.boleto.juros_por_dia))                     #161-173 juros por dia de atraso
        campos.append(data_ou_zeros(self.boleto.desconto_ate))                   #174-179 data limite do desconto
        campos.append(valor_cnab(self.boleto.valor_desconto))                    #180-192 valor do desconto
        campos.append(valor_cnab(self.boleto.valor_iof))                         #193-205 valor do iof
        campos.append(valor_cnab(self.boleto.valor_abatimento))                  #206-218 valor do abatimento
        campos.append(numerico(tipo_inscricao_ou_zeros(self.boleto.documento_pagador), 2)) #219-220 01 = CPF e 02 = CNPJ do pagador
        campos.append(numerico(self.boleto.documento_pagador, 14))               #221-234 cpf ou cnpj do pagador
        campos.append(alfa(self.boleto.nome_pagador, 30))                        #235-264 nome do pagador
        campos.append(branco(10))                                                #265-274 complemento de registro
        campos.append(alfa(logradouro, 40))                                      #275-314 logradouro do pagador
        campos.append(alfa(bairro, 12))                                          #315-326 bairro do pagador
        campos.append(numerico(cep, 8))                                          #327-334 cep do pagador
        campos.append(alfa(cidade, 15))                                          #335-349 cidade do pagador
        campos.append(alfa(uf, 2))                                               #350-351 uf do pagador
        campos.append(alfa(self.boleto.sacador_avalista, 30))                    #352-381 nome do sacador ou avalista
        campos.append(branco(4))                                                 #382-385 complemento de registro
        campos.append(data_ou_zeros(self.boleto.data_mora))                      #386-391 data a partir da qual conta a mora
        campos.append(numerico(self.boleto.dias_da_instrucao, 2))                #392-393 quantidade de dias da instrucao
        campos.append(branco(1))                                                 #394-394 complemento de registro
        campos.append(numerico(self.sequencial_registro, 6))                     #395-400 sequencial do registro

        linha = "".join(campos)

        if len(linha) != 400:
            raise Exception("Registro de detalhe do Itau saiu com " + str(len(linha)) + " posicoes em vez de 400")

        return linha
