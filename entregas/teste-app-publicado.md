# Teste do app publicado · verificação parcial em 29/10/2026

**URL:** https://avd-atividade-w5d8w43i4vfnpdt4ktapyr.streamlit.app/

**Ambiente verificado:** nova aba do navegador integrado, sem autenticação no app e sem login do autor. Isso não comprova uso de uma janela InPrivate.

**InPrivate:** pendente. A tentativa de controlar o Edge foi bloqueada por não ser possível confirmar a URL com segurança. Não foi marcado como concluído.

**Evidência:** [Dashboard 2 publicado](evidencias/dashboard-2-publicado.png). A imagem foi capturada na aplicação real, com recorte integral, antes da correção da restauração. Não é uma prévia estática dos gráficos.

## Resultado por item

- [x] URL pública responde HTTPS 200 sem autenticação.
- [x] Dashboard 1 abre na primeira aba, com mapa de calor e cinco histogramas.
- [x] Dashboard 2 abre na segunda aba, com cinco cartões e três visuais.
- [x] KPIs publicados sem filtros: 46,1%; 32,7%; 56 anos; 243 mg/dL; 153 bpm.
- [x] Pearson, Spearman e Kendall atualizam e exibem o mapa no servidor público.
- [x] Controle do máximo de classes foi alterado de 20 para 25 e separação por desfecho foi ativada.
- [x] Os cinco sliders de limites inferiores foram exercitados: idade 30, pressão 95, colesterol 127, FC 72 e ST 0,1; contagem atualizada para 199 pacientes.
- [x] Remoção de Normal no filtro de desfecho altera o recorte.
- [x] Controle de proporções por faixa responde na segunda aba.
- [x] Interface verificada mostra somente atributos da base pública, sem identificadores de pacientes ou credenciais.
- [x] Link público do app registrado no README.
- [ ] Teste específico em janela anônima/InPrivate.
- [ ] Seletor de quantitativas, opções vazias e todos os limites superiores exercitados no app publicado.
- [ ] Restauração dos filtros reconferida no app público após a correção do commit 23fbf7c.
- [ ] Recorte exato idade 45–60 e colesterol 200–260 confirmado no app público (82 registros nos testes locais).
- [ ] Recorte vazio confirmado no app público.
- [ ] Tooltips e zoom da dispersão exercitados.
- [ ] Expander, download CSV e link da fonte exercitados no servidor público.

## Correção encontrada no teste online

A versão inicial restaurava a contagem no backend, mas podia manter valores antigos dos sliders na interface. Isso foi corrigido usando `st.session_state` para atualizar explicitamente as variáveis, classes e intervalos. Os 15 testes locais passaram após a alteração e o navegador local mostrou o slider ST voltando de 0,1 a 0,0. A correção foi enviada ao GitHub para atualização automática do Streamlit; confirmar no servidor público antes de marcar a restauração acima.

## Roteiro para concluir em InPrivate

1. No Edge, pressione Ctrl+Shift+N e abra a URL pública.
2. Confirme os dois dashboards e altere os controles listados acima.
3. Restrinja um intervalo; clique em Restaurar filtros e confirme também a posição dos sliders. Em seguida, filtre apenas Cardíaco: deve haver 137 registros e KPI positivo de 100%.
4. Faça os recortes de 82 pacientes e vazio, baixe o CSV e confira suas colunas.
5. Registre responsável, data, horário, navegador e capturas. Marque somente itens efetivamente executados.

Os testes automatizados locais são documentados em docs/VALIDACAO.md e não substituem esta conferência.
