# Entrega — Consolidador de Reservas Onfly

## 1. Defeitos Corrigidos (código)

Durante a investigação guiada pelos testes do `pytest`, IA e pela amostra de validação, foram identificados 5 defeitos principais:

1.1. **Cálculo de Noites (`stay_calculator.py`)**
   * **Dor:** Reservas que viravam o mês resultavam em noites negativas (ex: `-28` noites na virada de janeiro para fevereiro).
   * **Causa Raiz:** O código subtraía o dia do mês (`checkout.day - checkin.day`) em vez de calcular a diferença real entre as datas `(checkout - checkin).days`.
   * **Correção:** Alterei para `(checkout - checkin).days * rooms` para evitar noites negativas caso o checkout seja menor que o checkin, dessa forma, o resultado (certo ou errado) retorna mais rápido e é mais fácil de ser corrigido, caso falhe.
   * **Cobertura:** `test_nights_across_month_boundary`; teste pessoal `test_room_nights_with_zero_rooms`

1.2. **Conversão de Câmbio invertido e `float` (`currency_converter.py`)**
   * **Dor:** O total em BRL ´total_amount_brl´ ficava muito abaixo do esperado (ex: `118.45` em vez de `642.00`).
   * **Causa Raiz:** O código estava **dividindo** o valor pela taxa de câmbio (`amount / rate`) e utilizando `float`, o que feria a regra de exatidão.
   * **Correção:** Alterei para multiplicação (`return amount * rate`) mantendo o tipo `Decimal`, sem conversões desnecessárias para float, tentando ao máximo manter um código limpo e com respostas diretas.
   * **Cobertura:** `test_currency_conversion_to_brl` e `test_regression_report_on_sample` (falhavam por efeito cascata do primeiro e segundo teste).

1.3. **`NO_SHOW` somado ao financeiro (`status_policy.py`)**
   * **Dor:** O valor `total_amount_brl` e `NO_SHOW` estavam sendo somados aos totais financeiros, ocasionando um resultado diferente de (`120.00` em vez de `100.00`).
   * **Causa Raiz:** O filtro era por exclusão (`status != "CANCELLED"`) que era usado por `is_billable`, permitindo que o `NO_SHOW` passasse direto.
   * **Correção:** Foi aplicado um filtro por inclusão `if status != "CONFIRMED": return False`, mantendo a mesma lógica de código limpo e direto.
   * **Cobertura:** `test_status_rules_exclude_cancelled_and_no_show`.

1.4. **Ordenação do Top Hotels (`report_builder.py`)**
   * **Dor:** `top_hotels` retornava com os hotéis mais 'fracos' em vez de priorizar os melhores resultados (`H01, H02, H03`).
   * **Causa Raiz:** A ordenação `sorted` estava ascendente e não previa o desempate por ID `hotel_id`.
   * **Correção:** Usei a chave composta `(key=lambda item: (-item[1]["amount"], item[0])` para ordenar o valor de forma decrescente e o ID `hotel_id` de forma ascendente, conforme as regras de negócio.
   * **Cobertura:** `test_top_hotels_are_ranked_descending`

1.5. **ERRO Oculto - Truncamento em 200 Linhas (`repositories/csv_reservation_repository.py`)**
   * **Dor:** O resultado `total_reservations` era fixado em `200` mesmo com a lista CSV com mais informações.
   * **Causa Raiz:** Há um comando `break` arbitrário dentro do loop de leitura do CSV, o que descarta o restante das reservas após 200ª, violando o "total_reservations = número de reservas no arquivo"
   * **Teste:** Antes, `reservas_hoteis.csv` retornava com (`200 reservas, 153 confirmadas, 909 noites e um total de R$249.543,79`), feito a remoção do `break` limitador de 200, obtivemos um resultado de (`300 reservas, 235 confirmadas, 1347 noites e um total de R$ 396.170,00`), o que ocasionava uma perda silenciosa de (`100 reservas, 82 confirmadas, 438 noites e R$146.626,21 reais`).
   * **Cobertura:** Não foi identificada pelos 5 testes fornecidos, foi identificado juntamente com a utilização da IA para apuração e exatidão das informações. 

## 2. Melhorias defensivas (não alteram os dados atuais)

2.1. **Ajuste utf-8 (`csv_rate_repository.py e csv_reservation_repository.py`)**
   * **Dor:** O formato `encoding="utf-8"` não tolera BOM (Byte Order Mark).
   * **Causa Raiz:** Ambos os arquivos se encontram com esta padronização, inviabilizando a visualização correta dos arquivos gerados em python.
   * **Correção:** Inserção do `-sig`após o `encoding="utf-8-sig"`, nos arquivos `csv_reservation_repository.py`e `csv_rate_repository.py`, passando a ser lido e compatível com o BOM, não alterando o dataset atual.

2.2. **Simetria de Dados (`row_parser.py`)**
   * **Dor:** Inconsistência na formatação do código da moeda, letras minúsculas ou espaços em branco durante a leitura dos dados.
   * **Causa Raiz:** O `row_parse.py` extraia e limpava espaços do campo `currency`, mas não normalizava a capitalização, quebrando a simetria com o padrão em maiúsculas que era aguardado pelo CsvRateRepository.
   * **Correção:** Adição do `.upper()`no encadeamento de limpeza do campo `currency=(values.get("currency") or "").strip().upper(),` garantindo e prevenindo `KeyError` se uma informação vier em minúsculo, não alterando o resultado do Dataset.

## 3. Abordagem e Investigação
- Utilizado o `pytest` para mapear os sintomas (causa raiz) e realizado a investigação cada arquivo na camada de `services`. 
- Isolando os testes (ex: `pytest tests/test_nights.py`), foi confirmado a causa raiz de cada um e corrigido um por um. 
- Por fim, foram validadas as informações obtidas com as amostras de validação do README.md e os testes foram auditados com para identificar outros dois problemas ocultos no desafio.

## 4. Aplicação de 'Early Return'
Para manter o código limpo e legível, foi adotado o padrão de Early return, em vez de aninhar condições com `if/else`, o código falha cedo (ou retorna o valor padrão) se uma regra de negócio não for atendida, resultando em um fluxo principal livre de aninhamentos, reduzindo a complexidade do código.

## 5. Separação de Responsabilidades (Layers)
A arquitetura do projeto separa muito bem as responsabilidades:

* **CLI / Report Builder (`cli.py`):** Organiza o fluxo (ler → converter → agregar) e lida com a apresentação final (formatação de strings, JSON), garantindo a injeção das dependências de forma correta conforme a regra de negócio.
* **Dados / Input (`data/`):** Contém os arquivos CSV de origem (reservas, taxas de câmbio e o exemplo de validação). É a fonte bruta de informação do projeto.
* **Repositories (`repositories/`):** Responsáveis apenas por ler e entregar os dados (CSV).
* **Services (`services/`):** Contém as regras de negócio puras (cálculo de noites, câmbio, status). Não sabem como o CLI funciona, o que permite testá-los isoladamente.
* **Models / Exceptions (`models.py`, `exceptions.py`):** São tipos do domínios.

Essa separação permite, por exemplo, testar o cálculo de noites ou de câmbio de forma isolada, sem precisar rodar o CLI inteiro ou depender de arquivos externos para isso.

## 6. Como validar
```bash
# Testes unitários
pytest -q

# Gerar relatório da amostra
python -m onfly_report --input data/exemplo-validacao.csv --rates data/taxas_cambio.csv --output output/exemplo.json

# Gerar o report
python -m onfly_report --input data/reservas_hoteis.csv --rates data/taxas_cambio.csv --output output/report.json

## 7. Resultado do Pytest
$ pytest -q
......    [100%]
6 passed in 0.90s
```

## 8. Testes adicionais
- Além dos testes fornecidos, foi adicionado um teste de casos de borda (zero rooms) arquivo `tests/test_zero_rooms.py`. O objetivo é validar uma reserva com rooms = 0 retorna 0 noites, onde foi bem sucedido.

## 9. Diferenças de ambientes
- No Windows PowerShell, o comando PYTHONPATH="src" do README original não funciona. Então utilizei a sintaxe $env:PYTHONPATH="src", e também é possível rodar de forma direta apenas com python -m... a partir da raiz do projeto, pois o sys.path já se encontra no diretório atual do projeto.

## 10. Uso de IA
- `[Utilizado IA]` Ferramenta de uso DeepSeek, modelo: DeepSeek (assistente de IA conversacional).
- `[sessao.md]` sessão em `entrega/uso-de-ia/sessao.md`.
- `[declaracao.md]` declaração em `entrega/uso-de-ia/declaracao.md`.
