# Métricas do Dashboard 2 - validação individual

**Público-alvo adotado no projeto:** coordenadores de pesquisa cardiovascular.

**Conjunto implementado:** A, escolhido pelo aluno durante a preparação. As definições abaixo documentam o cálculo; não são uma justificativa pessoal redigida em nome do aluno.

| Métrica | Definição técnica | Unidade / denominador |
| --- | --- | --- |
| Diagnóstico positivo | `100 * quantidade(doenca_cardiaca == 'Cardíaco') / n` | % dos pacientes do recorte |
| Angina no esforço | `100 * quantidade(exang == 1) / n` | % dos pacientes do recorte |
| Idade mediana | `median(age)` | anos |
| Colesterol mediano | `median(chol)` | mg/dL |
| FC máxima mediana | `median(thalach)` | bpm |

Todos os cartões usam o mesmo recorte. A contagem de pacientes e os dois numeradores ficam visíveis abaixo dos cartões. Recorte vazio aparece como **Sem dados**, sem produzir percentuais artificiais de 0%.

## Preenchimento pessoal antes da entrega

O template da professora reserva ao aluno a escolha, a justificativa e a validação das métricas. Complete os pontos abaixo com suas palavras:

1. Quem é seu público e que pergunta ele quer responder com este painel?
2. Por que você escolheu cada uma das cinco métricas? Relacione cada cartão a uma necessidade do público.
3. Por que usar mediana nas três medidas? Confira a definição e as distribuições da sua EDA.
4. Como você conferiu os valores? Registre os cálculos ou amostras que verificou pessoalmente.
5. Que limites da base histórica e dos filtros precisam ser considerados na leitura?

**Estado:** fórmulas implementadas e testadas; justificativa pessoal ainda a ser preenchida pelo aluno. Este arquivo não afirma autoria ou revisão humana que não ocorreu.
