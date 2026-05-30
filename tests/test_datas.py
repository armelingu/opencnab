from datetime import date
from app.nucleo.datas import data_cnab

def test_data_cnab():
    resultado = data_cnab(date(2026, 5, 30))
    assert resultado == "300526"