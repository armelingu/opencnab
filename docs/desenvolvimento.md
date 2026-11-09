# Desenvolvimento

`main` contém a versão estável. `develop` reúne as entregas da próxima versão.
O trabalho de cada task começa em uma branch própria criada de `develop`
atualizada. Use o checkout existente do ambiente.

## Branches e commits

O nome da branch segue `tipo/escopo-descricao`, por exemplo:

```text
fix/retorno-leitura-repetida
feat/itau-registro-multa
test/nucleo-limites-dos-campos
docs/arquitetura-e-roadmap
ci/testes-python
```

Use os tipos `feat`, `fix`, `refactor`, `test`, `docs`, `ci` e `hotfix`.
Faça commits por avanço coerente, com mensagens em português e prefixo
correspondente ao trabalho:

```text
test/itau: reproduz os casos de multa do manual
feat/itau: gera registro de multa na remessa
docs/itau: explica os campos de multa
```

Uma entrega pode ter vários commits. Inclua todos os arquivos pertinentes;
credenciais, ambientes virtuais, arquivos temporários e saídas geradas ficam
fora do Git. Antes de commitar, confira `git status` e o diff. Use a identidade
Git do autor configurada para o projeto e confira nome e e-mail.

## Validação e PR

Instale as dependências de desenvolvimento e execute a suíte:

```bash
python -m pip install -e ".[dev]"
python -m pip check
python -m pytest -q
```

Execute os testes relevantes durante a implementação e a suíte completa
antes de apresentar mudanças de comportamento para revisão. Para documentação,
confira a exatidão do conteúdo, os links locais e os comandos fornecidos.

Envie a branch e abra um único PR para `develop` reunindo a entrega. Um PR
em rascunho pode ser aberto durante o trabalho; marque como pronto depois
de completar o escopo e as verificações. A descrição precisa explicar o
problema, o comportamento resultante, os testes e mudanças na API ou no CNAB.

Mantenha correções e funcionalidades sem relação em entregas separadas.
O GitHub Actions executa os testes em Python 3.11, 3.12 e 3.13. Confira seus
resultados e aguarde a revisão antes do merge.

## Integração e versões

O padrão combinado para tasks é squash merge em `develop`, deixando uma
entrada por entrega no histórico de integração. A entrega de versão usa
um PR de `develop` para `main`, com merge commit para preservar a relação
entre as branches. Cada versão publicada recebe uma tag, como `v0.8.1`.

Correções urgentes partem de `main` em uma branch `hotfix/...`. Depois de
integradas, precisam chegar também a `develop`. Remova branches de tasks
após o merge e preserve o histórico, sem force push nas branches compartilhadas.

O fluxo descreve o acordo de trabalho; as proteções de branch e verificações
obrigatórias dependem das configurações existentes no GitHub.
