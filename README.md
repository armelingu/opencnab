# OpenCNAB

OpenCNAB é uma biblioteca Python para trabalhar com arquivos CNAB, focada em CNAB 400 e suporte inicial ao banco BMP.

## Visão geral

O projeto oferece utilitários para:
- gerar registros de remessa em formato CNAB 400
- formatar campos de data e valores para CNAB
- gerar "nosso número" com dígito verificador
- representar boletos e dados de cobrança

## Recursos atuais

- Cabeçalho de remessa para BMP Money Plus (CNAB 400)
- Registro tipo 1 para BMP (CNAB 400)
- Geração de "nosso número" com cálculo do dígito verificador
- Modelos de boleto para uso interno
- Validação e formatação de campos CNAB

## Requisitos

- Python 3.11 ou superior

## Instalação

Para instalar localmente:

```bash
git clone https://github.com/armelingu/opencnab.git
cd opencnab
pip install .
```

Para instalar dependências de desenvolvimento:

```bash
pip install -e .[dev]
```

## Uso

### Gerar nosso número

```python
from app.bancos.bmp.cnab_400.nosso_numero import gerar_nosso_numero

nosso_numero = gerar_nosso_numero("12345")
print(nosso_numero)  # Ex: 00000012345-<digito>
```

### Gerar cabeçalho de remessa BMP CNAB 400

```python
from datetime import date
from app.bancos.bmp.cnab_400.remessa import HeaderRemessaBMP

header = HeaderRemessaBMP(
    codigo_empresa="123",
    nome_empresa="EMPRESA TESTE",
    data_geracao=date(2026, 6, 5),
    sequencial_remessa=1
)
linha_header = header.gerar()
print(len(linha_header))  # 400
```

### Gerar registro tipo 1 BMP CNAB 400

```python
from datetime import date
from app.bancos.bmp.cnab_400.registros import RegistroTipo1BMP

registro = RegistroTipo1BMP(
    numero_documento="NF001",
    valor=150.70,
    vencimento=date(2026, 6, 30),
    nome_pagador="CLIENTE TESTE",
    documento_pagador="12345678901",
    sequencial_registro=2
)
linha_registro = registro.gerar()
print(len(linha_registro))  # 400
```

### Criar boleto BMP

```python
from datetime import date
from app.bancos.bmp.cnab_400.modelos import BoletoBMP

boleto = BoletoBMP(
    numero_documento="NF001",
    nosso_numero="0000000001",
    valor=150.75,
    vencimento=date(2026, 6, 30),
    nome_pagador="CLIENTE TESTE",
    documento_pagador="12345678901"
)
print(boleto.numero_documento)
```

## Testes

Execute a suíte de testes com:

```bash
pytest
```

## Estrutura do projeto

- `app/bancos/bmp/cnab_400/` - implementação de BMP CNAB 400
- `app/boletos/` - classes auxiliares para boletos
- `app/nucleo/` - formatação de campos, datas, valores e validações
- `tests/` - casos de teste para as funcionalidades

## Limitações e escopo

Atualmente, o foco principal é o suporte a BMP no formato CNAB 400. O projeto pode ser ampliado para outros bancos e formatos em versões futuras.

## Licença

Consulte o arquivo `LICENSE` para detalhes sobre a licença do projeto.
