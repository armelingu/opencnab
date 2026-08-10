# dados de um titulo que vai na remessa do Itau
# especie 01 e duplicata mercantil, que e o caso mais comum
# aceite N quer dizer que o pagador nao assinou aceitando o titulo
class BoletoItauCobranca:

    def __init__(self, numero_documento, nosso_numero, valor, vencimento, data_emissao, nome_pagador, documento_pagador, especie="01", aceite="N", uso_da_empresa=""):
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
