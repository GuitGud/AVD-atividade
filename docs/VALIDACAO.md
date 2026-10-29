# Validação técnica · 29/10/2026

Ambiente: Python 3.12, Streamlit 1.66.0, pandas 2.3.3, Altair 6.3.0.

## Testes automatizados

Comando: `python -m unittest discover -s tests -v`.

**15 testes passaram.** Incluem:

- Correspondência do tratado com a EDA, exclusão dos seis incompletos e variáveis derivadas.
- Fórmulas de percentuais e medianas em uma amostra pequena com resposta conhecida.
- Denominador específico por grupo e combinações sem observações.
- Filtros inclusivos sem modificação do dataframe de origem.
- Duas abas presentes, cinco métricas e nove gráficos no estado inicial.
- Métodos Pearson, Spearman e Kendall; bins e separação de desfechos nos histogramas; proporções por faixa.
- Todos os filtros de medidas/desfecho e restauração.
- Seleções vazias, medida constante e amostra com um paciente.

Os testes do Streamlit executam a lógica e a árvore dos elementos das duas abas. Eles não reproduzem cliques em abas no navegador nem comprovam renderização em uma sessão pública.

## Conferência numérica

Sem filtros: 297 pacientes; 137 positivos; 97 com angina no esforço; 46,1% positivos; 32,7% com angina; medianas de idade 56, colesterol 243 e FC máxima 153.

Recorte de idade 45–60 e colesterol 200–260: 82 registros. As contagens de cada visual somam o recorte; percentuais por sexo usam o total de cada grupo.

## Dados e privacidade

O CSV tratado deriva do arquivo público da UCI e não contém nome, telefone, endereço, e-mail, documentos ou IDs de pacientes. O carregador limita os dados ao esquema conhecido. A tabela e o download expõem apenas medidas selecionadas e desfecho. Não há uso de secrets ou autenticação no app, e arquivos de ambiente/credenciais são ignorados pelo Git.

A revisão dos arquivos versionados é documentada na preparação do commit. Nenhum token é gravado no projeto. Dados médicos desta base pública não devem ser misturados com dados privados de novos pacientes.

## Verificação visual e limites

Os nove gráficos foram exportados a PNG a partir das mesmas especificações Altair do app para conferir escalas, legendas, rótulos e dados. Os dois rascunhos em PDF e o exemplo fictício foram renderizados e inspecionados.

**Pendente:** publicação, teste real das abas e dos widgets no navegador publicado, janela anônima e inclusão de link real do app no README. O controle de navegador foi interrompido por não identificar a URL com segurança. Não existe captura de tela ou resultado de teste remoto que comprove essas etapas.
