from datetime import date

# transforam o formato de data 00/00/0000
# no padrao cnab 000000
def data_cnab(data):
    data_texto = data.strftime("%d%m%y")
    return data_texto