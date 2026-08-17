from opencnab.bancos.bmp.cnab_400 import ocorrencias

# 2 = quem emite o boleto e o cliente e o banco so processa o registro,
# que e o caso de quem usa esta biblioteca para gerar o boleto
CONDICAO_EMISSAO_PELO_CLIENTE = "2"

# N = nao registra para debito automatico
SEM_DEBITO_AUTOMATICO = "N"


class BoletoBMP:

    def __init__(self, numero_documento, nosso_numero, valor, vencimento, nome_pagador, documento_pagador, especie="01", aceite="N", condicao_emissao=CONDICAO_EMISSAO_PELO_CLIENTE, debito_automatico=SEM_DEBITO_AUTOMATICO, data_emissao=None, logradouro_pagador="", cep_pagador="0", mensagem="", sacador_avalista="", instrucao_1="0", instrucao_2="0", juros_por_dia=0, valor_desconto=0, desconto_ate=None, valor_abatimento=0, valor_iof=0, ocorrencia=ocorrencias.ENTRADA):
        self.numero_documento = numero_documento
        self.nosso_numero = nosso_numero
        self.valor = valor
        self.vencimento = vencimento
        self.nome_pagador = nome_pagador
        self.documento_pagador = documento_pagador
        self.especie = especie
        self.aceite = aceite
        self.condicao_emissao = condicao_emissao
        self.debito_automatico = debito_automatico
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
