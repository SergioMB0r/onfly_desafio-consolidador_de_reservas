# Declaração de Uso de IA

## 1. Ferramenta e Modelo Utilizados
* **Ferramenta:** DeepSeek
* **Modelo:** DeepSeek (assistente de IA conversacional)

## 2. Como a IA foi utilizada (Apoio e Mentoria)
O uso da IA neste projeto foi estritamente voltado para **auxílio na resolução de dúvidas técnicas, revisão de conceitos e orientação de boas práticas**. 

É importante reforçar que a IA **não gerou ou implementou os códigos do projeto de forma autônoma**, nem escreveu os arquivos finais. O papel da ferramenta foi atuar como um mentor técnico durante o processo de debugging. Quando a IA sugeria trechos de código, esses trechos eram **exemplos conceituais e teóricos** para explicar o funcionamento da lógica (ex: como o sinal de `-` funciona no `sorted()` ou como estruturar um `if` de *early return*). A implementação real, a digitação, a aplicação nos arquivos e os testes foram realizados manualmente por mim.

## 3. O que a IA fez
* **Explicação de erros do `pytest`:** Auxiliou na interpretação das mensagens de falha (ex: entender por que o teste acusava `-28` noites ou `118.45` em vez de `642.00`), apontando em qual arquivo e função o defeito provavelmente estava.
* **Orientação sobre conceitos:** Explanou sobre como aplicar o padrão de *early return* (Guard Clauses) para substituir o uso de `else`, e forneceu exemplos teóricos de como estruturar a chave de ordenação composta no Python (`-amount, id`). A IA sugeriu o formato do código, mas a aplicação e adaptação foram feitas por mim.
* **Revisão de código:** Validou a sintaxe do teste adicional de caso de borda (zero quartos) e explicou o seu propósito de resiliência matemática e de engenharia.
* **Apoio na estruturação do README-ENTREGA:** Ajudou a organizar as ideias e a revisar a gramática, concordância e clareza do texto final, garantindo que a explicação sobre a separação em camadas (*Layers*) e a investigação dos defeitos ficassem coerentes e direto.
* **Resolução de problemas de ambiente:** Explicou a diferença de sintaxe para definir variáveis de ambiente no Windows PowerShell (`$env:PYTHONPATH="src"`) em comparação ao Linux/macOS.

## 4. O que eu (desenvolvedor) fiz
* **Leitura e Investigação:** Abri os arquivos da pasta `services`, li o código original e identifiquei, com base nas regras de negócio do README, o que se encontrava errado em cada função.
* **Testes e mapeamento de erros:** Identifiquei bugs no código durante a fase de testes para direcionar as correções do teste.
* **Correção do Código:** Apliquei as correções manuais nos arquivos `stay_calculator.py`, `currency_converter.py`, `status_policy.py`, `report_builder.py`, `csv_reservation_repository.py`, `csv_rate_repository.py` e `row_parser.py` inserindo *early return* em algumas correções.
* **Criação de Teste Adicional:** Escrevi um teste de caso de borda `test_room_nights_with_zero_rooms` para garantir que reservas com 0 quartos não quebrem o sistema.
* **Validação:** Executei os testes individualmente (`pytest tests/test_currency.py`, etc.) e depois o teste completo, além de rodar o CLI na amostra de validação para conferir campo a campo se as informações batiam com a documentação.
* **Redação da Entrega:** Escrevi o `README-ENTREGA.md` documentando as linhas de raciocínio, causas raízes e a visões sobre a arquitetura do projeto, utilizando a IA para auxilio nos códigos, duvidas, revisão e ajuste de textos.