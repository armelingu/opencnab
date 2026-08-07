from app.nucleo.campos import alfa
from app.nucleo.campos import branco
from app.nucleo.campos import numerico
from app.nucleo.datas import data_cnab
from app.nucleo.valores import valor_cnab
from app.nucleo.validacoes import tipo_inscricao
from app.bancos.bmp.cnab_400.nosso_numero import gerar_nosso_numero

# registro tipo 1 (detalhe) do CNAB 400
# cada registro tipo 1 representa um titulo enviado para o banco
# o mapa de posicoes esta comentado campo a campo no metodo gerar
class RegistroTipo1BMP:
    def __init__(self, numero_documento, nosso_numero, valor, vencimento, nome_pagador, documento_pagador, sequencial_registro):
        self.numero_documento = numero_documento
        self.nosso_numero = nosso_numero
        self.valor = valor
        self.vencimento = vencimento
        self.nome_pagador = nome_pagador
        self.documento_pagador = documento_pagador
        self.sequencial_registro = sequencial_registro

    def gerar(self):
        nosso_numero_completo = gerar_nosso_numero(self.nosso_numero)
        partes = nosso_numero_completo.split("-")
        nosso_numero_base = partes[0]
        digito_nosso_numero = partes[1]

        campos = []
        campos.append(numerico("1", 1))                              #001-001 identificacao do registro
        campos.append(branco(69))                                    #002-070 uso do banco
        campos.append(numerico(nosso_numero_base, 11))               #071-081 nosso numero
        campos.append(numerico(digito_nosso_numero, 1))              #082-082 digito do nosso numero
        campos.append(branco(27))                                    #083-109 uso do banco
        campos.append(numerico("01", 2))                             #110-111 ocorrencia 01 = entrada de titulo
        campos.append(alfa(self.numero_documento, 10))               #112-121 numero do documento
        campos.append(data_cnab(self.vencimento))                    #122-127 data de vencimento
        campos.append(valor_cnab(self.valor))                        #128-140 valor do titulo
        campos.append(branco(79))                                    #141-219 uso do banco
        campos.append(numerico(tipo_inscricao(self.documento_pagador), 2)) #220-221 01 = CPF e 02 = CNPJ
        campos.append(numerico(self.documento_pagador, 14))          #222-235 cpf ou cnpj do pagador
        campos.append(alfa(self.nome_pagador, 40))                   #236-275 nome do pagador
        campos.append(branco(119))                                   #276-394 endereco e mensagens
        campos.append(numerico(self.sequencial_registro, 6))         #395-400 sequencial do registro

        linha = "".join(campos)

        return linha
