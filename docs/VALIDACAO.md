# Validação técnica · atualização de 03/11/2026

## Verificação local automatizada

Comando: `python -m unittest discover -s tests -v`.

A suíte de **19 testes** foi executada novamente. Ela verifica as fórmulas de percentuais e medianas, denominadores de grupos, correspondência entre original e tratado, filtros inclusivos, duas abas, cinco cartões, nove gráficos, todos os controles de entrada, restauração, seleções vazias, recorte sem pacientes, medida constante e amostra unitária.

A execução e as versões estão registradas em `entregas/validacao-automatizada.json`.

## Verificação do app publicado

Em 03/11/2026, a aplicação pública foi reativada após suspensão por inatividade. Os dois dashboards e seus controles foram exercitados sem login do autor no navegador integrado. O roteiro completo e suas evidências estão em [entregas/teste-app-publicado.md](../entregas/teste-app-publicado.md).

O teste confirmou a correção da restauração dos sliders no servidor público, inclusive após uma nova interação. Também confirmou o recorte de 82 pacientes, o CSV baixado, recorte vazio, zoom e tooltip da dispersão. As unidades dos cartões aparecem em linha própria.

O teste literal em janela InPrivate foi confirmado pelo aluno em 03/11/2026. Ele informou acesso sem login e funcionamento dos filtros e, após o ajuste, confirmou o funcionamento do método de correlação e do número de classes. Essa validação é humana e está identificada dessa forma no registro; o controle automatizado do Edge permaneceu bloqueado pela verificação de URL.

## Números de referência

Sem filtros: 297 pacientes; 137 com diagnóstico positivo; 97 com angina no esforço; 46,1% positivos; 32,7% com angina; medianas de idade 56, colesterol 243 e FC máxima 153.

Idade 45–60 e colesterol 200–260: 82 registros. O CSV baixado do app foi comparado, linha por linha, com o recorte local, sem diferenças nas seis colunas exportadas.

## Dados e privacidade

O dataset provém do arquivo público Cleveland Heart Disease da UCI. O carregador limita o esquema às colunas necessárias e o download expõe somente as quantitativas selecionadas e o desfecho. Não há nomes de pacientes, contatos, documentos ou credenciais nesses dados. A revisão do repositório exclui ambientes, caches e arquivos de secrets do versionamento.

Os percentuais são descritivos da base histórica e do recorte, sem extrapolação de prevalência, causalidade ou risco clínico.

## Arquivos de entrega

Os dois rascunhos PDF permanecem em entregas/, junto à justificativa técnica das métricas e às evidências dos testes. A declaração real não foi criada, modificada ou assinada; por orientação do aluno, será entregue separadamente, fora do repositório.

## Ajuste após o teste do aluno em 03/11/2026

O aluno confirmou acesso sem login e funcionamento dos filtros de recorte, mas relatou que a troca de método e o máximo de classes pareciam não responder. O cálculo de correlação foi conferido e produz coeficientes diferentes. A interface passou a destacar o método aplicado, exibir uma referência de quatro casas decimais e recriar o gráfico quando o método muda.

O histograma deixou de usar maxbins automático do Altair. Agora os intervalos são calculados previamente com NumPy, em quantidade exata definida pelo slider, incluindo o máximo na última classe e preservando a soma das observações. Os controles foram renomeados para Número de classes do histograma. Os 19 testes passaram e as prévias estáticas foram regeneradas. A reconferência humana desses dois controles na publicação foi concluída: o aluno respondeu "Sim, os dois controles agora funcionam" ao pedido de reteste na janela anônima.
