# Justificativa técnica das métricas do Dashboard 2

**Público-alvo:** coordenadores de pesquisa cardiovascular.

**Objetivo do painel:** resumir a composição do recorte e as medidas registradas na amostra Cleveland, oferecendo uma visão descritiva que complemente o laboratório de distribuição e correlação.

O conjunto A foi selecionado pelo aluno. A redação abaixo é uma documentação técnica elaborada com apoio de IA, sem simular reflexão pessoal, validação humana ou conclusões clínicas.

## Relação entre as métricas e o objetivo do painel

| Métrica | Definição | Finalidade no painel | Unidade |
| --- | --- | --- | --- |
| Diagnóstico positivo | `100 * quantidade(doenca_cardiaca == 'Cardíaco') / n` | Mostrar a composição do desfecho na amostra selecionada, com numerador e denominador visíveis. | % do recorte |
| Angina no esforço | `100 * quantidade(exang == 1) / n` | Mostrar a frequência do sintoma registrado no teste dentro do mesmo recorte. | % do recorte |
| Idade mediana | `median(age)` | Caracterizar o centro da distribuição etária dos participantes. | anos |
| Colesterol mediano | `median(chol)` | Resumir o centro das medições de colesterol preservando a comparação com sua distribuição no laboratório. | mg/dL |
| FC máxima mediana | `median(thalach)` | Resumir a medida de frequência cardíaca máxima registrada no teste. | bpm |

Os dois percentuais resumem variáveis categóricas e as três medianas resumem medidas quantitativas distintas. A contagem total é exibida como contexto, sem ocupar um sexto cartão. Assim, o público consegue ler a composição do recorte e suas medidas centrais na mesma aba.

## Por que mediana nas três medidas

A mediana é o valor central após ordenar as observações. Ela não depende da magnitude dos extremos da mesma forma que a média. Como a EDA preserva outliers, essa escolha permite apresentar uma medida central sem excluir automaticamente observações extremas. Isso não torna a mediana sempre superior à média nem elimina a necessidade de olhar os histogramas; o Dashboard 1 mantém essas distribuições acessíveis.

## Coerência entre cartões, filtros e visuais

- Todos os cartões e gráficos usam o mesmo dataframe filtrado.
- Os intervalos são inclusivos e combinados com E; retirar uma medida do seletor também retira seu filtro de intervalo.
- O percentual por sexo usa o total de cada grupo, e não o total geral. Os tooltips mostram as contagens correspondentes.
- As barras por faixa etária podem mostrar contagens ou proporções dentro da própria faixa.
- A dispersão mostra colesterol e FC máxima por registro, mantendo a relação com duas medianas dos cartões.
- Filtrar apenas Cardíaco produz 100% de diagnóstico positivo por definição do filtro; isso não constitui descoberta sobre o risco dos pacientes.
- Recortes vazios são apresentados como **Sem dados**, sem converter ausência de observações em 0%.

## Conferência reproduzível

No conjunto tratado completo, há 297 registros, sendo 137 com desfecho Cardíaco e 97 com angina no esforço. Os valores esperados são:

- Diagnóstico positivo: `100 * 137 / 297 = 46,1279...%`, exibido como **46,1%**.
- Angina no esforço: `100 * 97 / 297 = 32,6599...%`, exibido como **32,7%**.
- Idade mediana: **56 anos**.
- Colesterol mediano: **243 mg/dL**.
- FC máxima mediana: **153 bpm**.

O recorte de idade entre 45 e 60 anos e colesterol entre 200 e 260 mg/dL contém 82 registros. Os testes automatizados também usam uma amostra artificial pequena, com respostas conhecidas, para distinguir mediana de média e verificar os denominadores sem depender apenas dos resultados do dataset.

## Limites de leitura

A base é histórica e foi formada por pacientes de um contexto clínico específico. Os percentuais descrevem a amostra disponível, não a prevalência ou o risco da população. A remoção de seis registros sem exames pode afetar sua composição. Comparações entre grupos são descritivas; os gráficos não demonstram causalidade, não controlam fatores de confusão e não orientam diagnóstico ou tratamento. A redução do recorte pode produzir grupos pequenos ou medidas constantes; esses casos recebem tratamento explícito na interface.

**Autoria e entrega:** este texto documenta as razões técnicas do desenho e as verificações automatizadas, sem afirmar que o aluno o redigiu sozinho.
