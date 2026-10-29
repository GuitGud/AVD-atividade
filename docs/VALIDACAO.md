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

## Aplicação publicada e verificação online

URL: https://avd-atividade-w5d8w43i4vfnpdt4ktapyr.streamlit.app/

Em 29/10/2026, o aluno publicou o app. Foi conferido acesso HTTPS 200 sem autenticação. Uma nova aba no navegador integrado carregou a aplicação sem login do autor, exibiu o laboratório e alternou para o segundo dashboard com os cinco KPIs esperados e os três visuais.

Foram exercitados os três métodos de correlação, o controle de classes dos histogramas, a separação por desfecho, os cinco sliders quantitativos, o filtro de desfecho e o controle de proporções por faixa. O recorte respondeu às alterações (por exemplo, 199 registros após elevar em um passo os cinco limites inferiores).

O teste online identificou restauração visual incompleta dos sliders: o backend voltava a 297 registros, mas os controles mantinham intervalos antigos na interação seguinte. A correção define explicitamente o estado de todos os filtros e usa somente uma origem para os valores iniciais. A suíte de 15 testes passou novamente e a correção foi verificada no navegador local. O commit 23fbf7c foi enviado para atualização automática do Streamlit. A reconferência dessa correção no servidor público permanece pendente.

Evidência: `entregas/evidencias/dashboard-2-publicado.png` (captura real da versão pública antes da correção, com KPIs de base integral).

**Limites:** o navegador integrado sem login não foi declarado equivalente a uma janela InPrivate. A tentativa de abrir o Edge para esse teste foi bloqueada pelo controle de URL do navegador. Os itens não exercitados e o teste InPrivate estão pendentes em `entregas/teste-app-publicado.md`.

Os cartões também foram ajustados para mostrar a unidade em linha própria, evitando truncamento de mg/dL. A suíte de 15 testes passou após esse ajuste; a conferência visual desse ajuste na publicação permanece pendente junto dos demais itens do navegador.
