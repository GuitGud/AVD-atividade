# Validação da entrega

Verificação realizada em 22/10/2026, com Python 3.12 e Streamlit 1.66.0.

## Notebook

- 42 células de código executadas, de 42 existentes.
- Nenhuma saída de erro.
- Original: 303 linhas e 14 colunas.
- Tratado: 297 linhas e 17 colunas; nenhum valor ausente.
- Desfecho no tratado: 160 Normal e 137 Cardíaco.
- Ausências no original: quatro em `ca` e duas em `thal`; seis linhas removidas.

## Testes automatizados

Comando: `python -m unittest discover -s tests -v`.

Seis testes passaram:

1. Inicialização com 297 pacientes e cinco sliders.
2. Filtros inclusivos e combinados de idade e colesterol, com prévia coerente.
3. Recorte vazio sem erro.
4. Seleção reduzida a uma variável e preservação do intervalo da medida mantida.
5. Seleção sem variáveis, com avisos adequados.
6. Correspondência entre original e tratado, exclusões, classe binária e transformação de colesterol.

Recorte de demonstração: idade entre 45 e 60 anos **e** colesterol entre 200 e 260 mg/dL mantém **82 pacientes**.

## Conferência visual

Aplicativo aberto no navegador local. Sidebar, seleção de variáveis, sliders, contagem, duas áreas reservadas e prévia tabular conferidos. Os containers ajustam a altura ao conteúdo para evitar corte de texto.

Os gráficos da EDA permanecem no notebook executado. Os espaços no dashboard são intencionalmente reservados para a aula seguinte; não representam falha de implementação.
