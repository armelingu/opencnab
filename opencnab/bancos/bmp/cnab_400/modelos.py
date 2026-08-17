from opencnab.bancos.bmp.cnab_400 import ocorrencias


class BoletoBMP:

    def __init__(self, numero_documento, nosso_numero, valor, vencimento, nome_pagador, documento_pagador, especie="01", aceite="N", data_emissao=None, logradouro_pagador="", cep_pagador="0", mensagem="", sacador_avalista="", instrucao_1="0", instrucao_2="0", juros_por_dia=0, valor_desconto=0, desconto_ate=None, valor_abatimento=0, valor_iof=0, ocorrencia=ocorrencias.ENTRADA):
        self.numero_documento = numero_documento
        self.nosso_numero = nosso_numero
        self.valor = valor
        self.vencimento = vencimento
        self.nome_pagador = nome_pagador
        self.documento_pagador = documento_pagador
        self.especie = especie
        self.aceite = aceite
        self.data_emissao = data_emissao
        self.logradouro_pagador = logradouro_pagador
        self.cep_pagador = cep_pagador
        self.mensagem = mensagem
        self.sacador_avalista = sacador_avalista
        self.instrucao_1 = instrucao_1
        self.instrucao_2 = instrucao_2
        self.juros_por_dia = juros_por_dia
        self.valor_desconto = valor_desconto
        self.desconto_ate = desconto_ate
        self.valor_abatimento = valor_abatimento
        self.valor_iof = valor_iof
        self.ocorrencia = ocorrencia
