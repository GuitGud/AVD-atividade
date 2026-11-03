# Teste do app publicado · 03/11/2026

**Aplicação:** https://avd-atividade-w5d8w43i4vfnpdt4ktapyr.streamlit.app/

**Resultado da automação:** controles e visuais exercitados na versão pública, em uma nova aba do navegador integrado, sem login do autor. O teste posterior do aluno apontou dúvidas sobre dois controles; os ajustes e seu reteste estão descritos ao final. A aplicação estava suspensa por inatividade e foi reativada pelo botão público do Streamlit antes do teste.

**Janela InPrivate: confirmada pelo aluno em 03/11/2026.** Ele confirmou acesso sem login e funcionamento dos filtros de recorte e, após a atualização, respondeu ao pedido de reteste: "Sim, os dois controles agora funcionam". Essa confirmação refere-se à comparação de 5 e 25 classes e à troca Pearson/Spearman/Kendall solicitadas na janela anônima. Trata-se de confirmação humana, não de automação do Edge; o controle nativo permaneceu bloqueado pela verificação de URL.

## Casos executados

- [x] A aplicação abre publicamente sem autenticação no app.
- [x] As duas abas carregam: laboratório e panorama.
- [x] Laboratório apresenta mapa de calor e cinco histogramas na seleção inicial.
- [x] Panorama apresenta cinco cartões e três visuais adicionais.
- [x] KPIs integrais conferidos: 46,1%; 32,7%; medianas 56 anos, 243 mg/dL e 153 bpm.
- [x] Seletor de quantitativas exercitado com uma e nenhuma variável; avisos adequados.
- [x] Limites inferiores e superiores dos cinco sliders alterados pela interface.
- [x] Filtro de desfecho exercitado, incluindo seleção vazia.
- [x] Restauração reconferida no servidor público: ST volta de 0,1 a 0,0; a interação seguinte, filtrando Cardíaco, mantém intervalos restaurados e resulta em 137 registros e 100% de diagnóstico positivo.
- [x] Pearson, Spearman e Kendall selecionados, aguardando o mapa correspondente aparecer.
- [x] Máximo de classes do histograma alterado de 20 para 25; separação por desfecho ativada.
- [x] Controle de proporções por faixa etária ativado.
- [x] Recorte idade 45–60 e colesterol 200–260 resulta em 82 registros na aplicação pública.
- [x] CSV baixado pelo botão do app: 82 linhas e seis colunas; conteúdo idêntico ao recorte calculado localmente.
- [x] Recorte idade 29–29 e colesterol 260–260 resulta em zero registros; os cinco cartões mostram Sem dados e não ocorre erro.
- [x] Zoom da dispersão exercitado com a rolagem do mouse; limites dos eixos mudaram de aproximadamente 100–580/80–200 para 200–440/110–170.
- [x] Tooltip de um ponto exibiu idade 65, colesterol 360 mg/dL, FC máxima 151 bpm e desfecho Normal.
- [x] Expander aberto e prévia tabular exibida.
- [x] Link da fonte abriu uma nova aba para a página oficial da UCI.
- [x] Colunas do CSV conferidas: age, trestbps, chol, thalach, oldpeak e doenca_cardiaca; sem contatos, identificadores de pacientes ou credenciais.
- [x] Link do app presente no README.
- [x] Teste em janela InPrivate/anônima confirmado pelo aluno, incluindo o reteste bem-sucedido dos dois controles ajustados.

## Evidências atuais

- [Laboratório publicado](evidencias/dashboard-1-publicado-2026-11-03.png)
- [Panorama publicado](evidencias/dashboard-2-publicado-2026-11-03.png)
- [Zoom e tooltip no gráfico público](evidencias/zoom-tooltip-publicado-2026-11-03.png)
- [Validação automatizada e números de referência](validacao-automatizada.json)

As capturas são reais, obtidas na versão pública em 03/11/2026. O histórico de 29/10, inclusive a restauração incompleta identificada naquela ocasião, permanece nos commits anteriores. A restauração foi agora reconferida na publicação.

## Privacidade e limites

A revisão corresponde aos dados públicos efetivamente servidos pela aplicação e ao CSV baixado. Nenhuma coluna de identificação privada foi exibida ou exportada. Não se afirma uma auditoria geral da infraestrutura do provedor.

## Retorno do aluno e ajuste dos dois controles

Relato recebido em 03/11/2026: os filtros do recorte funcionam sem login; método de correlação e slider de máximo de classes pareciam não funcionar. O cálculo de correlação foi verificado como distinto entre os métodos. O título, a referência numérica e o redesenho do mapa foram tornados explícitos. O histograma agora usa número exato de classes calculadas previamente, em lugar do limite máximo automático do Altair.

O reteste solicitado foi: recarregar a aplicação na janela anônima, conferir **Número de classes do histograma**, comparar 5 com 25 classes e trocar Pearson/Spearman/Kendall, observando o título e o coeficiente de referência. O aluno confirmou em 03/11/2026: **"Sim, os dois controles agora funcionam"**. O relato inicial foi mantido acima como histórico do problema e da correção; não há pendência desse reteste.
