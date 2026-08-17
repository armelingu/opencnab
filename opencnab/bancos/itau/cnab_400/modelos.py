from opencnab.bancos.itau.cnab_400 import instrucoes


# endereco do pagador, que vai nas posicoes 275 a 351 do registro de detalhe
# vale a pena preencher: o Itau usa o CEP para decidir a agencia cobradora
# e o endereco e o que sai impresso no boleto entregue ao pagador
class EnderecoPagador:

    def __init__(self, logradouro, bairro, cep, cidade, uf):
        self.logradouro = logradouro
        self.bairro = bairro
        self.cep = cep
        self.cidade = cidade
        self.uf = uf


# dados de um titulo que vai na remessa do Itau
# especie 01 e duplicata mercantil, que e o caso mais comum
# aceite N quer dizer que o pagador nao assinou aceitando o titulo
# tudo que vem depois de documento_pagador e opcional: sem informar nada o
# titulo e registrado do jeito mais simples, so com a cobranca
class BoletoItauCobranca:

    def __init__(self, numero_documento, nosso_numero, valor, vencimento, data_emissao, nome_pagador, documento_pagador, especie="01", aceite="N", uso_da_empresa="", endereco_pagador=None, juros_por_dia=0, data_mora=None, valor_desconto=0, desconto_ate=None, valor_abatimento=0, valor_iof=0, instrucao_1=instrucoes.SEM_INSTRUCAO, instrucao_2=instrucoes.SEM_INSTRUCAO, dias_da_instrucao=0, sacador_avalista=""):
        self.numero_documento = numero_documento
        self.nosso_numero = nosso_numero
        self.valor = valor
        self.vencimento = vencimento
        self.data_emissao = data_emissao
        self.nome_pagador = nome_pagador
        self.documento_pagador = documento_pagador
        self.especie = especie
        self.aceite = aceite
        self.uso_da_empresa = uso_da_empresa
        self.endereco_pagador = endereco_pagador
        self.juros_por_dia = juros_por_dia
        self.data_mora = data_mora
        self.valor_desconto = valor_desconto
        self.desconto_ate = desconto_ate
        self.valor_abatimento = valor_abatimento
        self.valor_iof = valor_iof
        self.instrucao_1 = instrucao_1
        self.instrucao_2 = instrucao_2
        self.dias_da_instrucao = dias_da_instrucao
        self.sacador_avalista = sacador_avalista
