from app.bancos.bmp.cnab_400.remessa import TrailerRemessaBMP


def test_trailer_400_posicoes():
    trailer = TrailerRemessaBMP(sequencial_registro=3)
    linha = trailer.gerar()
    assert len(linha) == 400


def test_trailer_comeca_com_9():
    trailer = TrailerRemessaBMP(sequencial_registro=3)
    linha = trailer.gerar()
    assert linha[0:1] == "9"


def test_trailer_sequencial():
    trailer = TrailerRemessaBMP(sequencial_registro=3)
    linha = trailer.gerar()
    assert linha[394:400] == "000003"
