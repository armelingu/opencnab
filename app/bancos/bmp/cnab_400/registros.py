from app.nucleo.campos import alfa
from app.nucleo.campos import branco
from app.nucleo.campos import numerico
from app.nucleo.datas import data_cnab
from app.nucleo.valores import valor_cnab

class RegistroTipo1BMP:
    def __init__(self, numero_documento, valor, vencimento, nome_pagador, documento_pagador, sequencial_registro):
        self.numero_documento = numero_documento
        self.valor = valor
        self.vencimento = vencimento
        self.nome_pagador = nome_pagador
        self.documento_pagador = documento_pagador
        self.sequencial_registro = sequencial_registro

    def gerar(self):
        campos = []
        campos.append(numerico("1", 1))
        campos.append(branco(108))
        campos.append(numerico("01", 2))
        campos.append(alfa(self.numero_documento, 10))

        campos.append(data_cnab(self.vencimento))
        campos.append(valor_cnab(self.valor))
        campos.append(branco(79))
        campos.append(numerico("01", 2))
        campos.append(numerico(self.documento_pagador,14))
        campos.append(alfa(self.nome_pagador,40))
        campos.append(branco(119))
        campos.append(numerico(self.sequencial_registro,6))

        linha = "".join(campos)

        return linha