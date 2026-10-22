# Explicação do resultado e da entrega

## O que foi feito

1. O notebook resolvido da Aula 11 foi copiado e atualizado para ler o Heart Disease localmente, sem `pip install` dentro das células nem consulta à UCI durante a execução.
2. A primeira leitura salva o dataframe original em `data/raw/dataset_original.csv`; o fim do notebook salva o tratado em `data/clean/dataset.csv`.
3. O aplicativo lê apenas o tratado. Cada mudança nos widgets reexecuta o script; o cache evita reler o CSV a cada interação.
4. O seletor escolhe quais medidas entram na futura correlação. Cada medida tem um slider de dois extremos, com limites inclusivos.
5. Os filtros são combinados com **E**: um paciente só aparece quando atende a todos os intervalos ativos. Desmarcar uma medida remove também seu filtro.
6. As duas áreas centrais são placeholders para os gráficos da próxima aula. Há uma prévia tabular para comprovar que o recorte funciona.

## Como demonstrar

- Abra o app. A seleção inicial mostra cinco medidas e **297 de 297 pacientes**.
- Restrinja a idade para 45 a 60 anos e observe a contagem e a prévia mudarem.
- Restrinja também o colesterol para 200 a 260 mg/dL. O novo recorte deve atender às duas condições.
- Selecione apenas uma medida para mostrar o aviso da correlação; selecione nenhuma para mostrar que o app continua funcionando.
- Explique que um recorte sem pacientes também tem aviso, sem erro de execução.

O filtro não altera o dataset tratado e não produz nova conclusão estatística nesta etapa. Ele prepara os dados que alimentarão os gráficos.

## Como explicar oralmente

> Usei o notebook de EDA de Heart Disease. Incluí o arquivo original da UCI e exportei os dataframes antes e depois do tratamento. A base passou de 303 para 297 pacientes pela remoção de seis registros com exames ausentes. No Streamlit, montei uma sidebar com seleção de variáveis e intervalos combinados. A área principal está dividida em correlação e distribuição. Os espaços dos gráficos estão reservados para a próxima aula, conforme o escopo da Aula 21.

## O que enviar

Aula 21, slides 21 e 22: **notebook + datasets + esqueleto funcional em um commit enviado ao GitHub**. Envie o link do repositório no local indicado pela professora. Se também for solicitado um arquivo, utilize o ZIP da entrega. Não inclua `.venv`, caches ou credenciais.

Antes de enviar, confira no GitHub se aparecem `app.py`, `notebooks/eda.ipynb`, `data/raw/dataset_original.csv` e `data/clean/dataset.csv`. Se o repositório for privado, a professora precisa ter acesso de leitura. O histórico do Git permite verificar esta etapa; não é preciso aguardar o dashboard final.

Texto sugerido para acompanhar o link:

> Entrega da Aula 21 – Streamlit parte 1. O repositório contém o notebook da EDA atualizado, os dados originais e tratados do Heart Disease e o esqueleto do Dashboard 1, com seleção de variáveis quantitativas, filtros de intervalo e áreas reservadas para correlação e distribuição. As instruções de execução estão no README.

Se o Heart Disease ainda não tiver sido aprovado como seu dataset próprio, alinhe com a professora e acrescente essa informação ao comentário da entrega. A atividade informa que mudanças de dataset ou ausência da EDA anterior precisam de alinhamento. O envio ao Classroom não é realizado por este projeto.

## Alterações técnicas no notebook

- Leitura local com caminhos relativos à raiz e identificação explícita de `?` como ausente.
- Exportação original antes de qualquer transformação, preservando `num`.
- Exportação final com os tratamentos já usados na EDA.
- Correção dos intervalos de faixa etária para os rótulos corresponderem aos limites.
- Nota conceitual: Pearson não exige normalidade para calcular o coeficiente; hipóteses adicionais são relevantes para inferência. Resultado não significativo também não prova igualdade ou normalidade.
- Registro do uso de IA e das validações executadas, sem atribuir revisão humana que ainda não aconteceu.
