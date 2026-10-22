# Dados · Heart Disease

Fonte: [UCI Machine Learning Repository, Heart Disease, ID 45](https://archive.ics.uci.edu/dataset/45/heart+disease).

Arquivo Cleveland: [processed.cleveland.data](https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data). Download realizado em 22/10/2026. Referência: Janosi, A., Steinbrunn, W., Pfisterer, M. e Detrano, R. (1989). Heart Disease. DOI: [10.24432/C52P4X](https://doi.org/10.24432/C52P4X). Licença declarada pela UCI: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

O arquivo baixado é preservado sem alterações em `raw/processed.cleveland.data`. O marcador `?` significa valor ausente. A ordem de colunas é `age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, num`.

O notebook exporta `raw/dataset_original.csv` antes de modificar o dataframe. O tratado em `clean/dataset.csv` remove linhas sem `ca` ou `thal`, converte o desfecho para duas classes e mantém as variáveis derivadas da EDA. Nenhum identificador pessoal é adicionado. Ambos os CSVs são UTF-8, separados por vírgula e sem índice.

| Coluna quantitativa | Significado | Unidade |
| --- | --- | --- |
| `age` | Idade | anos |
| `trestbps` | Pressão arterial em repouso | mmHg |
| `chol` | Colesterol sérico | mg/dL |
| `thalach` | Frequência cardíaca máxima atingida | bpm |
| `oldpeak` | Depressão de ST induzida por exercício, em relação ao repouso | escala registrada na base |

As demais variáveis originais são códigos de categorias ou exames: sexo (`sex`), tipo de dor (`cp`), glicemia em jejum (`fbs`), ECG (`restecg`), angina induzida por exercício (`exang`), inclinação de ST (`slope`), número de vasos (`ca`), resultado de exame de perfusão (`thal`) e diagnóstico (`num`).

A exclusão de casos incompletos reproduz a escolha da EDA encontrada. A ausência de apenas seis casos não demonstra por si só que o mecanismo é MCAR/MAR nem que a exclusão é isenta de viés. Não foram removidos extremos nem padronizadas as medidas para o dashboard desta etapa.
