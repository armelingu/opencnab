# Exemplos BMP CNAB 400

Os scripts mostram a geração de remessa e a leitura de retorno usando os
imports públicos do pacote. Execute os comandos a partir da raiz do repositório,
com a biblioteca instalada no ambiente Python:

```bash
python -m pip install -e ".[dev]"
```

## Gerar uma remessa

```bash
python tests/exemplos/gerar_remessa_bmp.py /tmp/remessa-exemplo.rem
```

O script grava uma remessa com dois títulos fictícios, um header e um trailer.
O caminho de saída é obrigatório; se já existir um arquivo nesse caminho,
ele será substituído. Use um caminho reservado para o exemplo.

O resultado tem quatro registros de 400 posições, separados por CRLF, em
ASCII. O nome do primeiro pagador é gravado sem acentos. O programa informa
o caminho gravado e a quantidade de títulos:

```text
Remessa gravada em: /tmp/remessa-exemplo.rem
Quantidade de titulos: 2
```

Datas, documentos, código da empresa e nomes são dados de demonstração.
O script não transmite arquivos ao banco. Para uma integração real, preencha
os dados do contrato e confira o arquivo no processo de homologação do banco.

## Ler um retorno

```bash
python tests/exemplos/ler_retorno_bmp.py /caminho/do/retorno.ret
```

Substitua o caminho pelo arquivo de retorno BMP recebido do banco. O script
abre o arquivo em Latin-1 e mostra os dados da empresa, a quantidade de
títulos, as ocorrências, os títulos pagos e o total pago.

A remessa gerada pelo primeiro exemplo não serve como entrada deste script.
Ela contém as instruções enviadas ao banco; o retorno contém as ocorrências
que o banco devolve. Uma entrada confirmada não é um pagamento.

O script apenas lê o arquivo e imprime os resultados, sem alterar o retorno.
Os valores lidos são `Decimal`. Na primeira integração, confira o total com
o extrato e as posições do layout com o manual do banco.

Os dois scripts também aceitam `--help` para consultar os argumentos.
